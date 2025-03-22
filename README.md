# Sistema de Seguimiento Solar Automatizado con Raspberry Pi

Este proyecto implementa un sistema de seguimiento solar automatizado utilizando una Raspberry Pi, un **sensor LM393 de herradura** (para la elevación), un **encoder KY-040** (para el azimut), y un **driver L298N** para controlar los motores. El sistema calcula la posición del sol en tiempo real y ajusta los motores para alinear un panel solar hacia la dirección óptima.

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Requisitos](#requisitos)
3. [Conexiones](#conexiones)
4. [Uso](#uso)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Licencia](#licencia)
7. [Contacto](#contacto)

---

## Descripción del Proyecto

El objetivo de este proyecto es maximizar la eficiencia de un panel solar mediante un sistema de seguimiento automatizado. Utiliza una Raspberry Pi para:

1. **Obtener la ubicación geográfica** manualmente.
2. **Calcular los ángulos de elevación y azimuth** del sol en tiempo real.
3. **Leer encoders** para determinar la posición actual del panel solar.
4. **Controlar motores** mediante un driver L298N para ajustar la posición del panel solar.

---

## Instalación dependencias 

```
pip install -r requirements.txt
```
---

## Requisitos

### Hardware
- **Raspberry Pi** (cualquier modelo con GPIO).
- **Sensor LM393 de herradura** (para la elevación).
- **Encoder KY-040** (para el azimut).
- **Driver L298N** (para controlar los motores).
- **Motores DC** (2 unidades, uno para elevación y otro para azimut).
- **Fuente de alimentación** (para los motores).
- **Cables y conectores** (jumpers, cables dupont, etc.).

### Software
- **Python 3.x**.
- **Librerías** listadas en `requirements.txt`.

---

## Conexiones

### Sensor LM393 (Elevación)

| Pin del LM393 | Pin de la Raspberry Pi | Descripción                     |
|---------------|------------------------|---------------------------------|
| VCC           | 3.3V o 5V             | Alimentación del sensor.        |
| GND           | GND                   | Tierra del sensor.              |
| DO (Digital)  | GPIO17 (Pin 11)       | Señal de pulsos (eje A).        |

### Encoder KY-040 (Azimut)

| Pin del KY-040 | Pin de la Raspberry Pi | Descripción                     |
|----------------|------------------------|---------------------------------|
| VCC            | 3.3V o 5V             | Alimentación del encoder.       |
| GND            | GND                   | Tierra del encoder.             |
| CLK            | GPIO13 (Pin 33)       | Señal de pulsos (eje A).        |
| DT             | GPIO19 (Pin 35)       | Señal de dirección (eje B).     |
| SW             | No conectado          | Botón (no se usa en este caso). |

### Driver L298N

| Pin del L298N | Pin de la Raspberry Pi | Descripción                     |
|---------------|------------------------|---------------------------------|
| IN1           | GPIO29 (Pin 40)        | Control del motor 1 (elevación).|
| IN2           | GPIO31 (Pin 41)        | Control del motor 1 (elevación).|
| IN3           | GPIO35 (Pin 38)        | Control del motor 2 (azimut).   |
| IN4           | GPIO33 (Pin 36)        | Control del motor 2 (azimut).   |
| ENA           | No conectado           | Habilitación del motor 1 (opcional, PWM). |
| ENB           | No conectado           | Habilitación del motor 2 (opcional, PWM). |
| VCC           | 5V o fuente externa    | Alimentación del L298N.         |
| GND           | GND                   | Tierra del L298N.               |
| OUT1          | Motor 1 (Elevación)    | Conexión al motor de elevación. |
| OUT2          | Motor 1 (Elevación)    | Conexión al motor de elevación. |
| OUT3          | Motor 2 (Azimut)       | Conexión al motor de azimut.    |
| OUT4          | Motor 2 (Azimut)       | Conexión al motor de azimut.    |

### Motores

| Motor          | Conexión en L298N | Descripción                     |
|----------------|-------------------|---------------------------------|
| Motor 1        | OUT1 y OUT2       | Motor de elevación.             |
| Motor 2        | OUT3 y OUT4       | Motor de azimut.                |

### Fuente de Alimentación

| Fuente         | Conexión            | Descripción                     |
|----------------|---------------------|---------------------------------|
| Positivo (+)   | VCC del L298N       | Alimentación de los motores.    |
| Negativo (-)   | GND del L298N       | Tierra de los motores.          |

---

## Uso

1. **Iniciar el sistema**: Ejecuta `main.py` para iniciar el sistema.
2. **Monitorear la salida**: El programa imprimirá en consola los valores de los encoders, los ángulos calculados y el estado de los motores.
3. **Guardado automático**: Los valores de los encoders se guardan automáticamente en `Potenciometros.txt`.
4. **Control manual**: Si es necesario, puedes ajustar manualmente los valores de los encoders en el archivo `Potenciometros.txt`.

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

## Contacto

- **Nombre**: [Carlos Bautista]
- **Email**: [carlosbautista.info@gmail.com]

---

¡Gracias por visitar este proyecto! Esperamos que sea útil para tu trabajo. 🚀
