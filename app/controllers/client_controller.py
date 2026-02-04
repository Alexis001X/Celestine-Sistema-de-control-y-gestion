# app/controllers/client_controller.py
import sqlite3
from app.models.client import Client
from app.database.connection import get_db_connection


class ClientController:
    def __init__(self):
        self.conn = get_db_connection()

    def create_client(self, client_data):
        """
        Crea un nuevo cliente con los datos proporcionados.
        """
        client = Client(**client_data)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client.id, client.nombre ,client.cliente_ci, client.direccion, client.telefono, client.email, client.numero_conexion, client.estado))
        self.conn.commit()

    def validate_client_data(self, client_data):
        """
        Valida que todos los campos del formulario estén llenos.
        Retorna True si todos los campos están completos, de lo contrario, False.
        """
        required_fields = ["id", "cliente_ci", "nombre_cliente", "direccion", "telefono", "email", "numero_conexion"]
        for field in required_fields:
            if not client_data.get(field):
                return False, f"El campo '{field}' es obligatorio."
        return True, "Todos los campos están completos."

    def get_client_by_unique_fields(self, cliente_ci, email, numero_conexion):
        """
        Busca clientes que tengan valores duplicados en los campos únicos.
        """
        query = """
            SELECT * FROM clientes
            WHERE cliente_ci = ? OR email = ? OR numero_conexion = ?
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (cliente_ci, email, numero_conexion))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Error al buscar cliente por campos únicos: {e}")
            return None

    def get_clients(self, page=1, page_size=10):
        cursor = self.conn.cursor()
        offset = (page - 1) * page_size
        cursor.execute("""
            SELECT id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion, estado, fecha_registro
            FROM clientes
            ORDER BY fecha_registro DESC
            LIMIT ? OFFSET ?
        """, (page_size, offset))
        return [dict(zip(["id", "nombre_cliente", "cliente_ci", "direccion", "telefono", "email", "numero_conexion", "estado", "fecha_registro"], row)) for row in cursor.fetchall()]

    def get_total_pages(self, page_size):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clients = cursor.fetchone()[0]
        return (total_clients + page_size - 1) // page_size

    def search_clients(self, search_term):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion, estado, fecha_registro
            FROM clientes
            WHERE nombre_cliente LIKE ? OR cliente_ci LIKE ? OR numero_conexion LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        return [dict(zip(["id", "nombre_cliente", "cliente_ci", "direccion", "telefono", "email", "numero_conexion", "estado", "fecha_registro"], row)) for row in cursor.fetchall()]

    def update_client(self, client_id, client_data):
        """
        Actualiza un cliente existente con los datos proporcionados.
        """
        client = Client(**client_data)
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre_cliente = ?, cliente_ci = ?, direccion = ?, telefono = ?, email = ?, numero_conexion = ?, estado = ?
            WHERE id = ?
        """, (client.nombre, client.cliente_ci, client.direccion, client.telefono, client.email, client.numero_conexion, client.estado, client_id))
        self.conn.commit()

    def delete_client(self, client_id):
        """
        Elimina un cliente basado en su ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
        self.conn.commit()

    def get_client_by_id(self, client_id):
        """
        Obtiene un cliente basado en su ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion, estado, fecha_registro
            FROM clientes
            WHERE id = ?
        """, (client_id,))
        row = cursor.fetchone()
        if row:
            return dict(zip(["id", "nombre_cliente", "cliente_ci", "direccion", "telefono", "email", "numero_conexion", "estado", "fecha_registro"], row))
        return None

    def __del__(self):
        """
        Cierra la conexión a la base de datos al destruir la instancia.
        """
        self.conn.close()
