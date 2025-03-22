class DataPersistence:
    @staticmethod
    def save_potentiometers(pulsos1, pulsos2, filename="Potenciometros.txt"):
        """
        Guarda los valores de los encoders en un archivo.
        
        :param pulsos1: Pulsos del encoder 1.
        :param pulsos2: Pulsos del encoder 2.
        :param filename: Nombre del archivo donde se guardarán los datos.
        """
        with open(filename, "w") as file:
            file.write(f"{pulsos1},{pulsos2}")

    @staticmethod
    def load_potentiometers(filename="Potenciometros.txt"):
        """
        Carga los valores de los encoders desde un archivo.
        
        :param filename: Nombre del archivo desde donde se cargarán los datos.
        :return: Tupla con los pulsos de los encoders (encoder1, encoder2).
        """
        try:
            with open(filename, "r") as file:
                line = file.readline()
                pulsos1, pulsos2 = map(int, line.strip().split(","))
                return pulsos1, pulsos2
        except FileNotFoundError:
            return 0, 0  # Valores por defecto si el archivo no existe