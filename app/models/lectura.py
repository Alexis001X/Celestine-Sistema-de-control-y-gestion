import sqlite3
from datetime import datetime

class Lectura:
    def __init__(self, medidor_id, lectura_anterior, lectura_actual, consumo, usuario_id, fecha_lectura, direccion, nombre_cliente):
        self.medidor_id = medidor_id
        self.lectura_anterior = lectura_anterior
        self.lectura_actual = lectura_actual
        self.consumo = consumo  # Valor calculado que se pasa como argumento
        self.fecha_lectura = fecha_lectura  # Se recibe como argumento, ya no se calcula internamente
        self.usuario_id = usuario_id
        self.direccion = direccion
        self.nombre_cliente = nombre_cliente

    def calcular_consumo(self):
        """Método de cálculo en caso de que necesites recalcular en otro momento."""
        return self.lectura_actual - self.lectura_anterior

    @staticmethod
    def guardar_lectura(db_path, lectura):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            query = """
                INSERT INTO lecturas (medidor_id, lectura_anterior, lectura_actual, consumo, fecha_lectura, usuario_id, direccion, nombre_cliente)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                lectura.medidor_id, lectura.lectura_anterior, lectura.lectura_actual,
                lectura.consumo, lectura.fecha_lectura, lectura.usuario_id,
                lectura.direccion, lectura.nombre_cliente
            ))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al guardar la lectura: {e}")
            return False
        finally:
            conn.close()


    @staticmethod
    def obtener_lecturas(db_path, medidor_id=None):
        """Obtiene todas las lecturas o las de un cliente específico."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        if medidor_id:
            cursor.execute("SELECT * FROM lecturas WHERE medidor_id = ?", (medidor_id,))
        else:
            cursor.execute("SELECT * FROM lecturas")
        lecturas = cursor.fetchall()
        conn.close()
        return lecturas

    @staticmethod
    def obtener_cliente_y_direccion(db_path, medidor_id):
        """Obtiene el nombre y la dirección del cliente mediante su ID."""
        query = """
            SELECT nombre_cliente, direccion 
            FROM clientes 
            WHERE id = ?
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query, (medidor_id,))
            cliente = cursor.fetchone()
            conn.close()
            if cliente:
                return {"nombre_cliente": cliente[0], "direccion": cliente[1]}
            return None
        except sqlite3.Error as e:
            print(f"Error al recuperar cliente: {e}")
            return None

    @staticmethod
    def obtener_ultima_lectura(db_path, medidor_id):
        """Obtiene la última lectura registrada para un cliente específico."""
        query = """
            SELECT lectura_actual 
            FROM lecturas 
            WHERE medidor_id = ? 
            ORDER BY fecha_lectura DESC 
            LIMIT 1
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query, (medidor_id,))
            ultima_lectura = cursor.fetchone()
            conn.close()
            if ultima_lectura:
                return ultima_lectura[0]
            return None
        except sqlite3.Error as e:
            print(f"Error al recuperar la última lectura: {e}")
            return None
#revisar cambios en esta seccion