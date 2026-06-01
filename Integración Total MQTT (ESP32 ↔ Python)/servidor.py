# =================================================================
# Práctica 2: Integración Total MQTT (ESP32 ↔ Python)
# Fecha: 08/05/26
# =================================================================
# Objetivo:
# Recibir la telemetría enviada por la ESP32 con marcas de tiempo y
# publicar comandos MQTT desde la laptop hacia los actuadores del sistema.
# =================================================================
# Integrantes de equipo:
# - Alvarez Guevara Estefania Guadalupe (ID: 23240077)
# - Rangel Hernandez Aldo (ID: 23240272)
# - Reyes Gutierrez Pablo Alberto (ID: 23240055)
# =================================================================

import paho.mqtt.client as mqtt
import json
from datetime import datetime

BROKER = "127.0.0.1" 
PORT = 1883

def on_connect(client, userdata, flags, rc):
    # Callback de conexión: al abrir sesión con el broker se activa la suscripción.
    print("Conectado a Mosquitto exitosamente.")
    client.subscribe("vestaguard/telemetria/sensores")

def on_message(client, userdata, msg):
    # Callback de mensaje: interpreta el JSON, agrega timestamp y muestra la telemetría.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        datos = json.loads(msg.payload.decode())
        print(f"[{timestamp}] PIR: {datos['pir']} | Dist: {datos['distancia_cm']}cm | MPU: {datos['aceleracion_y']}")
    except Exception:
        # Si el payload no es JSON válido, se ignora sin detener la consola.
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    # Consola de control: lo que el usuario escribe se publica por MQTT hacia la ESP32.
    print("ESCRIBE UN COMANDO (VIB_ON, VIB_OFF, LED_ROJO, LED_VERDE, LED_OFF) Y PRESIONA ENTER:")
    while True:
        # El prompt vacío evita mezclar el texto del usuario con la telemetría entrante.
        comando = input("").strip().upper()
        
        if comando == 'VIB_ON':
            client.publish("vestaguard/control/vibrador", "ON")
            print(f"--> RED: Comando {comando} enviado a Mosquitto.")
        elif comando == 'VIB_OFF':
            client.publish("vestaguard/control/vibrador", "OFF")
            print(f"--> RED: Comando {comando} enviado a Mosquitto.")
        elif comando == 'LED_ROJO':
            client.publish("vestaguard/control/rgb", "ROJO")
            print(f"--> RED: Comando {comando} enviado a Mosquitto.")
        elif comando == 'LED_VERDE':
            client.publish("vestaguard/control/rgb", "VERDE")
            print(f"--> RED: Comando {comando} enviado a Mosquitto.")
        elif comando == 'LED_OFF':
            client.publish("vestaguard/control/rgb", "APAGAR")
            print(f"--> RED: Comando {comando} enviado a Mosquitto.")
            
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()