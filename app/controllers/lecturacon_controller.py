from app.models.lecturacon_model import LecturaModel

class LecturaController:
    def __init__(self, db_path):
        self.model = LecturaModel(db_path)

    def obtener_lecturas(self, filtros=None):
        """Obtiene lecturas desde el modelo con filtros."""
        return self.model.obtener_lecturas(filtros)
