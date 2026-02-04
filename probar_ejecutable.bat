@echo off
REM ========================================
REM Script para probar el ejecutable compilado
REM ========================================

echo.
echo ============================================================
echo   PRUEBA DEL EJECUTABLE CELESTINE
echo ============================================================
echo.

REM Verificar que existe el ejecutable
if not exist "dist\Celestine.exe" (
    echo [ERROR] No se encuentra dist\Celestine.exe
    echo.
    echo Primero debes compilar el ejecutable con build_installer.bat
    echo.
    pause
    exit /b 1
)

echo [OK] Ejecutable encontrado
echo.

REM Crear carpeta temporal para pruebas
echo Creando carpeta temporal de pruebas...
set TEST_DIR=test_ejecutable_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TEST_DIR=%TEST_DIR: =0%
mkdir "%TEST_DIR%" 2>nul

echo [OK] Carpeta de pruebas: %TEST_DIR%
echo.

REM Copiar ejecutable
echo Copiando ejecutable a carpeta de pruebas...
copy "dist\Celestine.exe" "%TEST_DIR%\" >nul
echo [OK] Ejecutable copiado
echo.

echo ============================================================
echo   INICIANDO PRUEBA
echo ============================================================
echo.
echo Se abrira el ejecutable. Verifica que:
echo.
echo 1. No aparezcan errores de modulos faltantes
echo 2. Se creen las carpetas: logs/, facturas_pdf/, reportes/
echo 3. Se cree la base de datos: sistema_facturacion.db
echo 4. Aparezca la ventana de login
echo 5. Puedas navegar por la interfaz
echo.
echo Presiona cualquier tecla para iniciar la prueba...
pause >nul

REM Ejecutar el programa
cd "%TEST_DIR%"
start Celestine.exe

echo.
echo El ejecutable se esta ejecutando...
echo.
echo Cuando termines de probar, presiona cualquier tecla aqui
echo para ver los archivos generados.
pause >nul

echo.
echo ============================================================
echo   ARCHIVOS GENERADOS
echo ============================================================
echo.
dir /b

echo.
echo ============================================================
echo   LOGS GENERADOS
echo ============================================================
echo.
if exist "logs" (
    echo Carpeta logs/:
    dir /b logs
) else (
    echo [ADVERTENCIA] No se creo la carpeta logs/
)

echo.
echo ============================================================
echo   BASE DE DATOS
echo ============================================================
echo.
if exist "sistema_facturacion.db" (
    echo [OK] Base de datos creada: sistema_facturacion.db
    echo Tamano:
    dir sistema_facturacion.db | find ".db"
) else (
    echo [ADVERTENCIA] No se creo la base de datos
)

echo.
echo ============================================================
echo   FIN DE LA PRUEBA
echo ============================================================
echo.
echo Carpeta de prueba: %CD%
echo.
echo Si todo funciono correctamente, puedes:
echo 1. Proceder a copiar Celestine.exe al equipo destino
echo 2. Eliminar esta carpeta de prueba si deseas
echo.

cd ..
pause
