import sqlite3


def agregar_campo_numero_factura(db_path="sistema_facturacion.db"):
    """
    Agrega el campo 'numero_factura' a la tabla facturas si no existe.

    Este campo almacenará el número de factura formateado (ej: 001-010-0000000001)
    para poder mantener la trazabilidad y permitir ediciones sin perder el número.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(facturas)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if "numero_factura" not in columnas:
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN numero_factura TEXT
            """)

            conn.commit()
            print("✅ Campo 'numero_factura' agregado exitosamente a la tabla facturas")

            # Migrar facturas antiguas (opcional)
            # Las facturas antiguas tendrán NULL en numero_factura
            # Podríamos generarles un número basado en el formato antiguo si se desea
            cursor.execute("SELECT COUNT(*) FROM facturas WHERE numero_factura IS NULL")
            facturas_antiguas = cursor.fetchone()[0]

            if facturas_antiguas > 0:
                print(f"ℹ️  Hay {facturas_antiguas} facturas antiguas sin número de factura")
                print("   Estas facturas mantendrán NULL hasta que sean editadas o reimpresas")

        else:
            print("ℹ️  El campo 'numero_factura' ya existe en la tabla facturas")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Error al agregar campo numero_factura: {e}")


def migrar_facturas_antiguas_formato_001_001(db_path="sistema_facturacion.db"):
    """
    Migra las facturas antiguas asignándoles un número en formato 001-001-XXXXXXXXX
    basado en su ID.

    Esta función es opcional y solo debe ejecutarse si se desea asignar números
    a las facturas antiguas que tienen numero_factura NULL.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener todas las facturas sin número de factura
        cursor.execute("SELECT id FROM facturas WHERE numero_factura IS NULL")
        facturas_sin_numero = cursor.fetchall()

        if not facturas_sin_numero:
            print("ℹ️  No hay facturas antiguas para migrar")
            conn.close()
            return

        print(f"🔄 Migrando {len(facturas_sin_numero)} facturas antiguas...")

        for factura in facturas_sin_numero:
            factura_id = factura[0]
            # Generar número en formato antiguo 001-001-XXXXXXXXX
            numero_antiguo = f"001-001-{factura_id:09d}"

            cursor.execute("""
                UPDATE facturas
                SET numero_factura = ?
                WHERE id = ?
            """, (numero_antiguo, factura_id))

        conn.commit()
        print(f"✅ {len(facturas_sin_numero)} facturas antiguas migradas exitosamente")
        print("   Formato usado: 001-001-XXXXXXXXX")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Error al migrar facturas antiguas: {e}")


if __name__ == "__main__":
    """
    Script de migración para agregar soporte de numeración de facturas.

    Ejecutar este script para:
    1. Agregar el campo numero_factura a la tabla facturas
    2. (Opcional) Migrar facturas antiguas con formato 001-001-XXXXXXXXX
    """
    import sys

    db_path = "sistema_facturacion.db"

    print("=" * 60)
    print("MIGRACIÓN: Sistema de Numeración de Facturas")
    print("=" * 60)
    print()

    # Paso 1: Agregar campo
    print("Paso 1: Agregando campo numero_factura...")
    agregar_campo_numero_factura(db_path)
    print()

    # Paso 2: Preguntar si se desea migrar facturas antiguas
    print("Paso 2: Migración de facturas antiguas")
    print("¿Desea asignar números (formato 001-001-XXXXXXXXX) a las facturas antiguas?")
    print("Esto es opcional. Las facturas sin número se pueden dejar como están.")
    respuesta = input("Migrar facturas antiguas? (s/n): ").lower()

    if respuesta == 's':
        migrar_facturas_antiguas_formato_001_001(db_path)
    else:
        print("ℹ️  Migración de facturas antiguas omitida")

    print()
    print("=" * 60)
    print("✅ Migración completada")
    print("=" * 60)
