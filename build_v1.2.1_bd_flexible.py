"""
Celestine V.1.2.1 - Build Script con Soporte para BD Externa
==============================================================

NUEVAS FUNCIONALIDADES:
- Soporte para multiples fuentes de BD (CLI, config.txt, importar_bd.db)
- Migracion automatica de bases de datos antiguas
- Recarga forzada de conexiones para cambio de BD en caliente

DIFERENCIAS CON V.1.2.0:
- Solucion #3: Parametros de linea de comandos
- Solucion #5: Migracion automatica de BD externa
- Mejora: Forzar recarga de conexiones
"""

import subprocess
import sys
import os
import shutil

# Colores para mensajes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_section(title):
    """Imprime un titulo de seccion"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def verificar_dependencias():
    """Verifica que todas las dependencias criticas esten instaladas"""
    print_section("VERIFICACION DE DEPENDENCIAS CRITICAS")

    dependencias = [
        ("PyQt6", "PyQt6"),
        ("PyQt6.QtGui", "PyQt6.QtGui"),
        ("PyQt6.QtWidgets", "PyQt6.QtWidgets"),
        ("PIL", "Pillow"),
        ("reportlab", "reportlab"),
        ("bcrypt", "bcrypt"),
        ("sqlite3", "sqlite3"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("openpyxl", "openpyxl"),
        ("qrcode", "qrcode"),
        ("fitz", "PyMuPDF"),
        ("matplotlib", "matplotlib"),
    ]

    todas_ok = True
    for modulo, nombre_paquete in dependencias:
        try:
            __import__(modulo)
            print(f"[OK] {nombre_paquete:25} - Instalado")
        except ImportError:
            print(f"[ERROR] {nombre_paquete:25} - NO INSTALADO")
            todas_ok = False

    print()
    if todas_ok:
        print("=" * 60)
        print("[EXITO] TODAS LAS DEPENDENCIAS ESTAN INSTALADAS")
        print("        Puedes proceder a compilar el ejecutable")
        print("=" * 60)
        return True
    else:
        print("=" * 60)
        print("[ERROR] FALTAN DEPENDENCIAS")
        print("        Instala las dependencias faltantes con:")
        print("        pip install <nombre_paquete>")
        print("=" * 60)
        return False


def limpiar_compilaciones_anteriores():
    """Limpia los archivos de compilaciones anteriores"""
    print("[2/4] Limpiando compilaciones anteriores...")

    # Eliminar ejecutable anterior en dist_v1.2.1 si existe
    if os.path.exists("dist_v1.2.1/Celestine.exe"):
        os.remove("dist_v1.2.1/Celestine.exe")
        print("  - Ejecutable anterior eliminado")

    # Eliminar directorio build si existe
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("  - Directorio build eliminado")

    # Eliminar archivo spec anterior si existe
    if os.path.exists("Celestine.spec"):
        os.remove("Celestine.spec")
        print("  - Archivo spec anterior eliminado")

    print()


def compilar_con_pyinstaller():
    """Ejecuta PyInstaller con los parametros correctos"""
    print("[3/4] Compilando con PyInstaller (linea de comandos)...")
    print("Este proceso puede tomar varios minutos...")
    print()

    # Argumentos de PyInstaller
    args = [
        sys.executable, "-m", "PyInstaller",

        # Configuracion basica
        "--onefile",
        "--windowed",
        "--name", "Celestine",

        # Datos de la aplicacion (NO incluir la base de datos)
        "--add-data", "app/controllers;app/controllers",
        "--add-data", "app/models;app/models",
        "--add-data", "app/views;app/views",
        "--add-data", "app/database;app/database",
        "--add-data", "app/helpers;app/helpers",
        "--add-data", "app/resources;app/resources",

        # Hidden imports - PIL/Pillow (CRITICO para ReportLab y QR)
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageDraw",
        "--hidden-import", "PIL.ImageFont",
        "--hidden-import", "PIL._imaging",

        # Hidden imports - matplotlib (CRITICO para Dashboard)
        "--hidden-import", "matplotlib",
        "--hidden-import", "matplotlib.figure",
        "--hidden-import", "matplotlib.backends",
        "--hidden-import", "matplotlib.backends.backend_qt5agg",
        "--hidden-import", "matplotlib.backends.backend_qtagg",

        # Hidden imports - PyQt6
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtPrintSupport",

        # Hidden imports - Otros modulos
        "--hidden-import", "pandas",
        "--hidden-import", "qrcode",
        "--hidden-import", "fitz",

        # Icono
        "--icon", "app/resources/CelestineICO.ico",

        # Archivo principal
        "main.py"
    ]

    # Ejecutar PyInstaller
    resultado = subprocess.run(args, capture_output=False, text=True)

    print()
    return resultado.returncode == 0


def verificar_ejecutable():
    """Verifica que el ejecutable se haya generado correctamente"""
    print("[4/4] Verificando ejecutable generado...")
    print()

    ejecutable = "dist/Celestine.exe"

    if os.path.exists(ejecutable):
        # Mover a dist_v1.2.1
        os.makedirs("dist_v1.2.1", exist_ok=True)
        shutil.move(ejecutable, "dist_v1.2.1/Celestine.exe")

        # Eliminar dist vacio
        if os.path.exists("dist") and not os.listdir("dist"):
            os.rmdir("dist")

        ejecutable = "dist_v1.2.1/Celestine.exe"
        tamano = os.path.getsize(ejecutable)
        tamano_mb = tamano / (1024 * 1024)

        print_section("[OK] Compilacion exitosa!")
        print(f"Ejecutable: {ejecutable}")
        print(f"Tamano: {tamano:,} bytes (aprox. {tamano_mb:.1f} MB)")
        print()
        print("IMPORTANTE:")
        print("- El ejecutable NO incluye la base de datos")
        print("- Copie Celestine.exe JUNTO a sistema_facturacion.db")
        print("- Ambos archivos deben estar en la MISMA carpeta")
        print()
        print("NUEVAS FUNCIONALIDADES V.1.2.1:")
        print("- Soporte para BD externa via parametros CLI")
        print("- Migracion automatica con importar_bd.db")
        print("- Configuracion via config.txt")
        print()
        print("ESTRUCTURA CORRECTA:")
        print("  C:\\Facturacion\\")
        print("    - Celestine.exe")
        print("    - sistema_facturacion.db       (BD principal)")
        print("    - importar_bd.db               (opcional: BD a migrar)")
        print("    - config.txt                   (opcional: ruta BD custom)")
        print()
        print("Correcciones aplicadas:")
        print("  [OK] PIL/Pillow incluido")
        print("  [OK] matplotlib incluido")
        print("  [OK] Rutas de BD corregidas (absolutas)")
        print("  [OK] Soporte multiples fuentes de BD")
        print("  [OK] Migracion automatica de BD")
        print("  [OK] Recarga forzada de conexiones")
        print()
        print_section("")

        return True
    else:
        print_section("[ERROR] No se encontro el ejecutable")
        print("La compilacion fallo. Revisa los mensajes de error anteriores.")
        return False


def main():
    """Funcion principal del script de compilacion"""
    print_section("Celestine V.1.2.1 - Build Installer")
    print("Compilacion via Linea de Comandos")
    print("Con soporte para BD Externa")
    print_section("")

    # Paso 1: Verificar dependencias
    print("[1/4] Verificando dependencias...")
    if not verificar_dependencias():
        sys.exit(1)

    print()

    # Paso 2: Limpiar compilaciones anteriores
    limpiar_compilaciones_anteriores()

    # Paso 3: Compilar con PyInstaller
    if not compilar_con_pyinstaller():
        print()
        print_section("[ERROR] Compilacion fallida")
        print("Revisa los mensajes de error de PyInstaller anteriores.")
        sys.exit(1)

    # Paso 4: Verificar ejecutable
    if not verificar_ejecutable():
        sys.exit(1)


if __name__ == "__main__":
    main()
