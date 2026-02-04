@echo off
echo ========================================
echo Celestine V.1.2.0 - Build Installer
echo Compilacion via Linea de Comandos
echo ========================================
echo.

echo [1/4] Verificando dependencias...
python verificar_dependencias.py
if errorlevel 1 (
    echo.
    echo [ERROR] Faltan dependencias criticas. Instale las dependencias faltantes.
    pause
    exit /b 1
)

echo.
echo [2/4] Limpiando compilaciones anteriores...
if exist "dist\Celestine.exe" del /F /Q "dist\Celestine.exe"
if exist "build" rmdir /S /Q "build"
if exist "Celestine.spec" del /F /Q "Celestine.spec"

echo.
echo [3/4] Compilando con PyInstaller (linea de comandos)...
echo Este proceso puede tomar varios minutos...
echo.

pyinstaller --noconfirm --onefile --windowed ^
--name Celestine ^
--add-data "app/controllers;app/controllers" ^
--add-data "app/models;app/models" ^
--add-data "app/views;app/views" ^
--add-data "app/database;app/database" ^
--add-data "app/helpers;app/helpers" ^
--add-data "app/resources;app/resources" ^
--hidden-import PIL ^
--hidden-import PIL.Image ^
--hidden-import PIL.ImageDraw ^
--hidden-import PIL.ImageFont ^
--hidden-import PIL._imaging ^
--hidden-import matplotlib ^
--hidden-import matplotlib.figure ^
--hidden-import matplotlib.backends ^
--hidden-import matplotlib.backends.backend_qt5agg ^
--hidden-import matplotlib.backends.backend_qtagg ^
--hidden-import PyQt6 ^
--hidden-import PyQt6.QtCore ^
--hidden-import PyQt6.QtGui ^
--hidden-import PyQt6.QtWidgets ^
--hidden-import PyQt6.QtPrintSupport ^
--hidden-import reportlab ^
--hidden-import reportlab.pdfgen ^
--hidden-import reportlab.lib ^
--hidden-import reportlab.platypus ^
--hidden-import bcrypt ^
--hidden-import sqlite3 ^
--hidden-import pandas ^
--hidden-import numpy ^
--hidden-import openpyxl ^
--hidden-import xlsxwriter ^
--hidden-import qrcode ^
--hidden-import fitz ^
--hidden-import app.controllers.client_controller ^
--hidden-import app.controllers.lectura_controller ^
--hidden-import app.controllers.factura_controller ^
--hidden-import app.controllers.consulta_controller ^
--hidden-import app.controllers.recaudacion_controller ^
--hidden-import app.controllers.servicio_controller ^
--hidden-import app.models.client ^
--hidden-import app.models.lectura ^
--hidden-import app.models.factura ^
--hidden-import app.models.servicio ^
--hidden-import app.views.login_window ^
--hidden-import app.views.main_window ^
--hidden-import app.views.clients_widget ^
--hidden-import app.views.lecturas_widget ^
--hidden-import app.views.facturas_widget ^
--hidden-import app.views.datos_recaudacion ^
--hidden-import app.views.consulta_widget ^
--hidden-import app.views.consulta_lecturas_widget ^
--hidden-import app.views.consulta_clientes_widget ^
--hidden-import app.views.servicios_widget ^
--hidden-import app.views.consulta_registros_y_deudas ^
--hidden-import app.database.connection ^
--hidden-import app.database.init_db ^
--hidden-import app.helpers.backup_helper ^
--hidden-import app.helpers.database_migrator ^
--hidden-import app.helpers.logger ^
--hidden-import app.helpers.pdf_generator ^
--hidden-import app.helpers.reporte_generator ^
--exclude-module tkinter ^
--exclude-module IPython ^
--exclude-module jupyter ^
--exclude-module notebook ^
--exclude-module sphinx ^
--exclude-module pytest ^
--exclude-module setuptools ^
--icon "app/resources/CelestineICO.ico" ^
main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Fallo la compilacion.
    pause
    exit /b 1
)

echo.
echo [4/4] Verificando ejecutable generado...
if exist "dist\Celestine.exe" (
    echo.
    echo ========================================
    echo [OK] Compilacion exitosa!
    echo ========================================
    echo.
    echo Ejecutable: dist\Celestine.exe
    for %%A in ("dist\Celestine.exe") do echo Tamano: %%~zA bytes (aprox. %%~zA / 1048576 MB^)
    echo.
    echo IMPORTANTE:
    echo - El ejecutable NO incluye la base de datos
    echo - Copie Celestine.exe JUNTO a sistema_facturacion.db
    echo - Ambos archivos deben estar en la MISMA carpeta
    echo - Las facturas se guardaran correctamente
    echo.
    echo ESTRUCTURA CORRECTA:
    echo   C:\Facturacion\
    echo     - Celestine.exe
    echo     - sistema_facturacion.db
    echo.
    echo Correcciones aplicadas:
    echo   [OK] PIL/Pillow incluido
    echo   [OK] matplotlib incluido
    echo   [OK] Rutas de BD corregidas (absolutas)
    echo   [OK] Facturas se guardan correctamente
    echo   [OK] Sin emojis Unicode
    echo.
    echo ========================================
) else (
    echo.
    echo [ERROR] No se encontro el ejecutable generado.
    pause
    exit /b 1
)

echo.
echo Presione cualquier tecla para salir...
pause >nul
