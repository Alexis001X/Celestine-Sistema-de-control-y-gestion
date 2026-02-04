@echo off
REM ========================================
REM Script de Compilacion - Celestine V.1.2.0
REM Sistema de Facturacion de Agua
REM ========================================

echo.
echo ============================================================
echo   COMPILADOR DE CELESTINE V.1.2.0
echo   Sistema de Facturacion de Agua
echo ============================================================
echo.

REM Verificar que PyInstaller esta instalado
echo Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller no esta instalado
    echo.
    echo Instalando PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller encontrado
echo.

REM Verificar e instalar dependencias
echo Verificando e instalando dependencias...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

REM Verificar dependencias críticas
echo Verificando dependencias criticas...
python verificar_dependencias.py
if errorlevel 1 (
    echo [ERROR] Faltan dependencias criticas
    echo Ejecute: pip install -r requirements.txt
    pause
    exit /b 1
)
echo.

REM Limpiar compilaciones anteriores
echo Limpiando compilaciones anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo [OK] Limpieza completada
echo.

REM Compilar con PyInstaller
echo ============================================================
echo   INICIANDO COMPILACION...
echo ============================================================
echo.

pyinstaller Celestine.spec

if errorlevel 1 (
    echo.
    echo ============================================================
    echo   [ERROR] La compilacion fallo
    echo ============================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   [EXITO] Compilacion completada
echo ============================================================
echo.
echo El ejecutable se encuentra en: dist\Celestine.exe
echo.

REM Crear carpeta de distribucion
echo Creando paquete de distribucion...
if not exist "Celestine_Instalacion" mkdir "Celestine_Instalacion"

REM Copiar ejecutable
copy "dist\Celestine.exe" "Celestine_Instalacion\" >nul

REM Crear archivo de instrucciones
echo Creando instrucciones de instalacion...
(
echo ========================================
echo INSTRUCCIONES DE INSTALACION
echo Celestine V.1.2.0
echo ========================================
echo.
echo INSTALACION NUEVA:
echo 1. Copie Celestine.exe a una carpeta de su eleccion
echo 2. Ejecute Celestine.exe
echo 3. El sistema creara automaticamente:
echo    - Base de datos
echo    - Carpetas necesarias
echo    - Tablas y secuencias
echo.
echo ACTUALIZACION (CON BASE DE DATOS EXISTENTE):
echo 1. HAGA BACKUP de sistema_facturacion.db
echo 2. Copie Celestine.exe a la carpeta con la base de datos
echo 3. Ejecute Celestine.exe
echo 4. El sistema actualizara automaticamente:
echo    - Campo numero_factura en tabla facturas
echo    - Tabla secuencias_facturacion
echo    - Secuencia 001-010 (nueva numeracion^)
echo.
echo IMPORTANTE:
echo - Las facturas antiguas NO se veran afectadas
echo - La nueva numeracion comienza desde 001-010-0000000001
echo - Al editar facturas antiguas, mantienen su numero original
echo.
echo CARPETAS QUE SE CREAN AUTOMATICAMENTE:
echo - logs/         (registros del sistema, se auto-limpian cada 5 dias^)
echo - facturas_pdf/ (PDFs de facturas generadas^)
echo - reportes/     (reportes del sistema^)
echo.
echo SOPORTE:
echo - Consulte BUILD.md para informacion detallada
echo - Logs del sistema en: logs/log_[FECHA].txt
echo.
echo Celestine V.1.2.0 - Sistema de Facturacion de Agua
echo ========================================
) > "Celestine_Instalacion\INSTRUCCIONES_INSTALACION.txt"

REM Copiar documentacion
if exist "BUILD.md" copy "BUILD.md" "Celestine_Instalacion\" >nul
if exist "README.md" copy "README.md" "Celestine_Instalacion\" >nul

echo [OK] Paquete de distribucion creado
echo.

REM Crear archivo de informacion
(
echo Celestine V.1.2.0
echo Sistema de Facturacion de Agua
echo.
echo CONTENIDO DE ESTE PAQUETE:
echo.
echo Celestine.exe - Ejecutable principal
echo INSTRUCCIONES_INSTALACION.txt - Guia de instalacion
echo BUILD.md - Documentacion tecnica completa
echo.
echo CARACTERISTICAS NUEVAS EN ESTA VERSION:
echo - Nueva secuencia de numeracion 001-010
echo - Sistema de edicion y reimpresion de facturas
echo - Logs automaticos de acciones de usuario
echo - Migraciones automaticas de base de datos
echo.
echo COMPATIBILIDAD:
echo - Windows 7 o superior
echo - No requiere Python instalado
echo - Compatible con bases de datos existentes
echo.
echo Para instalar, consulte INSTRUCCIONES_INSTALACION.txt
) > "Celestine_Instalacion\README.txt"

echo.
echo ============================================================
echo   PAQUETE DE INSTALACION LISTO
echo ============================================================
echo.
echo Ubicacion: Celestine_Instalacion\
echo.
echo Contenido:
echo   - Celestine.exe
echo   - INSTRUCCIONES_INSTALACION.txt
echo   - README.txt
echo   - BUILD.md
echo.
echo Ya puede copiar la carpeta Celestine_Instalacion
echo al equipo donde desea instalar el sistema.
echo.

REM Abrir carpeta de distribucion
explorer "Celestine_Instalacion"

pause
