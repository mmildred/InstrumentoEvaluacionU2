from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient

HALL_PIN = 14
led = Pin(2, Pin.OUT)
sensor = Pin(HALL_PIN, Pin.IN, Pin.PULL_UP)

MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    print("Conectando", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("\nWiFi conectada")

def llegada_mensaje(topic, msg):
    print("Mensaje recibido:", msg)
    if msg == b'1':
        ledPin.value(1)  
    elif msg == b'0':
        ledPin.value(0)

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, suscrito a %s" % (MQTT_Broker, MQTT_TOPIC))
    return client

wifi_connect()
client = subscribir()

while True:
    client.check_msg()

    estado = sensor.value()
        
    mensaje = "ALERTA_MAGNETICA" if estado == 0 else "NORMAL"
    client.publish(MQTT_TOPIC, mensaje)
    print("Estado:", mensaje)
        
    led.value(0 if estado else 1)
    sleep(0.5)