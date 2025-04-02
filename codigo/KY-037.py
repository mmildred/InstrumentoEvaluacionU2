from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT
MQTT_Broker = "192.168.137.233"
MQTT_TOPIC_SOUND = "utng/sound"  # Cambiado a topic de sonido
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

# Configuración KY-037
MIC_PIN = 34  # Pin analógico (GPIO34 - ADC1_CH6)
DIGITAL_PIN = 35  # Pin digital (GPIO35) - Opcional para detección digital

def wifi_connect():
    print("Conectando al WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    
    print("\nWiFi conectada")
    print("Dirección IP:", sta_if.ifconfig()[0])

def llegada_mensaje(topic, msg):
    print("Mensaje recibido:", topic.decode(), msg.decode())

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC_SOUND)
    print(f"Conectado a {MQTT_Broker}, topic: {MQTT_TOPIC_SOUND}")
    return client

# Hardware setup
adc = ADC(Pin(MIC_PIN))
adc.atten(ADC.ATTN_11DB)  # Rango completo 0-3.6V
digital_in = Pin(DIGITAL_PIN, Pin.IN)  # Pin digital opcional

def leer_sonido():
    # Lectura analógica (0-4095)
    analog_value = adc.read()
    # Lectura digital (0 o 1)
    digital_value = digital_in.value()
    
    # Calcular amplitud relativa (0-100%)
    amplitude = (analog_value / 4095) * 100
    
    return analog_value, digital_value, amplitude

# Main
wifi_connect()
client = subscribir()

print("Iniciando monitor de sonido KY-037...")

while True:
    analog, digital, amp = leer_sonido()
    
    # Formato: "ANALOG:valor,DIGITAL:valor,AMPLITUD:valor%"
    msg = f"ANALOG:{analog},DIGITAL:{digital},AMPLITUD:{amp:.1f}%"
    
    print(msg)
    client.publish(MQTT_TOPIC_SOUND, msg)
    
    time.sleep(1)  # Muestreo cada 1 segundo