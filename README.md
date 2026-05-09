# Integración Total MQTT (ESP32 ↔ Python)

Repositorio de entrega para la práctica de Sistemas Programables.

## Contenido de entrega
- `dispositivos.py`: Capa HAL para sensores y actuadores.
- `main.py`: Lógica MQTT en la ESP32.
- `servidor.py`: Servidor Python con telemetría y comandos.
- `conclusion_RG.md`: Conclusión y análisis individual.
- `lib/umqtt/simple.py`: Librería MQTT para MicroPython.

## Matriz de tópicos

| Tópico | Dirección | Uso |
|--------|-----------|-----|
| `vestaguard/telemetria/sensores` | ESP32 → Python | Publicación de sensores en JSON |
| `vestaguard/control/vibrador` | Python/App → ESP32 | Encendido y apagado del vibrador |
| `vestaguard/control/rgb` | Python/App → ESP32 | Control de color del LED RGB |

## Resumen de lo que debe verificarse
- El código debe tener encabezado con objetivo, integrantes y proyecto.
- La ESP32 debe publicar telemetría y recibir comandos por MQTT.
- La lógica MQTT debe usar la HAL y no tocar hardware directamente.
- El servidor Python debe mostrar timestamps al recibir telemetría.
- La entrega debe incluir evidencia de funcionamiento real del hardware.

## Análisis individual

### Alvarez Guevara Estefania Guadalupe
**Problema:** Se presentó inestabilidad al integrar la comunicación MQTT con el hardware físico.

**Solución:** Se separó la lógica por capas, corrigiendo primero la red, después la HAL y por último el cableado del sistema.

**Conclusión:** La depuración por partes permitió validar que el sistema podía comunicarse sin afectar directamente los actuadores.

### Rangel Hernandez Aldo
**Problema:** El cliente MQTT y algunos componentes físicos no respondían como se esperaba durante las primeras pruebas.

**Solución:** Se corrigieron el identificador MQTT, la configuración de red y las conexiones físicas que generaban falsos contactos.

**Conclusión:** El uso de MQTT con una estructura bien organizada ayudó a localizar errores de software y hardware de manera más rápida.

### Reyes Gutierrez Pablo Alberto
**Problema:** La telemetría y el control no se comportaban de forma estable al probar el motor vibrador y el LED RGB.

**Solución:** Se verificaron la alimentación, el transistor, los pines y la publicación de mensajes en los tópicos correctos.

**Conclusión:** Separar la HAL de la lógica MQTT hizo posible corregir fallas sin comprometer el funcionamiento general del proyecto.
