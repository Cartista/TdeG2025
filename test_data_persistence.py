from data_persistence import DataPersistence

def main():
    """
    Función principal para probar la persistencia de datos.
    """
    # Guardar valores de prueba
    DataPersistence.save_potentiometers(10, 20)
    print("Valores guardados: 10, 20")

    # Cargar valores guardados
    pulsos1, pulsos2 = DataPersistence.load_potentiometers()
    print(f"Valores cargados: {pulsos1}, {pulsos2}")

if __name__ == "__main__":
    main()