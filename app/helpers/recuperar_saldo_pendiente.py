import sqlite3
import time

class SaldoPendienteHelper:
    def __init__(self, db_path):
        self.db_path = db_path

    def obtener_saldo_pendiente(self, medidor_id):
        """Busca facturas con estado 'Deuda' y suma sus montos."""
        try:
            conn_saldo = sqlite3.connect(self.db_path)
            cursor_saldo = conn_saldo.cursor()

            query_saldo = """
                SELECT id, monto_total FROM facturas 
                WHERE medidor_id = ? AND estado = 'Deuda'
            """
            cursor_saldo.execute(query_saldo, (medidor_id,))
            facturas_deuda = cursor_saldo.fetchall()

            saldo_pendiente = sum(factura[1] for factura in facturas_deuda) if facturas_deuda else 0.00

            conn_saldo.close()
            return saldo_pendiente
        except sqlite3.Error as e:
            print(f"Error al recuperar saldo pendiente: {e}")
            return 0.00
