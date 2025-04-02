from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_OBSTACLE = "utng/obstacle"  # Topic para detección de obstáculos
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky032"

# Configuración del pin KY-032 (ESP32)
IR_PIN = 34  # GPIO34 para lectura digital (OUT del sensor)

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
    client.subscribe(MQTT_TOPIC_OBSTACLE)
    print(f"MQTT conectado | Broker: {MQTT_BROKER} | Topic: {MQTT_TOPIC_OBSTACLE}")
    return client

# Configuración KY-032
obstacle_sensor = Pin(IR_PIN, Pin.IN)

def leer_sensor():
    return obstacle_sensor.value()  # 0=Obstáculo detectado, 1=Libre

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

print("KY-032 - Sensor de obstáculos iniciado")
ultimo_estado = None

while True:
    estado_actual = leer_sensor()
    
    # Solo publicar si hay cambio de estado
    if estado_actual != ultimo_estado:
        estado_str = "OBSTACULO" if estado_actual == 0 else "LIBRE"
        print(f"Estado: {estado_str}")
        mqtt_client.publish(MQTT_TOPIC_OBSTACLE, estado_str)
        ultimo_estado = estado_actual
    
    time.sleep(0.1)  # Muestreo rápido para respuesta inmediata