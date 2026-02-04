class ServicioModel:
    def __init__(self, id_servicio=None, numero_medidor=None, nombre_usuario=None, 
                 direccion_usuario=None, usuario_servicio=None, monto_servicio=None,
                 pago_uno=None, pago_dos=None, pago_tres=None, pago_cuatro=None):
        self.id_servicio = id_servicio
        self.numero_medidor = numero_medidor
        self.nombre_usuario = nombre_usuario
        self.direccion_usuario = direccion_usuario
        self.usuario_servicio = usuario_servicio
        self.monto_servicio = monto_servicio or 0
        self.pago_uno = float(pago_uno) if pago_uno is not None and pago_uno != '' else 0
        self.pago_dos = float(pago_dos) if pago_dos is not None and pago_dos != '' else 0
        self.pago_tres = float(pago_tres) if pago_tres is not None and pago_tres != '' else 0
        self.pago_cuatro = float(pago_cuatro) if pago_cuatro is not None and pago_cuatro != '' else 0

    def to_dict(self):
        """Convierte el modelo a un diccionario."""
        return {
            "id_servicio": self.id_servicio,
            "numero_medidor": self.numero_medidor,
            "nombre_usuario": self.nombre_usuario,
            "direccion_usuario": self.direccion_usuario,
            "usuario_servicio": self.usuario_servicio,
            "monto_servicio": self.monto_servicio,
            "pago_uno": self.pago_uno,
            "pago_dos": self.pago_dos,
            "pago_tres": self.pago_tres,
            "pago_cuatro": self.pago_cuatro
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un modelo a partir de un diccionario."""
        return cls(
            id_servicio=data.get("id_servicio"),
            numero_medidor=data.get("numero_medidor"),
            nombre_usuario=data.get("nombre_usuario"),
            direccion_usuario=data.get("direccion_usuario"),
            usuario_servicio=data.get("usuario_servicio"),
            monto_servicio=data.get("monto_servicio"),
            pago_uno=data.get("pago_uno"),
            pago_dos=data.get("pago_dos"),
            pago_tres=data.get("pago_tres"),
            pago_cuatro=data.get("pago_cuatro")
        )

    def calcular_total_pagado(self):
        """Calcula el total pagado por el servicio."""
        return self.pago_uno + self.pago_dos + self.pago_tres + self.pago_cuatro

    def calcular_saldo_pendiente(self):
        """Calcula el saldo pendiente del servicio."""
        return self.monto_servicio - self.calcular_total_pagado() 