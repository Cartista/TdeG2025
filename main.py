# Programa principal para comparar los encoders del panel y el valor teórico y accionar los motores
# Creado por: Carlos Bautista, 2171513
import RPi.GPIO as GPIO
from time import sleep
import threading
from encoder_reader import EncoderReader
from angle_calculator import AngleCalculator
from motor_controller import MotorController
from data_persistence import DataPersistence

def main():
    """
    Función principal del programa.
    """
    # Configuración inicial de GPIO
    GPIO.setmode(GPIO.BOARD)  # Usar numeración física de pines
    GPIO.setwarnings(False)  # Desactivar advertencias de GPIO

    # Definir coordenadas manualmente (latitud, longitud, altitud)
    latitud = 7.1420939356621105  # Latitud de la ubicación (ejemplo: Bucaramanga, Colombia)
    longitud = -73.12132294503459  # Longitud de la ubicación
    altitud = 967  # Altitud en metros sobre el nivel del mar

    zona_horaria = 'Etc/GMT+5'  # Zona horaria para cálculos solares
    print(f"Coordenadas manuales: Latitud={latitud}, Longitud={longitud}, Altitud={altitud}")

    # Inicialización de módulos
    # Encoder de Elevación: CLK=13, DT=11
    encoder_elevacion = EncoderReader(clk_pin=13, dt_pin=11)
    
    # Encoder de Azimut: CLK=33, DT=35
    encoder_azimut = EncoderReader(clk_pin=33, dt_pin=35)
    
    # Cálculo de ángulos solares
    angle_calculator = AngleCalculator(latitud, longitud, altitud, zona_horaria)
    
    # Control de motores L298N con PWM
    motor_controller = MotorController(in1_pin=29, in2_pin=31, in3_pin=38, in4_pin=40, ena_pin=36, enb_pin=32)
    
    # Guardado y lectura de datos
    data_persistence = DataPersistence()

    # Cargar valores iniciales de los encoders desde archivo
    pulsos_elevacion, pulsos_azimut = data_persistence.load_potentiometers()
    encoder_elevacion.pulsos = pulsos_elevacion
    encoder_azimut.pulsos = pulsos_azimut

    # Función para mover el motor de azimut a la posición 0 con inicio suave
    def mover_azimut_a_cero():
        while encoder_azimut.get_pulsos() != 0:
            if encoder_azimut.get_pulsos() > 0:
                motor_controller.mover_azimut_izquierda()  # Mover en sentido antihorario
            else:
                motor_controller.mover_azimut_derecha()    # Mover en sentido horario
            motor_controller.inicio_suave(motor_controller.pwm_enb)  # Inicio suave
            sleep(0.1)
        motor_controller.detener_motores()  # Detener el motor

    # Función para mover el motor de elevación a la posición 0 con inicio suave
    def mover_elevacion_a_cero():
        while encoder_elevacion.get_pulsos() != 0:
            if encoder_elevacion.get_pulsos() > 0:
                motor_controller.mover_elevacion_abajo()  # Mover hacia abajo
            else:
                motor_controller.mover_elevacion_arriba() # Mover hacia arriba
            motor_controller.inicio_suave(motor_controller.pwm_ena)  # Inicio suave
            sleep(0.1)
        motor_controller.detener_motores()  # Detener el motor

    try:
        while True:
            # Calcular ángulos de elevación y azimuth del sol
            elevacion_deseada, azimut_deseado = angle_calculator.calculate_angles()

            # Convertir ángulos a pasos
            # Elevación: cada paso corresponde a 9° (0° a 36° en 4 pasos)
            paso_elevacion_deseado = int(elevacion_deseada / 9)
            if paso_elevacion_deseado > 4:  # Limitar a 36° (paso 4)
                paso_elevacion_deseado = 4

            # Azimut: cada paso corresponde a 9° (0° a 360° en 40 pasos)
            paso_azimut_deseado = int(azimut_deseado / 9)
            if paso_azimut_deseado > 39:  # Limitar a 351° (paso 39)
                paso_azimut_deseado = 39

            # Obtener posición angular actual de los encoders
            elevacion_actual = encoder_elevacion.get_pulsos()  # Paso actual de elevación
            azimut_actual = encoder_azimut.get_pulsos()        # Paso actual de azimut

            # Mostrar valores en consola
            print(f"Elevación: {elevacion_actual} pulsos, Azimut: {azimut_actual}°, Deseado: Elevación={paso_elevacion_deseado}, Azimut={paso_azimut_deseado}")

            # Verificar si el encoder de azimut está fuera de los límites (0 a 40)
            if azimut_actual > 40 or azimut_actual < 0:
                print("Azimut fuera de rango. Moviendo a posición 0...")
                mover_azimut_a_cero()

            # Verificar si el encoder de elevación está fuera de los límites (0 a 4)
            if elevacion_actual > 4 or elevacion_actual < 0:
                print("Elevación fuera de rango. Moviendo a posición 0...")
                mover_elevacion_a_cero()

            # Controlar motores basado en los valores de los encoders y ángulos solares
            motor_controller.control_motors(elevacion_actual, azimut_actual, paso_elevacion_deseado, paso_azimut_deseado)

            # Guardar valores de los encoders en archivo
            data_persistence.save_potentiometers(elevacion_actual, azimut_actual)

            # Esperar antes de la siguiente iteración
            sleep(0.1)
    except KeyboardInterrupt:
        print("Programa terminado.")
        motor_controller.detener_motores()
        GPIO.cleanup()  # Limpiar configuración de GPIO al salir

if __name__ == "__main__":
    main()