class ObtenerCedula:
    def __init__(self):
        """Simula una base de datos de clientes con sus cédulas."""
        self.base_de_datos = {
            "Juan Pérez": "1723456789",
            "María Gómez": "1809876543",
            "Carlos López": "1501234567",
            "Ana Torres": "1105678934",
            "Luis Sánchez": "1408765432"
        }

    def buscar_cedula(self, nombre_cliente):
        """
        Recupera la cédula del cliente basado en su nombre.
        Si el cliente no está registrado, devuelve 'Sin cédula'.
        """
        return self.base_de_datos.get(nombre_cliente, "Sin cédula")
