import sqlite3

class RecuperarLecturas:
    def __init__(self, db_path):
        self.db_path = db_path

    def recuperar_lecturas_por_medidor(self, medidor_id):
        """
        Recupera los campos consumo_anterior y consumo_actual de la tabla lecturas para un cliente específico.
        
        :param medidor_id: ID del medidor del cliente.
        :return: Un diccionario con los valores de consumo_anterior y consumo_actual o None si no se encuentra.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT lectura_anterior, lectura_actual
                FROM lecturas
                WHERE medidor_id = ?
                ORDER BY fecha_lectura DESC
                LIMIT 1
            """
            cursor.execute(query, (medidor_id,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return {
                    "lectura_anterior": resultado[0],
                    "lectura_actual": resultado[1],
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al recuperar lecturas: {e}")
            return None
