import angle_irl as ag

class AngleCalculator:
    def __init__(self, latitud, longitud, altitud, zona_horaria):
        """
        Inicializa el calculador de ángulos solares.
        
        :param latitud: Latitud de la ubicación.
        :param longitud: Longitud de la ubicación.
        :param altitud: Altitud de la ubicación.
        :param zona_horaria: Zona horaria para cálculos solares.
        """
        self.latitud = latitud
        self.longitud = longitud
        self.altitud = altitud
        self.zona_horaria = zona_horaria

    def calculate_angles(self):
        """
        Calcula los ángulos de elevación y azimuth del sol.
        
        :return: Tupla con los ángulos de elevación y azimuth.
        """
        return ag.angle_irl(self.latitud, self.longitud, self.zona_horaria, self.altitud)