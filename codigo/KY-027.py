from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_CUP = "utng/magiccup"  # Topic para el módulo de copa mágica
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky027"

# Configuración pines KY-027 (ESP32)
LED_PIN = 15    # GPIO15 para el LED
SENSOR_PIN = 34 # GPIO34 (ADC) para el sensor de mercurio

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
    print("MQTT:", topic.decode(), "->", msg.decode())

def init_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(MQTT_TOPIC_CUP)
    print(f"MQTT conectado | Broker: {MQTT_BROKER} | Topic: {MQTT_TOPIC_CUP}")
    return client

# Configuración KY-027
led = Pin(LED_PIN, Pin.OUT)
sensor = ADC(Pin(SENSOR_PIN))
sensor.atten(ADC.ATTN_11DB)  # Rango completo 0-3.6V

def leer_sensor():
    return sensor.read()  # Valor ADC 0-4095

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

print("KY-027 - Módulo Copa Mágica iniciado")
umbral = 1500  # Ajustar según sensibilidad necesaria

while True:
    valor_sensor = leer_sensor()
    deteccion = valor_sensor > umbral
    
    # Controlar LED
    led.value(deteccion)
    
    # Publicar estado
    estado = "DETECTADO" if deteccion else "AUSENTE"
    mensaje = f"{estado},{valor_sensor}"
    mqtt_client.publish(MQTT_TOPIC_CUP, mensaje)
    
    print(f"Valor: {valor_sensor} | Estado: {estado}")
    time.sleep(0.5)