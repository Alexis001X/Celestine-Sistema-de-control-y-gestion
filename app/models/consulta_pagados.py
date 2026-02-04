# app/models/consulta_pagados.py
import sqlite3

class ConsultaRegistrosYDeudasModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_pagados(self, mes_facturacion, direccion):
        """Obtiene los usuarios que han registrado facturas en un mes específico con estado 'Pagado'."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = """
                SELECT f.medidor_id, c.nombre_cliente, f.estado, c.direccion
                FROM facturas f
                JOIN clientes c ON f.medidor_id = c.id
                WHERE f.mes_facturacion = ? AND f.estado = 'Pagado' AND c.direccion LIKE ?
            """
            cursor.execute(query, (mes_facturacion, f"%{direccion}%"))
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al obtener usuarios pagados: {e}")
            return []

    def obtener_deudores(self, mes_facturacion, direccion):
        """Obtiene los clientes que no tienen facturas registradas en el mes especificado o cuya factura está en estado 'Deuda'."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = """
                SELECT c.id, c.nombre_cliente, COALESCE(f.estado, 'Sin registrar') AS estado_factura, c.direccion
                FROM clientes c
                LEFT JOIN facturas f ON c.id = f.medidor_id AND f.mes_facturacion = ?
                WHERE (f.estado IS NULL OR f.estado = 'Deuda') AND c.direccion LIKE ?
            """
            cursor.execute(query, (mes_facturacion, f"%{direccion}%"))
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al obtener deudores sin facturas: {e}")
            return []

    def mostrar_deudores_por_totales(self, direccion):
        """Obtiene los clientes y cuenta el número de facturas en estado 'Deuda', devolviendo solo los que tienen al menos 1 en deuda."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = """
                SELECT c.id, c.nombre_cliente, COUNT(f.id) AS facturas_en_deuda, c.direccion
                FROM clientes c
                JOIN facturas f ON c.id = f.medidor_id
                WHERE f.estado = 'Deuda' AND c.direccion LIKE ?
                GROUP BY c.id
                HAVING COUNT(f.id) > 0
            """
            cursor.execute(query, (f"%{direccion}%",))
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al obtener deudores por totales: {e}")
            return []
