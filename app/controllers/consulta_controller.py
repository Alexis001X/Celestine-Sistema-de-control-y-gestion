from app.models.consulta_model import ConsultaModel

class ConsultaController:
    def __init__(self, db_path):
        self.model = ConsultaModel(db_path)

    def filtrar_facturas(self, filtros):
        """Valida los filtros y solicita los datos al modelo."""
        return self.model.obtener_facturas(filtros)
        
    def obtener_factura_completa(self, id_factura):
        """Obtiene todos los datos de una factura específica para su reimpresión.
        
        Args:
            id_factura: Identificador único de la factura a reimprimir
            
        Returns:
            Un diccionario con todos los datos de la factura seleccionada
            o None si no se encuentra la factura
        """
        return self.model.obtener_factura_por_id(id_factura)