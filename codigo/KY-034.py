from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT (manteniendo tu estructura)
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_TILT = "utng/tilt"  # Topic para estado de inclinación
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky034"

# Configuración del pin KY-034 (ESP32)
TILT_PIN = 34  # GPIO34 para lectura digital

def wifi_connect():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    
    print("\nWiFi Conectada | IP:", sta_if.ifconfig()[0])

def mqtt_callback(topic, msg):
    print("MQTT:", topic.decode(), "->", msg.decode())

def init_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(MQTT_TOPIC_TILT)
    print(f"MQTT conectado | Broker: {MQTT_BROKER} | Topic: {MQTT_TOPIC_TILT}")
    return client

# Configuración KY-034
tilt = Pin(TILT_PIN, Pin.IN, Pin.PULL_UP)  # Resistencia pull-up interna

def leer_inclinacion():
    return tilt.value()  # 0=Inclinado, 1=Vertical

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

print("KY-034 - Sensor de inclinación activo")
ultimo_estado = None

while True:
    estado_actual = leer_inclinacion()
    
    # Solo publicar si hay cambio de estado
    if estado_actual != ultimo_estado:
        estado_str = "INCLINADO" if estado_actual == 0 else "VERTICAL"
        print(f"Estado: {estado_str}")
        mqtt_client.publish(MQTT_TOPIC_TILT, estado_str)
        ultimo_estado = estado_actual
    
    time.sleep(0.1)  # Muestreo rápido para detectar cambios bruscos