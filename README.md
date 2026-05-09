# Integración Total MQTT (ESP32 ↔ Python)

Repositorio de entrega para la práctica de Sistemas Programables.

## Contenido de entrega
- `dispositivos.py`: Capa HAL para sensores y actuadores.
- `main.py`: Lógica MQTT en la ESP32.
- `servidor.py`: Servidor Python con telemetría y comandos.
- `conclusion_RG.md`: Conclusión y análisis individual.
- `lib/umqtt/simple.py`: Librería MQTT para MicroPython.

## Arquitectura de Red y Matriz de Tópicos MQTT

El sistema implementa un modelo de publicación/suscripción asincrónico sobre Wi-Fi. El ESP32 actúa como nodo periférico gestionando la capa física (sensores y actuadores) a través de una HAL. La aplicación móvil (MQTT Dash) y el script Python operan como clientes de interfaz y registro de telemetría.

| Componente / Interfaz | Tópico MQTT | Flujo de Datos (QoS 0) | Payload |
|--------|-----------|-----|---------|
| Sensores (PIR, Ultrasónico, MPU6050) | `vestaguard/telemetria/sensores` | ESP32 Publica → Python/App Suscriben | `{"pir":"NO","distancia_cm":154.3,"aceleracion_y":-0.02}` |
| Motor Vibrador | `vestaguard/control/vibrador` | App/Python Publican → ESP32 Suscribe | `ON` / `OFF` |
| LED RGB | `vestaguard/control/rgb` | App/Python Publican → ESP32 Suscribe | `ROJO` / `VERDE` / `APAGAR` |
| Módulo Relevador (Foco 110V) | `vestaguard/control/relevador` | App/Python Publican → ESP32 Suscribe | `ON` / `OFF` |

**Flujo resumido:** El ESP32 publica telemetría JSON cada 2 s hacia el broker Mosquitto. El servidor Python (servidor.py) se suscribe y muestra los datos con marca de tiempo. Los comandos de control viajan en dirección contraria: MQTT Dash o servidor.py publican en los tópicos de control y la ESP32 delega la acción física a la clase HAL (ActuatorBox).

## Resumen de lo que debe verificarse
- El código debe tener encabezado con objetivo, integrantes y proyecto.
- La ESP32 debe publicar telemetría y recibir comandos por MQTT.
- La lógica MQTT debe usar la HAL y no tocar hardware directamente.
- El servidor Python debe mostrar timestamps al recibir telemetría.
- La entrega debe incluir evidencia de funcionamiento real del hardware.

## Análisis individual

### Alvarez Guevara Estefania Guadalupe (23240077)
**Problema:** El ESP32 no se conectaba al broker MQTT porque el identificador único (ID) que enviaba contenía caracteres crudos que corrompían la trama de conexión. Adicionalmente, en la parte física, el motor de vibración no activaba por dos razones: insuficiencia de potencia en la alimentación desde el pin 3.3V, y el transistor 2N2222 estaba conectado en polaridad invertida (pines en orden incorrecto).

**Solución:** Para la capa de red, se importó ubinascii para convertir el ID sucio a formato hexadecimal legible que el servidor MQTT interpretara correctamente. Para la capa física, se reconfiguró la alimentación desde el pin VIN (5V) para proporcionar suficiente corriente al motor, y se corrigió la polaridad del transistor (base, colector, emisor) girándolo 180°. Para optimizar la experiencia de pruebas, se adoptó MQTT Dash en dispositivo móvil como interfaz de control, separando completamente el flujo de telemetría entrante del de comandos salientes.

**Conclusión personal:** La arquitectura de capas (HAL separada de lógica MQTT) fue fundamental para identificar rápidamente que los problemas de conectividad que parecían ser defectos de red eran en realidad problemas de voltaje e inversión de polaridad. Esta separación permitió realizar correcciones precisas sin afectar el código ya funcional, demostrando que en sistemas IoT integrados, la claridad arquitectónica es más importante que la velocidad inicial de implementación.

