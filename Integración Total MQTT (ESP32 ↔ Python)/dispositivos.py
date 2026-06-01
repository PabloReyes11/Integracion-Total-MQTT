# =================================================================
# Práctica 2: Integración Total MQTT (ESP32 ↔ Python)
# Fecha: 08/05/26
# =================================================================
# Objetivo:
# Definir la capa HAL del proyecto para abstraer la lectura de sensores
# y el control de actuadores sin acceder directamente al hardware desde
# la lógica de red MQTT.
# =================================================================
# Integrantes de equipo:
# - Alvarez Guevara Estefania Guadalupe (ID: 23240077)
# - Rangel Hernandez Aldo (ID: 23240272)
# - Reyes Gutierrez Pablo Alberto (ID: 23240055)
# =================================================================


from machine import Pin, PWM, I2C, time_pulse_us
import time
import struct  # Conversión de bytes crudos del MPU6050 a enteros con signo.

class SensorBox:
    def __init__(self):
        # Entradas físicas de la capa HAL: movimiento y distancia.
        self.pir = Pin(19, Pin.IN)
        self.trig = Pin(5, Pin.OUT)
        self.echo = Pin(18, Pin.IN)
        
        # Inicialización del bus I2C del MPU6050 sin librerías externas.
        try:
            self.i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
            # El MPU6050 arranca dormido; escribir 0x00 en 0x6B lo habilita.
            self.i2c.writeto_mem(0x68, 0x6B, b'\x00')
            self.mpu_disponible = True
        except Exception as e:
            print("Error I2C MPU6050:", e)
            self.mpu_disponible = False

    def leer_movimiento(self):
        # La HAL entrega un estado simple para que MQTT no lea el pin directamente.
        return "SI" if self.pir.value() == 1 else "NO"

    def leer_distancia(self):
        # La HAL encapsula la secuencia trig/echo y devuelve una distancia lista para publicar.
        self.trig.off()
        time.sleep_us(2)
        self.trig.on()
        time.sleep_us(10)
        self.trig.off()
        duracion = time_pulse_us(self.echo, 1, 30000)  # Timeout de 30 ms.
        if duracion < 0:
            return -1.0  # Sin eco o fuera de rango.
        return (duracion / 2) / 29.1  # Conversión a centímetros.

    def leer_aceleracion(self):
        if not self.mpu_disponible:
            return 0.0
            
        try:
            # Lectura del bloque de aceleración y giroscopio desde la dirección 0x68.
            raw = self.i2c.readfrom_mem(0x68, 0x3B, 14)
            valores = struct.unpack('>7h', raw)
            # Se usa solo el eje Y como telemetría resumida del movimiento.
            ay = valores[1] / 16384.0
            return round(ay, 2)
        except Exception:
            return 0.0

class ActuatorBox:
    def __init__(self):
        # Salida física del motor vibrador controlada por transistor.
        self.vibrador = Pin(25, Pin.OUT)
        
        # Canales PWM del LED RGB en la escala nativa de MicroPython.
        self.led_r = PWM(Pin(13), freq=1000, duty=0)
        self.led_g = PWM(Pin(14), freq=1000, duty=0)
        self.led_b = PWM(Pin(33), freq=1000, duty=0)

    def activar_vibrador(self, estado):
        # La lógica MQTT solo decide el estado; la HAL ejecuta la acción física.
        self.vibrador.on() if estado else self.vibrador.off()

    def set_color_rgb(self, r, g, b):
        # Conversión de 0-255 a 0-1023 para el ciclo de trabajo PWM.
        self.led_r.duty(int((r / 255) * 1023))
        self.led_g.duty(int((g / 255) * 1023))
        self.led_b.duty(int((b / 255) * 1023))

    def estado_seguro(self):
        # Apaga salidas para dejar el sistema en un estado seguro.
        self.vibrador.off()
        self.set_color_rgb(0, 0, 0)
