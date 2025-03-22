import RPi.GPIO as GPIO
from time import sleep

# Pines del L298N
IN1 = 29  # Elevacion - Dirección 1
IN2 = 31  # Elevacion - Dirección 2
IN3 = 38  # Azimut - Dirección 1
IN4 = 40  # Azimut - Dirección 2
ENA = 36  # Enable Motor A (Elevacion)
ENB = 32  # Enable Motor B (Azimut)

# Frecuencia PWM (Hz)
PWM_FREQ = 1000

# Configuración de GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

# Configuración de PWM para los pines Enable
pwm_ENA = GPIO.PWM(ENA, PWM_FREQ)  # PWM para el motor de Elevación
pwm_ENB = GPIO.PWM(ENB, PWM_FREQ)  # PWM para el motor de Azimut

# Iniciar PWM con duty cycle 0 (motores detenidos)
pwm_ENA.start(0)
pwm_ENB.start(0)

def suave_inicio(pwm, duracion=2):
    """Función para un inicio suave del motor."""
    for dc in range(0, 101, 5):  # Aumenta el duty cycle de 0% a 100% en pasos de 5%
        pwm.ChangeDutyCycle(dc)
        sleep(duracion / 20)

def detener_motores():
    """Detiene todos los motores."""
    pwm_ENA.ChangeDutyCycle(0)  # Detener motor de Elevación
    pwm_ENB.ChangeDutyCycle(0)  # Detener motor de Azimut
    sleep(2)  # Pausa de 2 segundos entre cambios

try:
    while True:
        # Control del motor de Azimut
        print("Motor Azimut - Giro hacia arriba")
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        suave_inicio(pwm_ENB)  # Control suave del motor de Azimut
        sleep(10000)
        detener_motores()



except KeyboardInterrupt:
    print("Prueba finalizada")
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup()
 
