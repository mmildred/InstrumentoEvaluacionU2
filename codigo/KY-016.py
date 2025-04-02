from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

# Configuración de MQTT
MQTT_Broker = "192.168.137.233"
MQTT_TOPIC_RGB = "utng/cm"
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
    client.subscribe(MQTT_TOPIC_RGB)
    print("Conectado a %s, suscrito a %s" % (MQTT_Broker, MQTT_TOPIC_RGB))
    return client

# Conectar al WiFi
wifi_connect()

# Conectar y suscribirse a MQTT
client = subscribir()

# Definir pines de conexión del KY-016
RED_PIN = 15   # Conectar al pin GPIO 15
GREEN_PIN = 2  # Conectar al pin GPIO 2
BLUE_PIN = 4   # Conectar al pin GPIO 4

# Configurar los pines PWM
red = PWM(Pin(RED_PIN), freq=1000)
green = PWM(Pin(GREEN_PIN), freq=1000)
blue = PWM(Pin(BLUE_PIN), freq=1000)

# Función para establecer color
def set_color(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

# Lista de colores (duty de 0 a 1023, donde 0 es encendido y 1023 es apagado)
colors = [
    (0, 0, 1023, "Azul"),   # Azul (Solo Azul encendido)
    (0, 1023, 0, "Verde"),  # Verde (Solo Verde encendido)
    (1023, 0, 0, "Rojo"),   # Rojo (Solo Rojo encendido)
]

while True:
    for r, g, b, color_name in colors:
        set_color(r, g, b)
        print(f"Color: {color_name}")

        # Publicar el color en MQTT
        client.publish(MQTT_TOPIC_RGB, color_name)

        time.sleep(3)  # Esperar 3 segundos
