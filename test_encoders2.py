#Codigo para probar el funcionamiento de los encoders del sistema
#Hecho por: Carlos Bautista, 2171513
import RPi.GPIO as GPIO
from time import sleep

# Configuración de pines para el encoder de elevación
CLK_ELEVACION_PIN = 13  # Pin CLK del encoder de elevación
DT_ELEVACION_PIN = 11   # Pin DT del encoder de elevación

# Configuración de pines para el encoder de azimuth
CLK_AZIMUTH_PIN = 33  # Pin CLK del encoder de azimuth
DT_AZIMUTH_PIN = 35   # Pin DT del encoder de azimuth

# Variables globales para los pulsos de cada encoder
pulsos_elevacion = 0
pulsos_azimuth = 0

# Variables globales para el último estado de CLK de cada encoder
ultimo_estado_clk_elevacion = GPIO.LOW
ultimo_estado_clk_azimuth = GPIO.LOW

def setup_gpio():
    """Configura los pines GPIO y las interrupciones para ambos encoders."""
    GPIO.setmode(GPIO.BOARD)
    
    # Configuración del encoder de elevación
    GPIO.setup(CLK_ELEVACION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_ELEVACION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(CLK_ELEVACION_PIN, GPIO.BOTH, callback=actualizar_pulsos_elevacion, bouncetime=50)
    
    # Configuración del encoder de azimuth
    GPIO.setup(CLK_AZIMUTH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_AZIMUTH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(CLK_AZIMUTH_PIN, GPIO.BOTH, callback=actualizar_pulsos_azimuth, bouncetime=50)

def actualizar_pulsos_elevacion(channel):
    """Función de callback para actualizar los pulsos del encoder de elevación."""
    global pulsos_elevacion, ultimo_estado_clk_elevacion

    estado_clk = GPIO.input(CLK_ELEVACION_PIN)
    estado_dt = GPIO.input(DT_ELEVACION_PIN)

    if estado_clk != ultimo_estado_clk_elevacion:
        if estado_dt != estado_clk:
            pulsos_elevacion += 1  # Giro en sentido horario
            direccion = "Adelante"
        else:
            pulsos_elevacion -= 1  # Giro en sentido antihorario
            direccion = "Atrás"

        print(f"Elevación: Pulsos = {pulsos_elevacion}, Dirección = {direccion}")
        ultimo_estado_clk_elevacion = estado_clk

def actualizar_pulsos_azimuth(channel):
    """Función de callback para actualizar los pulsos del encoder de azimuth."""
    global pulsos_azimuth, ultimo_estado_clk_azimuth

    estado_clk = GPIO.input(CLK_AZIMUTH_PIN)
    estado_dt = GPIO.input(DT_AZIMUTH_PIN)

    if estado_clk != ultimo_estado_clk_azimuth:
        if estado_dt != estado_clk:
            pulsos_azimuth += 1  # Giro en sentido horario
            direccion = "horario"
        else:
            pulsos_azimuth -= 1  # Giro en sentido antihorario
            direccion = "antihorario"

        print(f"Azimuth: Pulsos = {pulsos_azimuth}, Dirección = {direccion}")
        ultimo_estado_clk_azimuth = estado_clk

def main():
    """Función principal para probar la lectura de ambos encoders."""
    try:
        setup_gpio()
        while True:
            sleep(0.1)  # Esperar antes de la siguiente lectura

    except KeyboardInterrupt:
        print("Prueba de los encoders KY-040 terminada.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()