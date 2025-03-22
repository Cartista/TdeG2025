import RPi.GPIO as GPIO
from time import sleep

# Configuración de pines
CLK_PIN = 13  # Pin CLK del encoder
DT_PIN = 11   # Pin DT del encoder

# Variables globales
pulsos = 0
ultimo_estado_clk = GPIO.LOW

def setup_gpio():
    """Configura los pines GPIO y las interrupciones."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Configurar interrupción en el pin CLK con un bouncetime mayor
    GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=actualizar_pulsos, bouncetime=50)  # Aumentado a 50 ms

def actualizar_pulsos(channel):
    """Función de callback para actualizar los pulsos cuando se detecta un cambio en el pin CLK."""
    global pulsos, ultimo_estado_clk

    estado_clk = GPIO.input(CLK_PIN)
    estado_dt = GPIO.input(DT_PIN)

    if estado_clk != ultimo_estado_clk:  # Solo actuar en cambios de estado de CLK
        if estado_dt != estado_clk:
            pulsos += 1  # Giro en una dirección
        else:
            pulsos -= 1  # Giro en la otra dirección

        print(f"Pulsos totales: {pulsos}")  # Mostrar los pulsos actuales
        ultimo_estado_clk = estado_clk

def main():
    """Función principal para probar la lectura del encoder."""
    try:
        setup_gpio()
        while True:
            sleep(0.1)  # Esperar antes de la siguiente lectura

    except KeyboardInterrupt:
        print("Prueba del encoder KY-040 terminada.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
