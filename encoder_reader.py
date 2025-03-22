import RPi.GPIO as GPIO
from time import sleep

class EncoderReader:
    def __init__(self, clk_pin, dt_pin, ppr=100):
        """
        Inicializa el lector de encoder KY-040.
        
        :param clk_pin: Pin GPIO conectado a la señal CLK del KY-040.
        :param dt_pin: Pin GPIO conectado a la señal DT del KY-040.
        :param ppr: Pulsos por revolución del encoder (por defecto 100 para elevación, 20 para azimuth).
        """
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        self.ppr = ppr
        self.pulsos = 0  # Contador de pulsos
        self.ultimo_estado_clk = GPIO.LOW  # Último estado de la señal CLK
        self.setup_gpio()

    def setup_gpio(self):
        """
        Configura los pines GPIO para el encoder KY-040.
        """
        GPIO.setmode(GPIO.BOARD)  # Usar numeración física de pines
        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configurar CLK como entrada con pull-up
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Configurar DT como entrada con pull-up
        # Detectar cambios en la señal CLK (flanco de subida y bajada) con debounce
        GPIO.add_event_detect(self.clk_pin, GPIO.BOTH, callback=self.actualizar_pulsos, bouncetime=50)

    def actualizar_pulsos(self, channel):
        """
        Función de callback que se ejecuta cuando cambia el estado de la señal CLK.
        Actualiza el contador de pulsos basado en la dirección de rotación.
        
        :param channel: Pin GPIO que generó la interrupción (no se usa en este caso).
        """
        estado_clk = GPIO.input(self.clk_pin)  # Leer estado actual de la señal CLK
        estado_dt = GPIO.input(self.dt_pin)    # Leer estado actual de la señal DT

        if estado_clk != self.ultimo_estado_clk:  # Si hubo un cambio en la señal CLK
            if estado_dt != estado_clk:
                self.pulsos += 1  # Sentido horario
            else:
                self.pulsos -= 1  # Sentido antihorario

        self.ultimo_estado_clk = estado_clk  # Actualizar el último estado de la señal CLK

    def get_pulsos(self):
        """
        Devuelve el número total de pulsos contados.
        
        :return: Número de pulsos.
        """
        return self.pulsos

    def get_posicion_angular(self):
        """
        Calcula la posición angular en grados basada en los pulsos contados.
        
        :return: Posición angular en grados (0° a 360°).
        """
        return (self.pulsos % self.ppr) * (360 / self.ppr)

    def reset_pulsos(self):
        """
        Reinicia el contador de pulsos a cero.
        """
        self.pulsos = 0