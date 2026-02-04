import sqlite3

class LecturaModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_lecturas(self, filtros=None):
        """Obtiene lecturas de la base de datos con filtros opcionales."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM lecturas"
            params = []

            # Aplicar filtros
            if filtros:
                condiciones = []
                if "mes" in filtros:
                    condiciones.append("strftime('%m', fecha_lectura) = ?")
                    params.append(f"{int(filtros['mes']):02d}")
                if "año" in filtros:
                    condiciones.append("strftime('%Y', fecha_lectura) = ?")
                    params.append(filtros["año"])
                if "direccion" in filtros:
                    condiciones.append("direccion LIKE ?")
                    params.append(f"%{filtros['direccion']}%")
                if "nombre_cliente" in filtros:
                    condiciones.append("nombre_cliente LIKE ?")
                    params.append(f"%{filtros['nombre_cliente']}%")

                query += " WHERE " + " AND ".join(condiciones)

            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()

            return resultados
        except sqlite3.Error as e:
            print(f"Error al obtener lecturas: {e}")
            return []
