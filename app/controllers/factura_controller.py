import sqlite3
from app.models.factura import FacturaModel

class FacturaController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.model = FacturaModel(db_path)

    def obtener_cliente_por_id(self, medidor_id):
        """Obtiene el nombre y la cédula del cliente por su ID."""
        try:
            query = "SELECT nombre_cliente, cliente_ci FROM clientes WHERE id = ?"
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, (medidor_id,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return {"nombre_cliente": resultado[0], "cliente_ci": resultado[1]}  # Devuelve ambos datos
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener cliente: {e}")
            return None


    def obtener_lectura_por_cliente_id(self, medidor_id):
        """Obtiene la lectura más reciente, consumo y dirección de un cliente por su ID."""
        try:
            query = """
                SELECT id, consumo, direccion
                FROM lecturas
                WHERE medidor_id = ?
                ORDER BY fecha_lectura DESC
                LIMIT 1
            """
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, (medidor_id,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return {
                    "id": resultado[0],
                    "consumo": resultado[1],
                    "direccion": resultado[2] if resultado[2] else ""
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener lectura: {e}")
            return None

    def calcular_montos(self, consumo, tarifa_basica_index, tarifa_excedente_index):
        """Calcula los montos básico, excedente y total."""
        try:
            tarifa_basica_rangos = [(10, 1.50), (50, 2.00), (100, 3.00), (101, 3.00)]
            tarifa_excedente_rangos = [(10, 0.30), (25, 0.40), (50, 0.50), (101, 0.75)]

            # Rango y tarifa básica seleccionados
            rango_basico = tarifa_basica_rangos[tarifa_basica_index]
            tarifa_basica_fija = rango_basico[1]

            # Rango y tarifa excedente seleccionados
            rango_excedente = tarifa_excedente_rangos[tarifa_excedente_index]
            tarifa_excedente_por_unidad = rango_excedente[1]

            # Calcular consumo excedente (restar siempre 10 como constante)
            consumo_excedente = max(consumo - 10, 0)

            if consumo_excedente <= 0:
                return {
                    "monto_basico": tarifa_basica_fija,
                    "monto_excedente": 0.0,
                    "monto_total": tarifa_basica_fija
                }

            monto_basico = tarifa_basica_fija
            monto_excedente = consumo_excedente * tarifa_excedente_por_unidad
            monto_total = monto_basico + monto_excedente

            return {
                "monto_basico": monto_basico,
                "monto_excedente": monto_excedente,
                "monto_total": monto_total
            }
        except Exception as e:
            print(f"Error al calcular montos: {e}")
            return {"monto_basico": 0, "monto_excedente": 0, "monto_total": 0}

    def registrar_factura(self, datos):
        """Valida los datos y envía la solicitud de registro al modelo."""
        if any(dato == "" or dato is None for dato in datos):
            return False, "Todos los campos son obligatorios."

        exito = self.model.registrar_factura(datos)
        if exito:
            return True, "Factura registrada exitosamente."
        else:
            return False, "Error al registrar la factura. Intente nuevamente."
