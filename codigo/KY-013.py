from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient
import math

# Configuración de MQTT
MQTT_Broker = "192.168.137.233"
MQTT_TOPIC_TEMP = "utng/temp"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    print("Conectando al WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    
    print("\nWiFi conectada")
    print("Dirección IP:", sta_if.ifconfig()[0])  # Muestra la IP asignada
    
# Función de callback para cuando llega un mensaje MQTT
def llegada_mensaje(topic, msg):
    print("Mensaje recibido en el topic:", topic.decode())
    print("Contenido:", msg.decode())

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC_TEMP)
    print("Conectado a %s, suscrito a %s" % (MQTT_Broker, MQTT_TOPIC_TEMP))
    return client

# Conectar al WiFi
wifi_connect()

# Conectar y suscribirse a MQTT
client = subscribir()

# Configuración del sensor KY-013 (Termistor NTC)
THERMISTOR_PIN = 34  # Conectar al pin GPIO34 (ADC1_CH6)
adc = ADC(Pin(THERMISTOR_PIN))
adc.atten(ADC.ATTN_11DB)  # Rango completo de 0-3.6V

# Parámetros del termistor
R0 = 10000  # Resistencia a 25°C (10k ohm)
T0 = 298.15  # Temperatura de referencia en Kelvin (25°C)
B = 3950    # Valor B del termistor
R
