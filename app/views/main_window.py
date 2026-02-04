from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QStackedWidget, QMessageBox
)
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication
from app.views.clients_widget import ClientsWidget
from app.views.lecturas_widget import LecturasWidget
from app.views.facturas_widget import FacturasWidget
from app.views.consulta_widget import ConsultaWidget
from app.views.lecturacon_widget import ConsultaLecturasWidget
from app.views.consulta_clientes import ConsultaClientesWidget
from app.views.consulta_pagados_vw import ConsultaRegistrosYDeudas
from app.views.datos_recaudacion import DatosRecaudacion
from app.views.servicios_widget import ServiciosWidget
from app.helpers.sistema_logs import get_logger


class MainWindow(QMainWindow):
    def __init__(self, user_data, db_path):
        super().__init__()
        self.user_data = user_data
        self.db_path = db_path
        self.app = QApplication.instance()
        self.init_ui()
        
    def init_ui(self):
        icon_path = self.app.get_resource_path("app/resources/CelestineICO.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Sistema de Facturación - Celestine V 1.2.0")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 4)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_left_panel(self):
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout()

        system_name = QLabel("Celestine V.1.2.0")
        system_name.setObjectName("systemName")
        system_name.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        system_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(system_name)

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        left_layout.addWidget(separator)

        menu_buttons = [
            ("Datos de Recaudación", "home", self.show_home),
            ("Usuarios", "clients", self.show_clients),
            ("Lecturas", "lecturas", self.show_lecturas),
            ("Facturación", "billing", self.show_billing),
            ("Consulta facturas", "request", self.show_request),
            ("Consultar Lecturas", "queries", self.show_queries),
            ("Consultar Usuarios", "list", self.show_list),
            ("Consulta Pagados", "pagados", self.show_pagados),
            ("Servicios", "servicios", self.show_servicios),
        ]

        for text, icon_name, callback in menu_buttons:
            button = QPushButton(text)
            button.setObjectName("menuButton")
            button.clicked.connect(callback)
            left_layout.addWidget(button)

        left_layout.addStretch()

        user_frame = QFrame()
        user_frame.setObjectName("userFrame")
        user_layout = QVBoxLayout()

        user_name = QLabel(self.user_data['name'])
        user_name.setObjectName("userName")
        user_layout.addWidget(user_name)

        user_role = QLabel(self.user_data['role'])
        user_role.setObjectName("userRole")
        user_layout.addWidget(user_role)

        logout_button = QPushButton("Cerrar sesión")
        logout_button.setObjectName("logoutButton")
        logout_button.clicked.connect(self.logout)
        user_layout.addWidget(logout_button)

        user_frame.setLayout(user_layout)
        left_layout.addWidget(user_frame)

        left_panel.setLayout(left_layout)
        return left_panel

    def create_right_panel(self):
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout()

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")

        # Agregar widgets al QStackedWidget
        self.datos_recaudacion_widget = DatosRecaudacion(self.db_path)
        self.clients_widget = ClientsWidget(self.user_data)
        self.lecturas_widget = LecturasWidget(self.db_path, self.user_data)
        self.facturas_widget = FacturasWidget(self.db_path, self)
        self.consulta_widget = ConsultaWidget(self.db_path, self)
        self.consulta_lecturas_widget = ConsultaLecturasWidget(self.db_path)
        self.consulta_clientes_widget = ConsultaClientesWidget(self.db_path)
        self.consulta_pagados_widget = ConsultaRegistrosYDeudas(self.db_path)
        self.servicios_widget = ServiciosWidget(self.db_path)
        self.content_stack.addWidget(self.datos_recaudacion_widget)
        self.content_stack.addWidget(self.clients_widget)
        self.content_stack.addWidget(self.lecturas_widget)
        self.content_stack.addWidget(self.facturas_widget)
        self.content_stack.addWidget(self.consulta_widget)
        self.content_stack.addWidget(self.consulta_lecturas_widget)
        self.content_stack.addWidget(self.consulta_clientes_widget)
        self.content_stack.addWidget(self.consulta_pagados_widget)
        self.content_stack.addWidget(self.servicios_widget)

        right_layout.addWidget(self.content_stack)
        right_panel.setLayout(right_layout)

        return right_panel
        
        
    def show_home(self):
        self.content_stack.setCurrentWidget(self.datos_recaudacion_widget)

    def show_clients(self):
        self.content_stack.setCurrentWidget(self.clients_widget)

    def show_lecturas(self):
        self.content_stack.setCurrentWidget(self.lecturas_widget)

    def show_billing(self):
        self.content_stack.setCurrentWidget(self.facturas_widget)

    def show_request(self):
        self.content_stack.setCurrentWidget(self.consulta_widget)
        
    def show_queries(self):
        self.content_stack.setCurrentWidget(self.consulta_lecturas_widget)
        
    def show_list(self):
        self.content_stack.setCurrentWidget(self.consulta_clientes_widget)
        
        
    def show_pagados(self):
        self.content_stack.setCurrentWidget(self.consulta_pagados_widget)

    def show_servicios(self):
        self.content_stack.setCurrentWidget(self.servicios_widget)


    def logout(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Cerrar sesión")
        message_box.setText("¿Está seguro de que desea cerrar sesión?")

        # Crear botones personalizados
        button_yes = message_box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        button_no = message_box.addButton("No", QMessageBox.ButtonRole.NoRole)

        # Mostrar el cuadro de diálogo
        message_box.exec()

        # Verificar qué botón fue presionado
        if message_box.clickedButton() == button_yes:
            # Registrar logout en el log
            logger = get_logger()
            logger.log_logout(self.user_data['name'], self.user_data['role'])

            self.close()
