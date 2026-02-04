import sqlite3
import bcrypt
from datetime import datetime

# Conectar a la base de datos SQLite
db_path = "sistema_facturacion.db"  # Ajusta la ruta según corresponda
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Datos del nuevo usuario
nombre = "RecaudadorRCH"
usuario = "recaudadorRCH"
password = "calicanto2025"
rol_id = 6  # Ajusta según el rol correspondiente
estado = 1  # 1 significa usuario activo
fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual

# Hashear la contraseña con bcrypt
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Insertar el usuario en la base de datos
query = """
INSERT INTO usuarios (nombre, usuario, password, rol_id, estado, fecha_creacion)
VALUES (?, ?, ?, ?, ?, ?)
"""
cursor.execute(query, (nombre, usuario, hashed_password, rol_id, estado, fecha_creacion))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Usuario insertado correctamente.")
