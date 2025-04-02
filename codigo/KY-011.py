from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT (manteniendo tu estructura original)
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_RGB = "utng/rgb"  # Topic para control RGB
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky011"

# Configuración pines KY-011 (ÁNODO COMÚN - Valores invertidos)
RED_PIN = 15   # GPIO15 - Canal rojo
GREEN_PIN = 2  # GPIO2 - Canal verde
BLUE_PIN = 4   # GPIO4 - Canal azul

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
    mensaje = msg.decode()
    print(f"Comando MQTT recibido: {mensaje}")
    
    try:
        # Formato esperado: "R,G,B" (ej: "255,0,128")
        r, g, b = map(int, mensaje.split(','))
        set_rgb(r, g, b)
    except:
        print("Error: Formato debe ser 'R,G,B' (0-255)")

def init_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(MQTT_TOPIC_RGB)
    print(f"MQTT conectado | Broker: {MQTT_BROKER} | Topic: {MQTT_TOPIC_RGB}")
    return client

# Configuración PWM para KY-011 (ÁNODO COMÚN)
red = PWM(Pin(RED_PIN), freq=1000)
green = PWM(Pin(GREEN_PIN), freq=1000)
blue = PWM(Pin(BLUE_PIN), freq=1000)

def set_rgb(r, g, b):
    # Convertir 0-255 a duty cycle 1023-0 (ÁNODO COMÚN)
    red.duty(1023 - int(r * 1023 / 255))
    green.duty(1023 - int(g * 1023 / 255))
    blue.duty(1023 - int(b * 1023 / 255))
    print(f"Color actualizado: R={r} G={g} B={b}")

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

# Secuencia de inicio
print("KY-011 - Control LED RGB iniciado")
set_rgb(0, 0, 0)  # Iniciar apagado

try:
    while True:
        # Esperar mensajes MQTT
        mqtt_client.check_msg()
        time.sleep(0.1)
        
except KeyboardInterrupt:
    set_rgb(0, 0, 0)  # Apagar al salir
    print("Programa terminado")