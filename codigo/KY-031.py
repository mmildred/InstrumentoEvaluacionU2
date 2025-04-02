from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración del sensor de vibración KY-031 (2 pines: GND, Signal)
sensor_vibracion = Pin(26, Pin.IN)  # Pin de señal (conectar al pin GPIO deseado)

# Configuración MQTT
MQTT_Broker = "192.168.137.233"  # Cambia por la IP de tu broker MQTT
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    """Conectar a la red WiFi con reintentos"""
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Cambia a tu SSID y contraseña

    for _ in range(30):  
        if sta_if.isconnected():
            print("\nWiFi conectada:", sta_if.ifconfig())
            return
        print(".", end="")
        sleep(0.3)
    
    print("\nError: No se pudo conectar a WiFi")
    raise Exception("Error de conexión WiFi")

def conectar_mqtt():
    """Intentar conectar al broker MQTT con reintentos"""
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
            client.connect()
            return client  # Solo retornamos el cliente si la conexión es exitosa
        except Exception:
            sleep(5)  # Intentar reconectar en 5 segundos, pero sin imprimir nada

# Conectar WiFi y MQTT antes de ejecutar el código
wifi_connect()
client = conectar_mqtt()

# Monitoreo de vibración
while True:
    try:
        estado_vibracion = sensor_vibracion.value()  # Leer valor de la señal

        if estado_vibracion == 1:
            print("💥 Vibración detectada")
            client.publish(MQTT_TOPIC, "Vibración detectada")  # Publica cuando hay vibración
        else:
            print("⚫ No hay vibración")
            client.publish(MQTT_TOPIC, "No hay vibración")  # Publica cuando no hay vibración
        
        sleep(1)

    except Exception:
        # Reintentar la conexión MQTT sin imprimir mensajes de error
        client = conectar_mqtt()  # Reconectar al broker sin mostrar el mensaje de error