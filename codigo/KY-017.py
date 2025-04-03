from machine import Pin, PWM
from time import sleep
import network
from umqtt.simple import MQTTClient

MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

sensor_pin = 12  
sensor = Pin(sensor_pin, Pin.IN)
ledPin = Pin(2, Pin.OUT)
ledPin.value(0)

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

estado_anterior = sensor.value()

while True:
    client.check_msg()  
    estado_actual = sensor.value()
  
  if estado_actual != estado_anterior:  
      if estado_actual == 1:
          print("✅ Posición vertical (Estado: 0)")
          client.publish(MQTT_TOPIC, "0")  
      else:
          print("⚠️ Posición inclinada (Estado: 1)")
          client.publish(MQTT_TOPIC, "1")  
  
  estado_anterior = estado_actual  
  sleep(1)