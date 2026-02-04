import sqlite3
from datetime import datetime

class ServiciosController:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_datos_cliente(self, medidor_id):
        """Obtiene los datos del cliente a partir del número de medidor."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, nombre_cliente, direccion, cliente_ci, telefono, email, numero_conexion
                FROM clientes 
                WHERE numero_conexion = ?
            """
            cursor.execute(query, (medidor_id,))
            resultado = cursor.fetchone()
            
            conn.close()
            
            if resultado:
                return {
                    "id": resultado[0],
                    "nombre_cliente": resultado[1],
                    "direccion": resultado[2],
                    "cliente_ci": resultado[3],
                    "telefono": resultado[4],
                    "email": resultado[5],
                    "numero_conexion": resultado[6]
                }
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Error al obtener datos del cliente: {e}")
            return None

    def registrar_servicio(self, datos_servicio):
        """Registra un nuevo servicio en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                INSERT INTO servicios (
                    numero_medidor, nombre_usuario, direccion_usuario, 
                    usuario_servicio, monto_servicio, pago_uno, pago_dos, 
                    pago_tres, pago_cuatro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Asegurarse de que los valores de pago sean números válidos
            pago_uno = float(datos_servicio.get("pago_uno", 0) or 0)
            pago_dos = float(datos_servicio.get("pago_dos", 0) or 0)
            pago_tres = float(datos_servicio.get("pago_tres", 0) or 0)
            pago_cuatro = float(datos_servicio.get("pago_cuatro", 0) or 0)
            
            cursor.execute(query, (
                datos_servicio["numero_medidor"],
                datos_servicio["nombre_usuario"],
                datos_servicio["direccion_usuario"],
                datos_servicio["usuario_servicio"],
                datos_servicio["monto_servicio"],
                pago_uno,
                pago_dos,
                pago_tres,
                pago_cuatro
            ))
            
            conn.commit()
            id_servicio = cursor.lastrowid
            conn.close()
            
            return id_servicio
            
        except sqlite3.Error as e:
            print(f"Error al registrar servicio: {e}")
            return None

    def obtener_servicio_por_id(self, id_servicio):
        """Obtiene un servicio por su ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM servicios WHERE id_servicio = ?"
            cursor.execute(query, (id_servicio,))
            resultado = cursor.fetchone()
            
            conn.close()
            
            if resultado:
                return {
                    "id_servicio": resultado[0],
                    "numero_medidor": resultado[1],
                    "nombre_usuario": resultado[2],
                    "direccion_usuario": resultado[3],
                    "usuario_servicio": resultado[4],
                    "monto_servicio": resultado[5],
                    "pago_uno": resultado[6],
                    "pago_dos": resultado[7],
                    "pago_tres": resultado[8],
                    "pago_cuatro": resultado[9]
                }
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Error al obtener servicio: {e}")
            return None

    def obtener_servicios_por_medidor(self, id):
        """Obtiene todos los servicios de un cliente por su número de medidor."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM servicios WHERE numero_medidor = ?"
            cursor.execute(query, (id,))
            resultados = cursor.fetchall()
            
            conn.close()
            
            servicios = []
            for resultado in resultados:
                servicios.append({
                    "id_servicio": resultado[0],
                    "numero_medidor": resultado[1],
                    "nombre_usuario": resultado[2],
                    "direccion_usuario": resultado[3],
                    "usuario_servicio": resultado[4],
                    "monto_servicio": resultado[5],
                    "pago_uno": resultado[6],
                    "pago_dos": resultado[7],
                    "pago_tres": resultado[8],
                    "pago_cuatro": resultado[9]
                })
            
            return servicios
                
        except sqlite3.Error as e:
            print(f"Error al obtener servicios: {e}")
            return []

    def actualizar_servicio(self, id_servicio, datos_servicio):
        """Actualiza un servicio existente."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                UPDATE servicios SET
                    usuario_servicio = ?,
                    monto_servicio = ?,
                    pago_uno = ?,
                    pago_dos = ?,
                    pago_tres = ?,
                    pago_cuatro = ?
                WHERE id_servicio = ?
            """
            
            cursor.execute(query, (
                datos_servicio["usuario_servicio"],
                datos_servicio["monto_servicio"],
                datos_servicio.get("pago_uno", 0),
                datos_servicio.get("pago_dos", 0),
                datos_servicio.get("pago_tres", 0),
                datos_servicio.get("pago_cuatro", 0),
                id_servicio
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Error al actualizar servicio: {e}")
            return False

    def eliminar_servicio(self, id_servicio):
        """Elimina un servicio por su ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "DELETE FROM servicios WHERE id_servicio = ?"
            cursor.execute(query, (id_servicio,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Error al eliminar servicio: {e}")
            return False 