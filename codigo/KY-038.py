from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración MQTT (manteniendo tu estructura original)
MQTT_BROKER = "192.168.137.233"
MQTT_TOPIC_SOUND = "utng/sound"  # Topic para datos de sonido
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_ky038"

# Configuración pines KY-038 (ESP32)
ANALOG_PIN = 34  # GPIO34 (ADC1_CH6) - Salida analógica
DIGITAL_PIN = 35  # GPIO35 - Salida digital (opcional)

def wifi_connect():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Tus credenciales

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
    client.subscribe(MQTT_TOPIC_SOUND)
    print(f"MQTT conectado a {MQTT_BROKER} | Topic: {MQTT_TOPIC_SOUND}")
    return client

# Configuración hardware KY-038
adc = ADC(Pin(ANALOG_PIN))
adc.atten(ADC.ATTN_11DB)  # Rango 0-3.6V
digital_in = Pin(DIGITAL_PIN, Pin.IN)  # Configuración pin digital

def leer_sensor():
    # Lectura analógica (0-4095)
    analog_val = adc.read()
    
    # Lectura digital (0/1)
    digital_val = digital_in.value()
    
    # Calcular intensidad relativa (0-100%)
    intensity = (analog_val / 4095) * 100
    
    return {
        "analog": analog_val,
        "digital": digital_val,
        "intensity": intensity
    }

# Programa principal
wifi_connect()
mqtt_client = init_mqtt()

print("KY-038 - Micrófono activo")

while True:
    datos = leer_sensor()
    
    # Formato del mensaje JSON-like
    mensaje = f"""
    {{
        "analogico": {datos['analog']},
        "digital": {datos['digital']},
        "intensidad": {datos['intensity']:.1f}%
    }}
    """
    
    print("Datos:", mensaje.strip())
    mqtt_client.publish(MQTT_TOPIC_SOUND, mensaje)
    
    time.sleep(1)  # Intervalo de muestreo