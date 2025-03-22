import RPi.GPIO as GPIO
from time import sleep

# Pines del L298N
IN1 = 29  # Elevación - Dirección 1
IN2 = 31  # Elevación - Dirección 2
IN3 = 38  # Azimut - Dirección 1
IN4 = 40  # Azimut - Dirección 2
ENA = 36  # Enable Motor A (Elevación)
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
    """Detiene todos los motores y reinicia los pines de dirección."""
    pwm_ENA.ChangeDutyCycle(0)  # Detener motor de Elevación
    pwm_ENB.ChangeDutyCycle(0)  # Detener motor de Azimut
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)  # Reiniciar pines de dirección
    sleep(2)  # Pausa de 2 segundos entre cambios

def mover_motor_elevacion(direccion, duracion=5):
    """Mueve el motor de elevación en la dirección especificada."""
    if direccion == "arriba":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif direccion == "abajo":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    suave_inicio(pwm_ENA)  # Inicio suave
    sleep(duracion)  # Mantener el movimiento durante la duración especificada
    detener_motores()  # Detener el motor

def mover_motor_azimut(direccion, duracion=5):
    """Mueve el motor de azimut en la dirección especificada."""
    if direccion == "izquierda":
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif direccion == "derecha":
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    
    suave_inicio(pwm_ENB)  # Inicio suave
    sleep(duracion)  # Mantener el movimiento durante la duración especificada
    detener_motores()  # Detener el motor

try:
    while True:
        # Control del motor de Elevación
        print("Motor Elevación - Moviendo hacia arriba")
        mover_motor_elevacion("arriba", 5)
        
        print("Motor Elevación - Moviendo hacia abajo")
        mover_motor_elevacion("abajo", 5)
        
        # Control del motor de Azimut
        print("Motor Azimut - Moviendo hacia la izquierda")
        mover_motor_azimut("izquierda", 5)
        
        print("Motor Azimut - Moviendo hacia la derecha")
        mover_motor_azimut("derecha", 5)

except KeyboardInterrupt:
    print("Prueba finalizada")
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup()