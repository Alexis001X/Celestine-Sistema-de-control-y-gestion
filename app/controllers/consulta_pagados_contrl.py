# app/controllers/consulta_registros_y_deudas_controller.py
from app.models.consulta_pagados import ConsultaRegistrosYDeudasModel

class ConsultaRegistrosYDeudasController:
    def __init__(self, db_path):
        self.model = ConsultaRegistrosYDeudasModel(db_path)

    def buscar_pagados(self, mes_facturacion, direccion):
        """Llama al modelo para obtener la lista de usuarios con facturas registradas en un mes."""
        return self.model.obtener_pagados(mes_facturacion, direccion)

    def buscar_deudores(self, mes_facturacion, direccion):
        """Llama al modelo para obtener la lista de usuarios que no han registrado factura en un mes."""
        return self.model.obtener_deudores(mes_facturacion, direccion)
    
    def buscar_deudores_por_totales(self, direccion):
        """Obtiene los clientes con al menos 1 factura en estado 'Deuda'."""
        return self.model.mostrar_deudores_por_totales(direccion)  # 🔹 Agregamos este método
