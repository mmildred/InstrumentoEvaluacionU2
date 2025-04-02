from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT (conservando tu estructura)
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_REED = "utng/reed"  # Topic para estado magnético
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky004"

# Configuración pin KY-004 (ESP32)
REED_PIN = 34  # GPIO34 para lectura digital (adaptable)

def wifi_connect():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Tus credenciales

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
    client.subscribe(MQTT_TOPIC_REED)
    print(f"MQTT conectado | Broker: {MQTT_BROKER} | Topic: {MQTT_TOPIC_REED}")
    return client

# Configuración KY-004
reed = Pin(REED_PIN, Pin.IN, Pin.PULL_UP)  # Resistencia pull-up interna

def leer_estado():
    return reed.value()  # 0=Activo (campo magnético), 1=Inactivo

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

print("KY-004 - Monitor magnético iniciado")
ultimo_estado = None

while True:
    estado_actual = leer_estado()
    
    # Solo publicar si hay cambio de estado
    if estado_actual != ultimo_estado:
        estado_str = "CERCADO" if estado_actual == 0 else "ABIERTO"
        print(f"Estado: {estado_str}")
        mqtt_client.publish(MQTT_TOPIC_REED, estado_str)
        ultimo_estado = estado_actual
    
    time.sleep(0.5)  # Anti-rebote y ahorro energético