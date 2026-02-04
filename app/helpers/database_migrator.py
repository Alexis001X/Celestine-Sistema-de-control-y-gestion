"""
Sistema de migración automática de base de datos.

Este módulo se ejecuta automáticamente al iniciar la aplicación y asegura
que todas las tablas y campos necesarios existan en la base de datos.
"""

import sqlite3
import os
from pathlib import Path


class DatabaseMigrator:
    """Gestiona las migraciones de la base de datos."""

    def __init__(self, db_path):
        """
        Inicializa el migrador de base de datos.

        Args:
            db_path: Ruta a la base de datos SQLite
        """
        self.db_path = db_path
        self.ensure_database_exists()

    def ensure_database_exists(self):
        """Asegura que la base de datos existe."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def run_all_migrations(self):
        """
        Ejecuta todas las migraciones necesarias.

        Este método debe ser llamado al iniciar la aplicación para
        asegurar que la base de datos esté actualizada.
        """
        print("=" * 60)
        print("INICIANDO MIGRACIONES DE BASE DE DATOS")
        print("=" * 60)
        print()

        # Migración 1: Campo numero_factura en tabla facturas
        self._migrar_numero_factura()

        # Migración 2: Tabla de secuencias de facturación
        self._migrar_tabla_secuencias()

        # Migración 3: Tabla de logs (si no existe)
        self._migrar_tabla_logs()

        # Migración 4: Campo tercera_edad en tabla facturas
        self._migrar_tercera_edad()

        print()
        print("=" * 60)
        print("MIGRACIONES COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        print()

    def _migrar_numero_factura(self):
        """Agrega el campo numero_factura a la tabla facturas si no existe."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(facturas)")
            columnas = [columna[1] for columna in cursor.fetchall()]

            if "numero_factura" not in columnas:
                print("[OK] Agregando campo 'numero_factura' a tabla facturas...")
                cursor.execute("""
                    ALTER TABLE facturas
                    ADD COLUMN numero_factura TEXT
                """)
                conn.commit()
                print("  [OK] Campo 'numero_factura' agregado exitosamente")
            else:
                print("[OK] Campo 'numero_factura' ya existe en tabla facturas")

            conn.close()

        except sqlite3.Error as e:
            print(f"  [ERROR] Error al migrar campo numero_factura: {e}")

    def _migrar_tabla_secuencias(self):
        """Crea la tabla de secuencias de facturación si no existe."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verificar si la tabla existe
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='secuencias_facturacion'
            """)
            tabla_existe = cursor.fetchone() is not None

            if not tabla_existe:
                print("[OK] Creando tabla 'secuencias_facturacion'...")
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
                print("  [OK] Tabla 'secuencias_facturacion' creada exitosamente")

                # Inicializar la secuencia 001-010
                print("[OK] Inicializando secuencia 001-010...")
                cursor.execute("""
                    INSERT OR IGNORE INTO secuencias_facturacion
                    (establecimiento, punto_emision, secuencial, activo)
                    VALUES ('001', '010', 0, 1)
                """)
                conn.commit()
                print("  [OK] Secuencia 001-010 inicializada (comienza desde 1)")
            else:
                print("[OK] Tabla 'secuencias_facturacion' ya existe")

                # Verificar si existe la secuencia 001-010
                cursor.execute("""
                    SELECT id FROM secuencias_facturacion
                    WHERE establecimiento = '001' AND punto_emision = '010'
                """)
                if not cursor.fetchone():
                    print("[OK] Inicializando secuencia 001-010...")
                    cursor.execute("""
                        INSERT INTO secuencias_facturacion
                        (establecimiento, punto_emision, secuencial, activo)
                        VALUES ('001', '010', 0, 1)
                    """)
                    conn.commit()
                    print("  [OK] Secuencia 001-010 inicializada")
                else:
                    print("[OK] Secuencia 001-010 ya existe")

            conn.close()

        except sqlite3.Error as e:
            print(f"  [ERROR] Error al migrar tabla secuencias: {e}")

    def _migrar_tabla_logs(self):
        """Verifica que exista la carpeta de logs."""
        try:
            # Obtener la ruta base de la aplicación
            if hasattr(self, 'app_path'):
                logs_path = os.path.join(self.app_path, 'logs')
            else:
                # Si no se especifica, usar la ruta relativa a la BD
                db_dir = os.path.dirname(self.db_path)
                logs_path = os.path.join(db_dir, 'logs')

            if not os.path.exists(logs_path):
                print("[OK] Creando carpeta de logs...")
                os.makedirs(logs_path, exist_ok=True)
                print(f"  [OK] Carpeta de logs creada en: {logs_path}")
            else:
                print("[OK] Carpeta de logs ya existe")

        except Exception as e:
            print(f"  [ERROR] Error al crear carpeta de logs: {e}")

    def _migrar_tercera_edad(self):
        """Agrega el campo tercera_edad a la tabla facturas si no existe."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(facturas)")
            columnas = [columna[1] for columna in cursor.fetchall()]

            if "tercera_edad" not in columnas:
                print("[OK] Agregando campo 'tercera_edad' a tabla facturas...")
                cursor.execute("""
                    ALTER TABLE facturas
                    ADD COLUMN tercera_edad INTEGER DEFAULT 0
                """)
                conn.commit()
                print("  [OK] Campo 'tercera_edad' agregado exitosamente")
            else:
                print("[OK] Campo 'tercera_edad' ya existe en tabla facturas")

            conn.close()

        except sqlite3.Error as e:
            print(f"  [ERROR] Error al agregar campo tercera_edad: {e}")


def ejecutar_migraciones(db_path):
    """
    Función de conveniencia para ejecutar todas las migraciones.

    Args:
        db_path: Ruta a la base de datos SQLite

    Returns:
        DatabaseMigrator: Instancia del migrador
    """
    migrator = DatabaseMigrator(db_path)
    migrator.run_all_migrations()
    return migrator


def migrar_bd_externa(bd_externa_path, bd_destino_path):
    """
    Importa y migra una base de datos externa.

    Esta funcion permite importar bases de datos antiguas que no tienen
    las tablas o columnas mas recientes, aplicando automaticamente todas
    las migraciones necesarias.

    Args:
        bd_externa_path: Ruta de la BD externa a importar
        bd_destino_path: Ruta donde quedara la BD migrada

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    import shutil

    print("\n" + "=" * 60)
    print("IMPORTACION Y MIGRACION DE BASE DE DATOS EXTERNA")
    print("=" * 60)
    print(f"Origen:  {bd_externa_path}")
    print(f"Destino: {bd_destino_path}")
    print()

    try:
        # 1. Verificar que BD externa existe
        if not os.path.exists(bd_externa_path):
            mensaje = f"[ERROR] BD externa no existe: {bd_externa_path}"
            print(mensaje)
            return False, mensaje

        # 2. Verificar que BD externa es valida
        print("[1/4] Validando BD externa...")
        try:
            conn = sqlite3.connect(bd_externa_path)
            cursor = conn.cursor()

            # Verificar que tenga tablas basicas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row[0] for row in cursor.fetchall()]

            if 'clientes' not in tablas:
                conn.close()
                mensaje = "[ERROR] BD externa no tiene tabla 'clientes'. No es una BD valida del sistema."
                print(mensaje)
                return False, mensaje

            # Obtener info de la BD
            cursor.execute("SELECT COUNT(*) FROM clientes")
            num_clientes = cursor.fetchone()[0]
            print(f"  [OK] BD valida: {len(tablas)} tablas, {num_clientes} clientes")

            conn.close()

        except sqlite3.Error as e:
            mensaje = f"[ERROR] BD externa corrupta o invalida: {e}"
            print(mensaje)
            return False, mensaje

        # 3. Crear backup de BD destino si existe
        if os.path.exists(bd_destino_path):
            print("[2/4] Creando backup de BD actual...")
            backup_path = bd_destino_path + ".backup_antes_importar"
            shutil.copy2(bd_destino_path, backup_path)
            print(f"  [OK] Backup creado: {backup_path}")
        else:
            print("[2/4] No hay BD destino, se creara nueva")

        # 4. Copiar BD externa a ubicacion destino
        print("[3/4] Copiando BD externa...")
        shutil.copy2(bd_externa_path, bd_destino_path)
        print(f"  [OK] BD copiada a: {bd_destino_path}")

        # 5. Ejecutar migraciones sobre la BD importada
        print("[4/4] Ejecutando migraciones sobre BD importada...")
        print()
        ejecutar_migraciones(bd_destino_path)

        mensaje = "[EXITO] BD importada y migrada correctamente"
        print()
        print("=" * 60)
        print(mensaje)
        print("=" * 60)
        print()

        return True, mensaje

    except Exception as e:
        mensaje = f"[ERROR] Error durante importacion: {e}"
        print(mensaje)
        import traceback
        traceback.print_exc()
        return False, mensaje


