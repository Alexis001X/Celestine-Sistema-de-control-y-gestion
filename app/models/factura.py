import sqlite3

class FacturaModel:
    def __init__(self, db_path):
        self.db_path = db_path
        self._verificar_campo_numero_factura()

    def _verificar_campo_numero_factura(self):
        """Verifica y agrega el campo numero_factura si no existe."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, isolation_level='DEFERRED')
            cursor = conn.cursor()

            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(facturas)")
            columnas = [columna[1] for columna in cursor.fetchall()]

            if "numero_factura" not in columnas:
                # Agregar la columna
                cursor.execute("""
                    ALTER TABLE facturas
                    ADD COLUMN numero_factura TEXT
                """)
                conn.commit()
                print("[OK] Campo 'numero_factura' agregado a la tabla facturas")

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Error al verificar campo numero_factura: {e}")
        finally:
            if conn:
                conn.close()

    def registrar_factura(self, datos):
        """Registra una factura en la base de datos."""
        query = """
            INSERT INTO facturas (
                medidor_id, nombre_cliente, lectura_id, mes_facturacion,
                monto_total, fecha_emision, estado, servicio, traspaso, medidor,
                reconexion, multas_sesiones, otros, tarifa_basica, tarifa_excedente,
                direccion, monto_lectura, conexion_nueva, multas_mingas, materiales, numero_factura, tercera_edad
            ) VALUES (:medidor_id, :nombre_cliente, :lectura_id, :mes_facturacion,
                :monto_total, :fecha_emision, :estado, :servicio, :traspaso, :medidor,
                :reconexion, :multas_sesiones, :otros, :tarifa_basica, :tarifa_excedente,
                :direccion, :monto_lectura, :conexion_nueva, :multas_mingas, :materiales, :numero_factura, :tercera_edad)
        """
        conn = None
        try:
            # Conectar a la base de datos con ruta absoluta
            conn = sqlite3.connect(self.db_path, isolation_level='DEFERRED')
            cursor = conn.cursor()

            # Ejecutar el INSERT
            cursor.execute(query, datos)
            factura_id = cursor.lastrowid

            # COMMIT EXPLÍCITO - CRÍTICO PARA PRODUCCIÓN
            conn.commit()

            # Verificar que se guardó
            cursor.execute("SELECT id FROM facturas WHERE id = ?", (factura_id,))
            verificacion = cursor.fetchone()

            if not verificacion:
                raise Exception(f"Factura {factura_id} no se encontró después del commit")

            return factura_id

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Error al registrar factura: {e}")
            return False
        finally:
            if conn:
                conn.close()
