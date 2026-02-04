from app.models.lectura import Lectura

class LecturaController:
    def __init__(self, db_path):
        self.db_path = db_path

    def guardar_lectura(self, medidor_id, lectura_anterior, lectura_actual, consumo, usuario_id, fecha_lectura, direccion, nombre_cliente):
        try:
            lectura = Lectura(
                medidor_id=medidor_id,
                lectura_anterior=lectura_anterior,
                lectura_actual=lectura_actual,
                consumo=consumo,
                usuario_id=usuario_id,
                fecha_lectura=fecha_lectura,
                direccion=direccion,
                nombre_cliente=nombre_cliente
            )
            Lectura.guardar_lectura(self.db_path, lectura)
            return True
        except Exception as e:
            print(f"Error al guardar la lectura: {e}")
            return False


    def obtener_lecturas(self, medidor_id=None):
        """Obtiene todas las lecturas o las de un cliente específico."""
        return Lectura.obtener_lecturas(self.db_path, medidor_id)

    def obtener_cliente_y_direccion(self, medidor_id):
        """Obtiene el nombre y dirección de un cliente por su ID."""
        return Lectura.obtener_cliente_y_direccion(self.db_path, medidor_id)

    def obtener_ultima_lectura(self, medidor_id):
        """Obtiene la última lectura registrada de un cliente por su ID."""
        return Lectura.obtener_ultima_lectura(self.db_path, medidor_id)

#revisar cambios en esta seccion