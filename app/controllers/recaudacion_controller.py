import sqlite3
from datetime import datetime

class RecaudacionController:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_años_disponibles(self):
        """Obtiene los años disponibles en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT strftime('%Y', fecha_emision) as año 
            FROM facturas 
            ORDER BY año DESC
        """)
        años = [str(row[0]) for row in cursor.fetchall()]
        conn.close()
        return años if años else [str(datetime.now().year)]

    def obtener_direcciones_disponibles(self):
        """Obtiene las direcciones disponibles en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT direccion FROM facturas ORDER BY direccion")
        direcciones = [row[0] for row in cursor.fetchall()]
        conn.close()
        return direcciones

    def obtener_datos_recaudacion(self, anio, direccion):
        """Obtiene los datos de recaudación filtrados por año y dirección."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT mes_facturacion, COUNT(*) as cantidad
            FROM facturas
            WHERE strftime('%Y', fecha_emision) = ?
        """
        params = [anio]
        
        if direccion != "Todas":
            query += " AND direccion = ?"
            params.append(direccion)
            
        query += " GROUP BY mes_facturacion ORDER BY CASE mes_facturacion "
        for i, mes in enumerate(["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]):
            query += f"WHEN '{mes}' THEN {i} "
        query += "END"
        
        cursor.execute(query, params)
        datos = cursor.fetchall()
        conn.close()
        return datos

    def realizar_cierre_caja(self):
        """Función en desarrollo."""
        return False, "Esta función se encuentra en desarrollo. Por favor, intente más tarde."
