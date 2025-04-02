from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración del LED bicolor KY-029 (3 pines)
led_rojo = Pin(26, Pin.OUT)  # Pin para el LED rojo
led_azul = Pin(27, Pin.OUT)  # Pin para el LED azul

# Configuración MQTT
MQTT_Broker = "192.168.137.233"  # Cambia por la IP de tu broker MQTT
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "led_cliente"

def wifi_connect():
    """Conectar a la red WiFi con reintentos"""
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Cambia a tu SSID y contraseña

    for _ in range(30):  
        if sta_if.isconnected():
            print("\nWiFi conectada:", sta_if.ifconfig())
            return
        print(".", end="")
        sleep(0.3)
    
    print("\nError: No se pudo conectar a WiFi")
    raise Exception("Error de conexión WiFi")

def conectar_mqtt():
    """Intentar conectar al broker MQTT con reintentos"""
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
            client.connect()
            print(f"Conectado a {MQTT_Broker}")
            return client
        except:
            print("Reintentando conexión MQTT en 5 segundos...")
            sleep(5)

# Conectar WiFi y MQTT antes de ejecutar el código
wifi_connect()
client = conectar_mqtt()

# Secuencia de encendido y apagado del LED bicolor
while True:
    try:
        print("🔴 LED Rojo Encendido")
        client.publish(MQTT_TOPIC, "LED Rojo Encendido")
        led_rojo.value(1)
        led_azul.value(0)
        sleep(2)

        print("🔵 LED Azul Encendido")
        client.publish(MQTT_TOPIC, "LED Azul Encendido")
        led_rojo.value(0)
        led_azul.value(1)
        sleep(2)

        print("⚫ LED Apagado")
        client.publish(MQTT_TOPIC, "LED Apagado")
        led_rojo.value(0)
        led_azul.value(0)
        sleep(2)

    except:
        print("Reconectando MQTT...")
        client = conectar_mqtt()  # Reintentar conexión antes de continuar