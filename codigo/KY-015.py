from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network
import dht

# Configuración del sensor KY-015 (DHT11 o DHT22)
sensor = dht.DHT11(Pin(12))  # KY-015 conectado al GPIO 12

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
    try:
        sensor.measure()  # Tomar medición
        temperatura = sensor.temperature()  # Obtener temperatura en °C
        humedad = sensor.humidity()  # Obtener humedad en %

        mensaje = f"Temp: {temperatura}°C, Hum: {humedad}%"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)  # Publicar en MQTT

    except Exception as e:
        print("Error al leer el sensor:", e)

    sleep(5)  # Esperar 5 segundos antes de la siguiente lectura
