import RPi.GPIO as GPIO
from time import sleep

class MotorController:
    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin, ena_pin, enb_pin):
        """
        Inicializa el controlador de motores L298N con PWM.
        
        :param in1_pin: Pin GPIO para IN1 del L298N.
        :param in2_pin: Pin GPIO para IN2 del L298N.
        :param in3_pin: Pin GPIO para IN3 del L298N.
        :param in4_pin: Pin GPIO para IN4 del L298N.
        :param ena_pin: Pin GPIO para ENA del L298N (PWM para motor de elevación).
        :param enb_pin: Pin GPIO para ENB del L298N (PWM para motor de azimut).
        """
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.in3_pin = in3_pin
        self.in4_pin = in4_pin
        self.ena_pin = ena_pin
        self.enb_pin = enb_pin
        self.setup_gpio()

    def setup_gpio(self):
        """
        Configura los pines GPIO para controlar el L298N con PWM.
        """
        GPIO.setmode(GPIO.BOARD)  # Usar numeración física de pines
        GPIO.setup(self.in1_pin, GPIO.OUT)  # Configurar IN1 como salida
        GPIO.setup(self.in2_pin, GPIO.OUT)  # Configurar IN2 como salida
        GPIO.setup(self.in3_pin, GPIO.OUT)  # Configurar IN3 como salida
        GPIO.setup(self.in4_pin, GPIO.OUT)  # Configurar IN4 como salida
        GPIO.setup(self.ena_pin, GPIO.OUT)  # Configurar ENA como salida (PWM)
        GPIO.setup(self.enb_pin, GPIO.OUT)  # Configurar ENB como salida (PWM)

        # Inicializar PWM en los pines ENA y ENB
        self.pwm_ena = GPIO.PWM(self.ena_pin, 1000)  # Frecuencia de 1000 Hz
        self.pwm_enb = GPIO.PWM(self.enb_pin, 1000)  # Frecuencia de 1000 Hz
        self.pwm_ena.start(0)  # Iniciar PWM con duty cycle 0 (motores detenidos)
        self.pwm_enb.start(0)

    def mover_elevacion_arriba(self):
        """Mueve el motor de elevación hacia arriba."""
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def mover_elevacion_abajo(self):
        """Mueve el motor de elevación hacia abajo."""
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def mover_azimut_izquierda(self):
        """Mueve el motor de azimut hacia la izquierda."""
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.LOW)

    def mover_azimut_derecha(self):
        """Mueve el motor de azimut hacia la derecha."""
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.HIGH)

    def detener_motores(self):
        """Detiene todos los motores."""
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.LOW)
        self.pwm_ena.ChangeDutyCycle(0)  # Detener PWM
        self.pwm_enb.ChangeDutyCycle(0)

    def inicio_suave(self, pwm, duracion=2):
        """
        Realiza un inicio suave del motor aumentando gradualmente el duty cycle del PWM.
        
        :param pwm: Objeto PWM (pwm_ena o pwm_enb).
        :param duracion: Duración del inicio suave en segundos.
        """
        for dc in range(0, 101, 5):  # Aumenta el duty cycle de 0% a 100% en pasos de 5%
            pwm.ChangeDutyCycle(dc)
            sleep(duracion / 20)