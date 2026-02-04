# app/database/connection.py
import sqlite3
from sqlite3 import Error
import os
import sys

class DatabaseConnection:
    _instance = None
    _db_path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.conn = None
        return cls._instance

    @classmethod
    def set_db_path(cls, db_path):
        """Establece la ruta de la base de datos para el singleton"""
        cls._db_path = db_path
        print(f"[DEBUG] DatabaseConnection.set_db_path establecido a: {db_path}")

    @classmethod
    def get_db_path(cls):
        """Obtiene la ruta de la base de datos"""
        if cls._db_path is None:
            # Si no se ha establecido, usar la ruta correcta segun el entorno
            if getattr(sys, 'frozen', False):
                # Ejecutable
                cls._db_path = os.path.join(os.path.dirname(sys.executable), 'sistema_facturacion.db')
            else:
                # Desarrollo
                cls._db_path = os.path.join(os.getcwd(), 'sistema_facturacion.db')
            print(f"[DEBUG] DatabaseConnection.get_db_path auto-detectado: {cls._db_path}")
        return cls._db_path

    def connect(self):
        try:
            # SIEMPRE obtener la ruta actual (no cachear)
            # Esto permite cambiar de BD sin reiniciar
            db_file = self.__class__.get_db_path()

            # Cerrar conexion anterior si existe
            if self.conn:
                try:
                    self.conn.close()
                    print(f"[DEBUG] Conexion anterior cerrada")
                except:
                    pass

            # Crear nueva conexion
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
            print(f"[DEBUG] Conexion establecida a: {db_file}")
            return self.conn
        except Error as e:
            print(f"[ERROR] Error al conectar a SQLite: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, parameters=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, parameters)
            self.conn.commit()
            return cursor
        except Error as e:
            print(f"[ERROR] Error al ejecutar la consulta: {e}")
            return None

    def fetch_all(self, query, parameters=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
        except Error as e:
            print(f"[ERROR] Error al obtener datos: {e}")
            return []

    def fetch_one(self, query, parameters=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchone()
        except Error as e:
            print(f"[ERROR] Error al obtener dato: {e}")
            return None

# Función para obtener la conexión a la base de datos
def get_db_connection():
    db = DatabaseConnection()
    connection = db.connect()
    return connection