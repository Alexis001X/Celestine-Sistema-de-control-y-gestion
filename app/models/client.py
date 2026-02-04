# app/models/client.py

from datetime import datetime

class Client:
    def __init__(self,id, cliente_ci, nombre_cliente, direccion, telefono, email, numero_conexion,estado=1, fecha_registro=None):
        self.id = id
        self.cliente_ci = cliente_ci
        self.nombre = nombre_cliente
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.numero_conexion = numero_conexion
        self.estado = estado
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()