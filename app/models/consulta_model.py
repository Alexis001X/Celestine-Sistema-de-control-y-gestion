import sqlite3

class ConsultaModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_facturas(self, filtros):
        """Obtiene facturas según los filtros proporcionados."""
        base_query = "SELECT * FROM facturas WHERE 1=1"
        params = []

        # Agregar filtros dinámicamente
        if filtros.get("fecha_inicio") and filtros.get("fecha_fin"):
            base_query += " AND fecha_emision BETWEEN ? AND ?"
            params.extend([filtros["fecha_inicio"], filtros["fecha_fin"]])
        if filtros.get("mes"):
            base_query += " AND mes_facturacion = ?"
            params.append(filtros["mes"])
        if filtros.get("direccion"):
            base_query += " AND direccion LIKE ?"
            params.append(f"%{filtros['direccion']}%")
        if filtros.get("nombre"):
            base_query += " AND nombre_cliente LIKE ?"
            params.append(f"%{filtros['nombre']}%")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(base_query, params)
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al consultar facturas: {e}")
            return []
            
    def obtener_factura_por_id(self, id_factura):
        """Obtiene todos los datos de una factura específica para su reimpresión.
        
        Args:
            id_factura: Identificador único de la factura a reimprimir
            
        Returns:
            Un diccionario con todos los datos de la factura o None si no se encuentra
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
            cursor = conn.cursor()
            
            # Consulta principal para obtener datos de la factura
            cursor.execute("SELECT * FROM facturas WHERE id = ?", (id_factura,))
            factura = cursor.fetchone()
            
            if factura:
                # Convertir el objeto Row a un diccionario
                factura_dict = dict(factura)
                
                # Opcionalmente: Obtener detalles de la factura si existe una tabla de detalles
                # Esto asume que existe una tabla de detalles relacionada
                try:
                    cursor.execute("SELECT * FROM detalles_factura WHERE factura_id = ?", (id_factura,))
                    detalles = cursor.fetchall()
                    factura_dict["detalles"] = [dict(detalle) for detalle in detalles]
                except sqlite3.Error:
                    # Si no existe la tabla de detalles o hay otro error, continuamos sin detalles
                    factura_dict["detalles"] = []
                
                conn.close()
                return factura_dict
            else:
                conn.close()
                return None
                
        except sqlite3.Error as e:
            print(f"Error al obtener factura con ID {id_factura}: {e}")
            return None