"""
Script de compilacion para Celestine V.1.2.0
Usa enfoque de linea de comandos de PyInstaller
"""
import os
import sys
import shutil
import subprocess

print("="*60)
print("Celestine V.1.2.0 - Build Installer")
print("Compilacion via Linea de Comandos")
print("="*60)
print()

# Paso 1: Verificar dependencias
print("[1/4] Verificando dependencias...")
result = subprocess.run([sys.executable, "verificar_dependencias.py"])
if result.returncode != 0:
    print("\n[ERROR] Faltan dependencias criticas.")
    sys.exit(1)

# Paso 2: Limpiar compilaciones anteriores
print("\n[2/4] Limpiando compilaciones anteriores...")
if os.path.exists("dist/Celestine.exe"):
    os.remove("dist/Celestine.exe")
    print("  - Ejecutable anterior eliminado")
if os.path.exists("build"):
    shutil.rmtree("build")
    print("  - Directorio build eliminado")
if os.path.exists("Celestine.spec"):
    os.remove("Celestine.spec")
    print("  - Archivo spec anterior eliminado")

# Paso 3: Compilar con PyInstaller
print("\n[3/4] Compilando con PyInstaller (linea de comandos)...")
print("Este proceso puede tomar varios minutos...")
print()

# Construir el comando de PyInstaller
pyinstaller_cmd = [
    "pyinstaller",
    "--noconfirm",
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

    # Hidden imports - Otras librerias criticas
    "--hidden-import", "reportlab",
    "--hidden-import", "reportlab.pdfgen",
    "--hidden-import", "reportlab.lib",
    "--hidden-import", "reportlab.platypus",
    "--hidden-import", "bcrypt",
    "--hidden-import", "sqlite3",
    "--hidden-import", "pandas",
    "--hidden-import", "numpy",
    "--hidden-import", "openpyxl",
    "--hidden-import", "xlsxwriter",
    "--hidden-import", "qrcode",
    "--hidden-import", "fitz",

    # Hidden imports - Controladores
    "--hidden-import", "app.controllers.client_controller",
    "--hidden-import", "app.controllers.lectura_controller",
    "--hidden-import", "app.controllers.factura_controller",
    "--hidden-import", "app.controllers.consulta_controller",
    "--hidden-import", "app.controllers.recaudacion_controller",
    "--hidden-import", "app.controllers.servicio_controller",

    # Hidden imports - Modelos
    "--hidden-import", "app.models.client",
    "--hidden-import", "app.models.lectura",
    "--hidden-import", "app.models.factura",
    "--hidden-import", "app.models.servicio",

    # Hidden imports - Vistas
    "--hidden-import", "app.views.login_window",
    "--hidden-import", "app.views.main_window",
    "--hidden-import", "app.views.clients_widget",
    "--hidden-import", "app.views.lecturas_widget",
    "--hidden-import", "app.views.facturas_widget",
    "--hidden-import", "app.views.datos_recaudacion",
    "--hidden-import", "app.views.consulta_widget",
    "--hidden-import", "app.views.consulta_lecturas_widget",
    "--hidden-import", "app.views.consulta_clientes_widget",
    "--hidden-import", "app.views.servicios_widget",
    "--hidden-import", "app.views.consulta_registros_y_deudas",

    # Hidden imports - Database y Helpers
    "--hidden-import", "app.database.connection",
    "--hidden-import", "app.database.init_db",
    "--hidden-import", "app.helpers.backup_helper",
    "--hidden-import", "app.helpers.database_migrator",
    "--hidden-import", "app.helpers.logger",
    "--hidden-import", "app.helpers.pdf_generator",
    "--hidden-import", "app.helpers.reporte_generator",

    # Exclusiones
    "--exclude-module", "tkinter",
    "--exclude-module", "IPython",
    "--exclude-module", "jupyter",
    "--exclude-module", "notebook",
    "--exclude-module", "sphinx",
    "--exclude-module", "pytest",
    "--exclude-module", "setuptools",

    # Icono
    "--icon", "app/resources/CelestineICO.ico",

    # Archivo principal
    "main.py"
]

# Ejecutar PyInstaller
result = subprocess.run(pyinstaller_cmd)

if result.returncode != 0:
    print("\n[ERROR] Fallo la compilacion.")
    sys.exit(1)

# Paso 4: Verificar ejecutable generado
print("\n[4/4] Verificando ejecutable generado...")
exe_path = "dist/Celestine.exe"
if os.path.exists(exe_path):
    exe_size = os.path.getsize(exe_path)
    exe_size_mb = exe_size / (1024 * 1024)

    print()
    print("="*60)
    print("[OK] Compilacion exitosa!")
    print("="*60)
    print()
    print(f"Ejecutable: {exe_path}")
    print(f"Tamano: {exe_size:,} bytes (aprox. {exe_size_mb:.1f} MB)")
    print()
    print("IMPORTANTE:")
    print("- El ejecutable NO incluye la base de datos")
    print("- Copie Celestine.exe JUNTO a sistema_facturacion.db")
    print("- Ambos archivos deben estar en la MISMA carpeta")
    print("- Las facturas se guardaran correctamente")
    print()
    print("ESTRUCTURA CORRECTA:")
    print("  C:\\Facturacion\\")
    print("    - Celestine.exe")
    print("    - sistema_facturacion.db")
    print()
    print("Correcciones aplicadas:")
    print("  [OK] PIL/Pillow incluido")
    print("  [OK] matplotlib incluido")
    print("  [OK] Rutas de BD corregidas (absolutas)")
    print("  [OK] Facturas se guardan correctamente")
    print("  [OK] Sin emojis Unicode")
    print()
    print("="*60)
else:
    print("\n[ERROR] No se encontro el ejecutable generado.")
    sys.exit(1)
