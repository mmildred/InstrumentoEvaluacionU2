from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración de pines
sensor_ky033 = Pin(14, Pin.IN)  # Sensor KY-033 conectado al GPIO 14
led = Pin(2, Pin.OUT)  # LED en el GPIO 2 (usado como indicador)

# Configuración MQTT
MQTT_Broker = "192.168.137.233"
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "cliente_unico_1"

def wifi_connect():
    """Conectar o reconectar a la red WiFi"""
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("MARCOS 3310", "123456789")  # Cambia a tu SSID y contraseña

    for _ in range(30):  # Intentar conectar durante 30 intentos
        if sta_if.isconnected():
            return
        sleep(0.3)

    raise Exception("Error de conexión WiFi")

def conectar_mqtt():
    """Conectar o reconectar al broker MQTT"""
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=30)
            client.connect()
            return client
        except OSError:
            sleep(5)

def check_wifi():
    """Verifica si el WiFi sigue conectado"""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        wifi_connect()

# Conectar a WiFi
wifi_connect()

# Conectar al broker MQTT
client = conectar_mqtt()
contador = 0  # Contador de mensajes publicados

# Bucle principal
while True:
    check_wifi()  # Verifica conexión WiFi antes de publicar
    
    estado = sensor_ky033.value()  # Leer el sensor
    print(f"Estado del sensor: {estado}")  # Agregado para ver el valor leído del sensor
    
    mensaje = "Línea detectada (Oscuro)" if estado == 0 else "No hay línea (Claro)"
    print(f"Mensaje a enviar: {mensaje}")  # Imprime el mensaje antes de publicarlo

    if estado == 0:
        led.on()  # Encender LED
    else:
        led.off()  # Apagar LED

    try:
        client.publish(MQTT_TOPIC, mensaje)  # Enviar datos por MQTT
        contador += 1

        if contador >= 3:  # Verificar conexión MQTT solo después de varias publicaciones
            try:
                client.ping()  # Verificar si la conexión sigue activa
            except OSError:
                client.disconnect()
                client = conectar_mqtt()
            contador = 0  # Reiniciar el contador

    except OSError:
        client = conectar_mqtt()  # Intentar reconectar al broker
    
    sleep(5)  # Esperar 5 segundos para evitar saturación
