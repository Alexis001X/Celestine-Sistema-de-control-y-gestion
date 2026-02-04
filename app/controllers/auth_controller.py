# app/controllers/auth_controller.py
import bcrypt
from app.database.connection import DatabaseConnection

class AuthController:
    @staticmethod
    def login(username, password):
        db = DatabaseConnection()
        conn = db.connect()
        
        if conn is None:
            return None

        # Consulta para obtener el usuario y su contraseña hasheada
        query = """
        SELECT u.id, u.usuario, u.nombre, u.password, r.nombre as rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        WHERE u.usuario = ? AND u.estado = 1
        """
        
        # Ejecutar la consulta
        user = db.fetch_one(query, (username,))
        db.close()
        
        if user:
            stored_hashed_password = user['password'].encode()  # Convertir a bytes
            if bcrypt.checkpw(password.encode(), stored_hashed_password):  # Comparar contraseñas
                return {
                    "id": user['id'],
                    "username": user['usuario'],
                    "name": user['nombre'],
                    "role": user['rol']
                }
        
        return None
