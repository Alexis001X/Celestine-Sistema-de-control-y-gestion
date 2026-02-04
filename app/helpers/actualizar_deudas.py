import sqlite3

class ActualizarDeudasHelper:
    def __init__(self, db_path):
        self.db_path = db_path

    def actualizar_facturas_pagadas(self, medidor_id):
        """
        Si la última factura del cliente está en estado 'Pagado',
        actualiza todas las facturas anteriores en estado 'Deuda' a 'Pagado'.
        Retorna un mensaje indicando el resultado de la operación.
        """
        try:
            conn_check = sqlite3.connect(self.db_path)
            cursor_check = conn_check.cursor()

            # Verificamos el estado de la última factura registrada
            cursor_check.execute("""
                SELECT estado FROM facturas 
                WHERE medidor_id = ? 
                ORDER BY id DESC LIMIT 1
            """, (medidor_id,))
            ultima_factura = cursor_check.fetchone()

            if ultima_factura and ultima_factura[0] == "Pagado":
                conn_update = sqlite3.connect(self.db_path)
                cursor_update = conn_update.cursor()

                # Obtenemos el total de facturas en estado "Deuda" antes de actualizar
                cursor_update.execute("""
                    SELECT COUNT(*) FROM facturas 
                    WHERE medidor_id = ? AND estado = 'Deuda'
                """, (medidor_id,))
                total_deudas = cursor_update.fetchone()[0]

                # Actualizamos todas las facturas antiguas en estado "Deuda"
                cursor_update.execute("""
                    UPDATE facturas 
                    SET estado = 'Pagado' 
                    WHERE medidor_id = ? AND estado = 'Deuda'
                """, (medidor_id,))

                filas_actualizadas = cursor_update.rowcount
                conn_update.commit()
                conn_update.close()

                return f"Actualización exitosa: Se han actualizado {filas_actualizadas} facturas de un total de {total_deudas} facturas en estado 'Deuda' a estado 'Pagado'."
            else:
                return "No se pueden actualizar las facturas: La última factura registrada no está en estado 'Pagado'."

            conn_check.close()

        except sqlite3.Error as e:
            return f"Error al actualizar facturas pagadas: {e}"