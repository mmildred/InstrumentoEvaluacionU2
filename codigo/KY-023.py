from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient
import network

# Configuración del joystick KY-023
joy_x = ADC(Pin(34))  # Eje X
joy_y = ADC(Pin(35))  # Eje Y
joy_sw = Pin(25, Pin.IN, Pin.PULL_UP)  # Botón del joystick

joy_x.atten(ADC.ATTN_11DB)  # Configurar rango de voltaje
joy_y.atten(ADC.ATTN_11DB)

# Configuración MQTT
MQTT_Broker = "192.168.137.233"  # Cambia por la IP de tu broker MQTT
MQTT_TOPIC = "utng/cm"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "joystick_cliente"

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
    """Intentar conectar al broker MQTT con reintentos antes de iniciar el código del sensor"""
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_Broker, port=MQTT_PORT, keepalive=60)
            client.connect()
            print(f"Conectado a {MQTT_Broker}")
            return client
        except:
            print("Reintentando conexión MQTT en 5 segundos...")
            sleep(5)

# Primero conectar WiFi y MQTT antes de ejecutar el sensor
wifi_connect()
client = conectar_mqtt()

# Inicia la lectura del sensor solo después de la conexión exitosa
while True:
    try:
        x_value = joy_x.read()
        y_value = joy_y.read()

        # Determinar dirección
        if x_value < 1500:
            direccion = "Derecha"
        elif x_value > 2500:
            direccion = "Izquierda"
        elif y_value < 1500:
            direccion = "Abajo"
        elif y_value > 2500:
            direccion = "Arriba"
        else:
            direccion = "Centro"

        print(direccion)  # Solo imprime la dirección
        client.publish(MQTT_TOPIC, direccion)  # Solo envía la dirección

    except:
        print("Reconectando MQTT...")
        client = conectar_mqtt()  # Reintentar conexión antes de continuar

    sleep(1)  # Control del envío de datos