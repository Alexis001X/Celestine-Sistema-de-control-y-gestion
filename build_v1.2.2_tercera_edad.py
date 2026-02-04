"""
Script de compilacion para Celestine V.1.2.2 - Tercera Edad y Discapacitados
Incluye funcionalidad de descuento 50% para tercera edad y discapacitados
"""
import os
import sys
import shutil
import subprocess

print("="*60)
print("Celestine V.1.2.2 - Build Installer")
print("Nueva funcionalidad: Descuento Tercera Edad y Discapacitados")
print("="*60)
print()

# Paso 1: Verificar dependencias
print("[1/5] Verificando dependencias...")
result = subprocess.run([sys.executable, "verificar_dependencias.py"])
if result.returncode != 0:
    print("\n[ERROR] Faltan dependencias criticas.")
    sys.exit(1)

# Paso 2: Limpiar compilaciones anteriores
print("\n[2/5] Limpiando compilaciones anteriores...")
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
print("\n[3/5] Compilando con PyInstaller...")
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
    "--hidden-import", "app.views.factura_edit",

    # Hidden imports - Database y Helpers
    "--hidden-import", "app.database.connection",
    "--hidden-import", "app.database.init_db",
    "--hidden-import", "app.helpers.backup_helper",
    "--hidden-import", "app.helpers.database_migrator",
    "--hidden-import", "app.helpers.logger",
    "--hidden-import", "app.helpers.pdf_generator",
    "--hidden-import", "app.helpers.reporte_generator",
    "--hidden-import", "app.helpers.recuperar_lecturas",
    "--hidden-import", "app.helpers.secuencia_facturacion",

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

# Paso 4: Copiar base de datos y crear estructura de carpetas
print("\n[4/5] Creando estructura de carpetas y copiando archivos...")

# Crear carpetas necesarias
folders = ["facturas_pdf", "logs", "reportes"]
for folder in folders:
    folder_path = os.path.join("dist", folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"  - Carpeta creada: {folder}")

# Copiar base de datos
if os.path.exists("sistema_facturacion.db"):
    shutil.copy("sistema_facturacion.db", "dist/sistema_facturacion.db")
    print("  - Base de datos copiada a dist/")
else:
    print("  [ADVERTENCIA] No se encontro sistema_facturacion.db")

# Crear archivo de notas de version
notas_version = """CELESTINE V.1.2.2 - NOTAS DE VERSION
====================================

NUEVA FUNCIONALIDAD - DESCUENTO TERCERA EDAD Y DISCAPACITADOS
--------------------------------------------------------------

Se ha agregado una nueva funcionalidad de descuento especial para
personas de tercera edad y con discapacidad.

CARACTERISTICAS:
- Descuento del 50% en la tarifa base del servicio
- Aplicable a todos los tipos de servicio:
  * DOMICILIARIA: $2.50 → $1.25
  * COMERCIAL: $3.50 → $1.75
  * INDUSTRIAL: $4.50 → $2.25

- Checkbox destacado en color azul en el formulario de registro
- Checkbox visible en la columna de acciones al editar facturas
- El descuento se guarda en la base de datos
- Compatible con todas las demás funcionalidades

UBICACION:
- Registro de Facturas: Al final del formulario, antes de "INFORMACION DE DEUDA"
- Edicion de Facturas: Columna derecha "ACCIONES", sección "DESCUENTO ESPECIAL"

MIGRACIONES AUTOMATICAS:
- Al iniciar el sistema por primera vez, se agregará automáticamente
  el campo "tercera_edad" a la tabla facturas
- No requiere intervención manual

CORRECCIONES ANTERIORES INCLUIDAS:
- [OK] PIL/Pillow para generación de QR y PDF
- [OK] matplotlib para dashboard
- [OK] Guardado correcto de facturas en BD
- [OK] Soporte para BD externa flexible
- [OK] Migraciones automáticas de esquema

INSTALACION:
1. Copie Celestine.exe junto a sistema_facturacion.db
2. Ejecute Celestine.exe
3. El sistema aplicará automáticamente las migraciones necesarias
4. La funcionalidad de tercera edad estará disponible de inmediato

IMPORTANTE:
- La base de datos incluida ya tiene el campo "tercera_edad"
- Si usa una BD antigua, la migración se aplicará automáticamente
- El descuento NO afecta tarifas excedentes ni servicios adicionales
- Solo aplica a la tarifa base del servicio

Fecha: Noviembre 2024
Version: 1.2.2
"""

with open("dist/NOTAS_VERSION_1.2.2.txt", "w", encoding="utf-8") as f:
    f.write(notas_version)
print("  - Notas de versión creadas")

# Paso 5: Verificar ejecutable generado
print("\n[5/5] Verificando ejecutable generado...")
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
    print("CONTENIDO DEL PAQUETE:")
    print("  - Celestine.exe")
    print("  - sistema_facturacion.db (con campo tercera_edad)")
    print("  - facturas_pdf/ (carpeta)")
    print("  - logs/ (carpeta)")
    print("  - reportes/ (carpeta)")
    print("  - NOTAS_VERSION_1.2.2.txt")
    print()
    print("NUEVA FUNCIONALIDAD V.1.2.2:")
    print("  [NUEVO] Descuento Tercera Edad y Discapacitados (50%)")
    print("  [NUEVO] Checkbox destacado en formulario de facturas")
    print("  [NUEVO] Migracion automatica de campo tercera_edad")
    print("  [NUEVO] Guardado y carga de estado en edicion")
    print()
    print("FUNCIONALIDADES ANTERIORES:")
    print("  [OK] PIL/Pillow incluido")
    print("  [OK] matplotlib incluido")
    print("  [OK] Facturas se guardan correctamente")
    print("  [OK] Soporte BD externa flexible")
    print("  [OK] Migraciones automaticas")
    print()
    print("LISTO PARA DISTRIBUIR:")
    print("  Todo el contenido de la carpeta 'dist/' puede ser")
    print("  copiado y distribuido. El sistema funcionara de inmediato.")
    print()
    print("="*60)
else:
    print("\n[ERROR] No se encontro el ejecutable generado.")
    sys.exit(1)
