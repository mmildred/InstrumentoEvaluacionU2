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

# Callback cuando se recibe un mensaje MQTT
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

# Definir pines de conexión del KY-016 SMD
RED_PIN = 15   # GPIO 15 - Rojo
GREEN_PIN = 2  # GPIO 2 - Verde
BLUE_PIN = 4   # GPIO 4 - Azul

# Configurar los pines PWM
red = PWM(Pin(RED_PIN), freq=1000)
green = PWM(Pin(GREEN_PIN), freq=1000)
blue = PWM(Pin(BLUE_PIN), freq=1000)

# Función para establecer el color
def set_color(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

# Lista de colores (duty de 0 a 1023, donde 0 es encendido y 1023 es apagado)
colors = [
    (1023, 1023, 0, "Azul"),      # Azul (Solo Azul encendido)
    (1023, 0, 1023, "Verde"),     # Verde (Solo Verde encendido)
    (0, 1023, 1023, "Rojo"),      # Rojo (Solo Rojo encendido)
    (1023, 0, 0, "Cian"),         # Cian (Verde y Azul encendidos)
    (0, 1023, 0, "Magenta"),      # Magenta (Rojo y Azul encendidos)
    (0, 0, 1023, "Amarillo"),     # Amarillo (Rojo y Verde encendidos)
    (0, 0, 0, "Blanco"),          # Blanco (Todos encendidos)
    (500, 1023, 0, "Naranja"),    # Naranja (Rojo intenso, Verde medio)
    (0, 500, 1023, "Rosa"),       # Rosa (Rojo fuerte con azul bajo)
    (500, 0, 500, "Morado"),      # Morado (Rojo y Azul a media intensidad)
    (700, 700, 700, "Gris"),      # Gris (Intensidad media en todos los colores)
    (1023, 700, 200, "Celeste"),  # Celeste (Azul medio, Verde alto)
]

while True:
    for r, g, b, color_name in colors:
        set_color(r, g, b)
        print(f"Color: {color_name}")

        # Publicar el color en MQTT
        client.publish(MQTT_TOPIC_RGB, color_name)

        time.sleep(1)  # Esperar 1 segundo
