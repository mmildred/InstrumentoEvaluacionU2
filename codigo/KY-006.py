from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración del buzzer
buzzer = Pin(12, Pin.OUT)  # KY-006 conectado al GPIO 12

# Configuración MQTT
MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    """Conectar a la red WiFi"""
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
    """Conectar al broker MQTT"""
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_Broker}")
    return client

# Conectar a WiFi
wifi_connect()

# Conectar al broker MQTT
client = conectar_mqtt()

# Bucle principal
while True:
    buzzer.value(1)  # Encender buzzer
    print("Buzzer encendido")
    client.publish(MQTT_TOPIC, "Buzzer encendido")  # Publicar mensaje MQTT
    sleep(3)  # Esperar 3 segundos

    buzzer.value(0)  # Apagar buzzer
    print("Buzzer apagado")
    client.publish(MQTT_TOPIC, "Buzzer apagado")  # Publicar mensaje MQTT
    sleep(3)  # Esperar 3 segundos