### Rangel Hernandez Aldo (23240272)
**Problema:** El cliente MQTT y algunos componentes físicos no respondían como se esperaba durante las primeras pruebas. El identificador de cliente con bytes crudos provocaba rechazos silenciosos en el broker Mosquitto y las conexiones físicas mal aseguradas generaban lecturas de sensores inconsistentes que confundían la lógica de control.

**Solución:** Se corrigió el identificador MQTT codificándolo a hexadecimal, se verificó la configuración de red (IP del broker, puerto 1883 y conexión a la misma WLAN) y se revisaron y aseguraron todas las conexiones físicas del protoboard que generaban falsos contactos e interferencias en las lecturas.

**Conclusión personal:** El uso de MQTT con una estructura de tópicos jerárquica y bien definida facilitó localizar errores de software (ID inválido, parámetros de conexión erróneos) y de hardware (falsos contactos) de forma independiente. La separación de responsabilidades entre la capa de red y la HAL redujo significativamente el tiempo total de depuración del sistema.

### Reyes Gutierrez Pablo Alberto (23240055)
**Problema:** Fallas críticas en múltiples capas: el cliente MQTT no podía conectarse porque el identificador único se enviaba como bytes crudos (corrupción de trama en umqtt.simple); la telemetría cada 2 segundos interrumpía comandos en la consola de VS Code, generando asincronía; el motor vibrador permanecía inactivo a pesar de que los mensajes MQTT llegaban correctamente al ESP32.

**Solución:** (1) Red: conversión del ID con ubinascii a hexadecimal legible. (2) Interacción: adopción de MQTT Dash en dispositivo móvil para aislar telemetría de comandos. (3) Hardware: diagnóstico diferencial reveló transistor 2N2222 invertido (180°) y alimentación insuficiente; se corrigió polaridad y se cambió fuente de 3.3V a pin VIN de 5V. Cada capa se validó de forma independiente.

**Conclusión personal:** La HAL permitió ejecutar pruebas de comunicación sin riesgo de daño físico, demostrando que un problema aparente de conectividad era realmente caída de voltaje y polaridad en el hardware. La depuración metódica por capas es esencial en sistemas IoT integrados; separar software de hardware permite corregir fallas sin comprometer el sistema completo.

## Evidencias de Funcionamiento

Las evidencias de funcionamiento del sistema (capturas de pantalla de telemetría en Thonny, logs en servidor.py con timestamps, MQTT Dash con comandos activos) se adjuntan en el documento PDF de entrega.

## Verificación del Repositorio GitHub

### Archivos requeridos en el repositorio
- `main.py` — Lógica MQTT de la ESP32; callback `enrutar_topico()` invoca explícitamente la HAL.
- `dispositivos.py` — Capa HAL (SensorBox / ActuatorBox); sin acceso directo al hardware desde la lógica de red.
- `servidor.py` — Servidor Python con timestamps y consola de comandos interactiva.
- Los tres archivos tienen el bloque docstring con OBJETIVO, INTEGRANTES y PROYECTO en la cabecera.
- El repositorio está configurado como público para evitar error 404 durante la revisión.

### Bloque de cabecera requerido (idéntico en los 3 archivos)
```python
"""
OBJETIVO: <Punto de entrada MQTT / HAL de Sensores / Servidor de recepción>
INTEGRANTES: Alvarez Guevara Estefania Guadalupe,
             Rangel Hernandez Aldo,
             Reyes Gutierrez Pablo Alberto
PROYECTO: VestaGuard
"""
```

### Comentarios críticos en main.py
El callback `enrutar_topico()` debe contener comentarios que señalen explícitamente donde ocurre la invocación a la HAL (actuadores.activar_vibrador() y actuadores.set_color_rgb()), validando el encapsulamiento exigido por la rúbrica.

## Nota final
Antes de subir a GitHub, asegúrate de incluir evidencia de funcionamiento real del hardware y el enlace al repositorio en la plataforma de entrega.
