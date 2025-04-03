import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin, ADC

AO_PIN = ADC(Pin(35))  
AO_PIN.atten(ADC.ATTN_11DB)

led = Pin(2, Pin.OUT)  
led.value(0)  

MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    """Conectar a la red WiFi"""
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")

    for _ in range(30):  
        if sta_if.isconnected():
            print("\nWiFi conectada:", sta_if.ifconfig())
            return
        print(".", end="")
        sleep(0.3)
    
    print("\nError: No se pudo conectar a WiFi")

def llegada_mensaje(topic, msg):
    """Callback para manejar mensajes MQTT"""
    print("Mensaje recibido:", msg)
    if msg == b'1':
        led.value(1)
    elif msg == b'0':
        led.value(0)

def subscribir():
    """Conectar al broker MQTT y suscribirse al tópico"""
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print(f"Conectado a {MQTT_Broker}, suscrito a {MQTT_TOPIC}")
    return client

wifi_connect()
client = subscribir()

ultimo_valor = None  

while True:
    client.check_msg()  
    valor = AO_PIN.read() 
    temperaturaN = (valor / 4095.0) * 100  #
    temperaturaRedo = round(temperaturaN, 2) 
  
  print("Dato:", temperaturaRedo, "°C")
  
  if temperaturaRedo != ultimo_valor:
      print("Nueva temperatura detectada:", temperaturaRedo)
      client.publish(MQTT_TOPIC, str(temperaturaRedo))
      print("Dato publicado:", temperaturaRedo)
      
      led.value(1)
      sleep(0.2)
      led.value(0)
      
      ultimo_valor = temperaturaRedo
  
  sleep(1)  