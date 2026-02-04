import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta

# Configuración
BACKUP_DIR = "backups"
RETENCION_DIAS = 5  # Mantener solo la copia más reciente en un rango de 5 días

def get_db_path():
    """Obtiene la ruta correcta de la base de datos según el entorno."""
    if getattr(sys, 'frozen', False):
        # Ejecutable: BD está junto al .exe
        return os.path.join(os.path.dirname(sys.executable), 'sistema_facturacion.db')
    else:
        # Desarrollo: BD está en la raíz del proyecto
        return "sistema_facturacion.db"

def crear_backup(db_path=None):
    """Crea un respaldo de la base de datos con la fecha en el nombre del archivo."""
    if db_path is None:
        db_path = get_db_path()

    # Directorio de backups junto a la BD
    db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else '.'
    backup_dir = os.path.join(db_dir, BACKUP_DIR)

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    backup_path = os.path.join(backup_dir, f"backup_{fecha_actual}.db")

    try:
        # Crear la copia de seguridad
        shutil.copy2(db_path, backup_path)
        print(f"[OK] Backup creado: {backup_path}")

        # Limpiar copias antiguas
        limpiar_backups_antiguos(backup_dir)
    except Exception as e:
        print(f"[ERROR] Error al crear backup: {e}")

def limpiar_backups_antiguos(backup_dir=None):
    """Elimina las copias de seguridad antiguas y solo mantiene la más reciente dentro del período de retención."""
    if backup_dir is None:
        db_path = get_db_path()
        db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else '.'
        backup_dir = os.path.join(db_dir, BACKUP_DIR)

    try:
        if not os.path.exists(backup_dir):
            return

        archivos = sorted([
            os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith("backup_") and f.endswith(".db")
        ])

        if len(archivos) > 1:  # Si hay más de una copia, eliminar las antiguas
            fecha_limite = datetime.now() - timedelta(days=RETENCION_DIAS)

            for archivo in archivos[:-1]:  # Mantener solo la más reciente
                fecha_archivo = datetime.strptime(archivo.split("_")[-1].split(".db")[0], "%Y-%m-%d")

                if fecha_archivo < fecha_limite:
                    os.remove(archivo)
                    print(f"[LIMPIEZA] Backup eliminado: {archivo}")

    except Exception as e:
        print(f"[ERROR] Error al limpiar backups antiguos: {e}")

if __name__ == "__main__":
    crear_backup()