def verificar_bd_importar(directorio_ejecutable):
    """
    Verifica si existe un archivo 'importar_bd.db' y lo migra automaticamente.

    Args:
        directorio_ejecutable: Directorio donde esta el ejecutable

    Returns:
        str: Ruta de la BD a usar (puede ser la importada o la default)
    """
    bd_importar = os.path.join(directorio_ejecutable, 'importar_bd.db')
    bd_destino = os.path.join(directorio_ejecutable, 'sistema_facturacion.db')

    if os.path.exists(bd_importar):
        print()
        print("=" * 60)
        print("DETECTADO: importar_bd.db")
        print("=" * 60)
        print("Se procedera a importar y migrar esta base de datos...")
        print()

        exito, mensaje = migrar_bd_externa(bd_importar, bd_destino)

        if exito:
            # Renombrar para que no se importe de nuevo
            bd_importada = bd_importar + ".importada"
            os.rename(bd_importar, bd_importada)
            print(f"[OK] Archivo renombrado a: {os.path.basename(bd_importada)}")
            print("[OK] Para volver a importar, renombre el archivo a 'importar_bd.db'")
        else:
            print("[ERROR] La importacion fallo. Se usara la BD por defecto.")

    return bd_destino


if __name__ == "__main__":
    """
    Script standalone para ejecutar migraciones manualmente.

    Uso:
        python database_migrator.py [ruta_a_base_datos]
    """
    import sys

    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "sistema_facturacion.db"

    print(f"\nEjecutando migraciones en: {db_path}\n")
    ejecutar_migraciones(db_path)
