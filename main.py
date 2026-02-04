# main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from app.views.login_window import LoginWindow
from app.views.main_window import MainWindow
from app.helpers.database_migrator import ejecutar_migraciones

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.base_path = self.get_base_path()
        self.setup_directories()

        # CRITICO: Establecer db_path en el singleton ANTES de cualquier operacion
        from app.database.connection import DatabaseConnection
        db_path = self.get_db_path()
        DatabaseConnection.set_db_path(db_path)
        print(f"[INIT] Base de datos establecida en: {db_path}")

        # IMPORTANTE: Ejecutar migraciones de base de datos ANTES de cargar la UI
        self.run_database_migrations()

        self.load_stylesheet()
        self.login_window = LoginWindow()
        self.main_window = None

        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()
    
    def get_base_path(self):
        """Obtiene la ruta base de la aplicación"""
        if getattr(sys, 'frozen', False):
            # Ejecutable
            return sys._MEIPASS
        # Código fuente
        return os.path.dirname(os.path.abspath(__file__))
    
    def get_output_path(self):
        """Obtiene la ruta para archivos de salida"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return self.base_path

    def setup_directories(self):
        """Configura las carpetas necesarias para la aplicación"""
        output_path = self.get_output_path()

        # Crear directorios para archivos generados
        self.facturas_path = os.path.join(output_path, 'facturas_pdf')
        self.reportes_path = os.path.join(output_path, 'reportes')
        self.logs_path = os.path.join(output_path, 'logs')

        # Asegurar que existan los directorios
        os.makedirs(self.facturas_path, exist_ok=True)
        os.makedirs(self.reportes_path, exist_ok=True)
        os.makedirs(self.logs_path, exist_ok=True)

    def run_database_migrations(self):
        """Ejecuta las migraciones de base de datos al iniciar la aplicación"""
        db_path = self.get_db_path()
        print(f"\n{'='*60}")
        print(f"Verificando base de datos: {db_path}")
        print(f"{'='*60}\n")

        try:
            ejecutar_migraciones(db_path)
        except Exception as e:
            print(f"\n[ADVERTENCIA] Error durante las migraciones: {e}")
            print("La aplicacion continuara, pero algunas funciones pueden no estar disponibles.\n")

    def get_db_path(self):
        """
        Obtiene la ruta de la base de datos con soporte para multiples fuentes.

        PRIORIDAD DE BUSQUEDA:
        1. Argumento de linea de comandos: Celestine.exe "C:\ruta\a\mi_bd.db"
        2. Archivo config.txt junto al ejecutable
        3. Archivo importar_bd.db junto al ejecutable (se migrara automaticamente)
        4. sistema_facturacion.db en la carpeta del ejecutable (default)
        """
        # PRIORIDAD 1: Argumento de linea de comandos
        if len(sys.argv) > 1:
            custom_db = sys.argv[1]
            if os.path.exists(custom_db) and custom_db.endswith('.db'):
                print(f"[INIT] Usando BD desde parametro CLI: {custom_db}")
                return custom_db
            else:
                print(f"[WARN] BD especificada no existe o no es valida: {custom_db}")
                print(f"[WARN] Se usara la BD por defecto")

        # PRIORIDAD 2: Archivo de configuracion config.txt
        if getattr(sys, 'frozen', False):
            config_file = os.path.join(os.path.dirname(sys.executable), 'config.txt')
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        db_from_config = f.read().strip()
                        if os.path.exists(db_from_config) and db_from_config.endswith('.db'):
                            print(f"[INIT] Usando BD desde config.txt: {db_from_config}")
                            return db_from_config
                        else:
                            print(f"[WARN] BD en config.txt no existe: {db_from_config}")
                except Exception as e:
                    print(f"[WARN] Error al leer config.txt: {e}")

        # PRIORIDAD 3: Verificar si hay BD para importar (importar_bd.db)
        if getattr(sys, 'frozen', False):
            from app.helpers.database_migrator import verificar_bd_importar
            exe_dir = os.path.dirname(sys.executable)
            bd_importar = os.path.join(exe_dir, 'importar_bd.db')

            if os.path.exists(bd_importar):
                # verificar_bd_importar() se encarga de migrar y devolver ruta correcta
                return verificar_bd_importar(exe_dir)

        # PRIORIDAD 4: BD por defecto en carpeta del ejecutable
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), 'sistema_facturacion.db')
        return os.path.join(self.base_path, 'sistema_facturacion.db')
    
    def get_resource_path(self, relative_path):
        """Obtiene la ruta absoluta para cualquier recurso"""
        return os.path.join(self.base_path, relative_path)

    def on_login_successful(self, user_data):
        self.login_window.close()
        db_path = self.get_db_path()
        self.main_window = MainWindow(user_data, db_path)
        self.main_window.show()

    def load_stylesheet(self):
        style_file_path = self.get_resource_path(os.path.join("app", "resources", "styles.qss"))
        file = QFile(style_file_path)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())

def main():
    app = App(sys.argv)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()