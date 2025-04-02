from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración del sensor KY-022
ir_sensor = Pin(25, Pin.IN)  # GPIO 12 como entrada

# Configuración MQTT
MQTT_Broker = "192.168.137.233"  # Cambia por la IP de tu broker MQTT
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    """Conectar a la red WiFi con reintentos"""
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Cambia a tu SSID y contraseña

    for _ in range(30):  # Intentar conectar durante 30 intentos
        if sta_if.isconnected():
            print("\nWiFi conectada:", sta_if.ifconfig())
            return
        print(".", end="")
        sleep(0.3)
    
    print("\nError: No se pudo conectar a WiFi")
    raise Exception("Error de conexión WiFi")

def conectar_mqtt():
    """Intentar conectar al broker MQTT con reintentos."""
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
            client.connect()
            print(f"Conectado a {MQTT_Broker}")
            return client
        except Exception as e:
            print(f"Error al conectar MQTT: {e}, reintentando en 5 segundos...")
            sleep(5)

# Conectar a WiFi y MQTT
wifi_connect()
client = conectar_mqtt()

# Variable para evitar publicaciones repetitivas
estado_anterior = ir_sensor.value()

while True:
    try:
        estado_actual = ir_sensor.value()  # Leer estado del sensor IR

        if estado_actual != estado_anterior:  # Solo publica si cambia
            if estado_actual == 0:
                print("🔴 Infrarrojos detectados")
                client.publish(MQTT_TOPIC, "Infrarrojos detectados")
            else:
                print("⚫ No hay infrarrojos")
                client.publish(MQTT_TOPIC, "No hay infrarrojos")

            estado_anterior = estado_actual  # Actualizar estado previo

    except Exception as e:
        print("Error de conexión MQTT:", e)
        client = conectar_mqtt()  # Reintentar conexión

    sleep(0.2)  # Evitar saturar el broker
