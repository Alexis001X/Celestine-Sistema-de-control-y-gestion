import sqlite3

class RecuperarFacturaID:
    def __init__(self, db_path):
        """
        Inicializa el componente con la ruta de la base de datos.
        :param db_path: Ruta al archivo SQLite de la base de datos.
        """
        self.db_path = db_path

    def obtener_id_factura(self, factura_id=None):
        """
        Recupera el ID de la factura.
        Si no se proporciona factura_id, devuelve el ID más reciente.
        :param factura_id: ID específico de la factura (opcional).
        :return: El ID de la factura (int) o None si no se encuentra.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if factura_id:
                # Buscar una factura específica por su ID
                query = "SELECT id FROM facturas WHERE id = ?"
                cursor.execute(query, (factura_id,))
            else:
                # Obtener el ID más reciente de la factura
                query = "SELECT id FROM facturas ORDER BY id DESC LIMIT 1"
                cursor.execute(query)

            resultado = cursor.fetchone()
            conn.close()

            return resultado[0] if resultado else None

        except sqlite3.Error as e:
            print(f"Error al recuperar el ID de la factura: {e}")
            return None
