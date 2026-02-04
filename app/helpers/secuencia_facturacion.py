import sqlite3
from pathlib import Path


class SecuenciaFacturacion:
    """
    Gestiona las secuencias de numeración de facturas.

    Permite manejar múltiples secuencias de facturación con diferentes formatos,
    por ejemplo: 001-001-XXXXXXXXX y 001-010-XXXXXXXXX
    """

    def __init__(self, db_path):
        """
        Inicializa el gestor de secuencias.

        Args:
            db_path: Ruta a la base de datos SQLite
        """
        self.db_path = db_path
        self._crear_tabla_secuencias()

    def _crear_tabla_secuencias(self):
        """
        Crea la tabla de secuencias si no existe.

        Campos:
        - id: ID autoincremental
        - establecimiento: Código de establecimiento (ej: "001")
        - punto_emision: Código de punto de emisión (ej: "001" o "010")
        - secuencial: Último número secuencial utilizado
        - activo: Indica si esta secuencia está activa (1) o no (0)
        - fecha_creacion: Fecha de creación de la secuencia
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS secuencias_facturacion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    establecimiento TEXT NOT NULL,
                    punto_emision TEXT NOT NULL,
                    secuencial INTEGER NOT NULL DEFAULT 0,
                    activo INTEGER NOT NULL DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(establecimiento, punto_emision)
                )
            """)

            conn.commit()
            conn.close()

            # Inicializar la nueva secuencia 001-010 si no existe
            self._inicializar_secuencia_001_010()

        except sqlite3.Error as e:
            print(f"Error al crear tabla de secuencias: {e}")

    def _inicializar_secuencia_001_010(self):
        """
        Inicializa la secuencia 001-010 si no existe.
        Esta es la nueva secuencia que comienza desde 1.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verificar si ya existe la secuencia 001-010
            cursor.execute("""
                SELECT id FROM secuencias_facturacion
                WHERE establecimiento = '001' AND punto_emision = '010'
            """)

            if not cursor.fetchone():
                # Insertar la nueva secuencia
                cursor.execute("""
                    INSERT INTO secuencias_facturacion (establecimiento, punto_emision, secuencial, activo)
                    VALUES ('001', '010', 0, 1)
                """)
                conn.commit()
                print("Secuencia 001-010 inicializada correctamente")

            conn.close()

        except sqlite3.Error as e:
            print(f"Error al inicializar secuencia 001-010: {e}")

    def obtener_siguiente_numero(self, establecimiento="001", punto_emision="010"):
        """
        Obtiene y reserva el siguiente número de factura disponible en la secuencia.

        IMPORTANTE: Esta función busca el primer número disponible (hueco) en la
        secuencia de facturas. Si se elimina una factura, su número será reutilizado.

        Args:
            establecimiento: Código de establecimiento (default: "001")
            punto_emision: Código de punto de emisión (default: "010")

        Returns:
            str: Número de factura formateado (ej: "001-010-0000000001")
            None: Si hay un error
        """
        conn = None
        try:
            # Conectar con isolation_level DEFERRED para transacción explícita
            conn = sqlite3.connect(self.db_path, isolation_level='DEFERRED')
            cursor = conn.cursor()

            # Prefijo del número de factura
            prefijo = f"{establecimiento}-{punto_emision}-"

            # Buscar el primer número disponible en la secuencia
            # Obtener todos los números de factura existentes con este prefijo
            cursor.execute("""
                SELECT numero_factura
                FROM facturas
                WHERE numero_factura LIKE ?
                ORDER BY numero_factura ASC
            """, (f"{prefijo}%",))

            numeros_existentes = cursor.fetchall()

            # Extraer solo los secuenciales numéricos
            secuenciales_usados = set()
            for (numero_completo,) in numeros_existentes:
                try:
                    # Extraer la parte del secuencial (después del segundo guion)
                    partes = numero_completo.split('-')
                    if len(partes) == 3:
                        secuencial = int(partes[2])
                        secuenciales_usados.add(secuencial)
                except (ValueError, IndexError):
                    continue

            # Buscar el primer número disponible (el primer hueco o el siguiente)
            secuencial_nuevo = 1
            while secuencial_nuevo in secuenciales_usados:
                secuencial_nuevo += 1

            # Actualizar la tabla de secuencias con el mayor valor encontrado
            # (solo para mantener un registro del último número usado)
            cursor.execute("""
                UPDATE secuencias_facturacion
                SET secuencial = ?
                WHERE establecimiento = ? AND punto_emision = ? AND activo = 1
            """, (secuencial_nuevo, establecimiento, punto_emision))

            if cursor.rowcount == 0:
                print(f"[ERROR] No existe secuencia activa para {establecimiento}-{punto_emision}")
                return None

            # COMMIT EXPLÍCITO - CRÍTICO
            conn.commit()

            # Verificar que se guardó
            cursor.execute("""
                SELECT secuencial
                FROM secuencias_facturacion
                WHERE establecimiento = ? AND punto_emision = ?
            """, (establecimiento, punto_emision))

            verificacion = cursor.fetchone()

            if not verificacion or verificacion[0] != secuencial_nuevo:
                raise Exception(f"Secuencial {secuencial_nuevo} no se confirmó después del commit")

            # Formatear como 001-010-0000000001 (10 dígitos para el secuencial)
            numero_factura = f"{establecimiento}-{punto_emision}-{secuencial_nuevo:010d}"
            print(f"[OK] Número de factura generado: {numero_factura} (primer número disponible)")
            return numero_factura

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Error al obtener siguiente número de factura: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def obtener_secuencial_actual(self, establecimiento="001", punto_emision="010"):
        """
        Obtiene el secuencial actual sin incrementarlo.

        Args:
            establecimiento: Código de establecimiento
            punto_emision: Código de punto de emisión

        Returns:
            int: Secuencial actual
            None: Si hay un error
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT secuencial
                FROM secuencias_facturacion
                WHERE establecimiento = ? AND punto_emision = ?
            """, (establecimiento, punto_emision))

            resultado = cursor.fetchone()
            conn.close()

            return resultado[0] if resultado else None

        except sqlite3.Error as e:
            print(f"Error al obtener secuencial actual: {e}")
            return None

    def formatear_numero_factura(self, secuencial, establecimiento="001", punto_emision="010"):
        """
        Formatea un número secuencial como número de factura.

        Args:
            secuencial: Número secuencial
            establecimiento: Código de establecimiento
            punto_emision: Código de punto de emisión

        Returns:
            str: Número formateado (ej: "001-010-0000000123")
        """
        return f"{establecimiento}-{punto_emision}-{secuencial:010d}"

    def crear_nueva_secuencia(self, establecimiento, punto_emision, secuencial_inicial=0):
        """
        Crea una nueva secuencia de facturación.

        Args:
            establecimiento: Código de establecimiento
            punto_emision: Código de punto de emisión
            secuencial_inicial: Número inicial de la secuencia

        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO secuencias_facturacion (establecimiento, punto_emision, secuencial, activo)
                VALUES (?, ?, ?, 1)
            """, (establecimiento, punto_emision, secuencial_inicial))

            conn.commit()
            conn.close()

            print(f"Secuencia {establecimiento}-{punto_emision} creada correctamente")
            return True

        except sqlite3.IntegrityError:
            print(f"La secuencia {establecimiento}-{punto_emision} ya existe")
            return False
        except sqlite3.Error as e:
            print(f"Error al crear nueva secuencia: {e}")
            return False

    def desactivar_secuencia(self, establecimiento, punto_emision):
        """
        Desactiva una secuencia de facturación.

        Args:
            establecimiento: Código de establecimiento
            punto_emision: Código de punto de emisión

        Returns:
            bool: True si se desactivó exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE secuencias_facturacion
                SET activo = 0
                WHERE establecimiento = ? AND punto_emision = ?
            """, (establecimiento, punto_emision))

            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as e:
            print(f"Error al desactivar secuencia: {e}")
            return False

    def listar_secuencias(self):
        """
        Lista todas las secuencias de facturación.

        Returns:
            list: Lista de tuplas con información de secuencias
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT establecimiento, punto_emision, secuencial, activo, fecha_creacion
                FROM secuencias_facturacion
                ORDER BY fecha_creacion DESC
            """)

            resultados = cursor.fetchall()
            conn.close()

            return resultados

        except sqlite3.Error as e:
            print(f"Error al listar secuencias: {e}")
            return []


# Función de conveniencia para obtener la instancia
_secuencia_instance = None

def get_secuencia_facturacion(db_path="sistema_facturacion.db"):
    """
    Obtiene la instancia del gestor de secuencias (patrón Singleton).

    Args:
        db_path: Ruta a la base de datos

    Returns:
        SecuenciaFacturacion: Instancia del gestor
    """
    global _secuencia_instance
    if _secuencia_instance is None:
        _secuencia_instance = SecuenciaFacturacion(db_path)
    return _secuencia_instance
