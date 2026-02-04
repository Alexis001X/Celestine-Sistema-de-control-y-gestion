"""
Script para verificar que todas las dependencias críticas estén instaladas
antes de compilar el ejecutable.
"""

import sys
import importlib

DEPENDENCIAS_CRITICAS = [
    ('PyQt6', 'PyQt6.QtCore'),
    ('PyQt6.QtGui', 'PyQt6.QtGui'),
    ('PyQt6.QtWidgets', 'PyQt6.QtWidgets'),
    ('PIL', 'PIL.Image'),
    ('reportlab', 'reportlab.pdfgen'),
    ('bcrypt', 'bcrypt'),
    ('sqlite3', 'sqlite3'),
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
    ('openpyxl', 'openpyxl'),
    ('qrcode', 'qrcode'),
    ('fitz (PyMuPDF)', 'fitz'),
    ('matplotlib', 'matplotlib.figure'),
]

def verificar_modulo(nombre_mostrar, nombre_importar):
    """Verifica si un módulo está instalado."""
    try:
        importlib.import_module(nombre_importar)
        print(f"[OK] {nombre_mostrar:25} - Instalado")
        return True
    except ImportError as e:
        print(f"[FALTA] {nombre_mostrar:25} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN DE DEPENDENCIAS CRÍTICAS")
    print("=" * 60)
    print()

    todos_ok = True
    for nombre_mostrar, nombre_importar in DEPENDENCIAS_CRITICAS:
        if not verificar_modulo(nombre_mostrar, nombre_importar):
            todos_ok = False

    print()
    print("=" * 60)
    if todos_ok:
        print("[EXITO] TODAS LAS DEPENDENCIAS ESTAN INSTALADAS")
        print("        Puedes proceder a compilar el ejecutable")
    else:
        print("[ERROR] FALTAN DEPENDENCIAS")
        print("        Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
