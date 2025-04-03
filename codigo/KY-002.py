from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

Led = Pin(22, Pin.OUT)  
PinSensor = Pin(18, Pin.IN)

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
        Led.value(1)  
    elif msg == b'0':
        Led.value(0)  

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, suscrito a %s" % (MQTT_Broker, MQTT_TOPIC))
    return client


wifi_connect()

client = subscribir()

estado_anterior = PinSensor.value()

while True:
    client.check_msg() 
    estado_actual = PinSensor.value()  
  
  if estado_actual != estado_anterior: 
      if estado_actual == 1:  
          Led.value(1)  
          client.publish(MQTT_TOPIC, "1")  
      else:
          Led.value(0)  
          client.publish(MQTT_TOPIC, "0")  

      print("Cambio detectado:", estado_actual)  
      estado_anterior = estado_actual  
  
  time.sleep(0.1)  