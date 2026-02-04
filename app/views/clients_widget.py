# app/views/clients_widget.py
import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox,
    QGridLayout, QGroupBox, QLabel, QHBoxLayout
)
from app.controllers.client_controller import ClientController
from app.helpers.sistema_logs import get_logger

def resource_path(relative_path):
    """Obtiene la ruta absoluta para recursos empaquetados."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class ClientsWidget(QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.client_controller = ClientController()
        self.user_data = user_data  # Datos del usuario logueado
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica."""
        main_layout = QVBoxLayout()
        
        # Grupo para el formulario de cliente
        client_group = QGroupBox("Datos del Cliente")
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10) # Añadir un poco de espacio entre widgets

        # Campos del formulario
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ej: 12345")
        self.cliente_ci_input = QLineEdit()
        self.cliente_ci_input.setPlaceholderText("Ej: 1700000001")
        self.nombre_cliente_input = QLineEdit()
        self.nombre_cliente_input.setPlaceholderText("Nombre completo del cliente")
        self.direccion_input = QComboBox()
        self.direccion_input.addItems([
            "SANTA ROSA ALTA", "SANTA ROSA BAJA", "LA JOYA", 
            "EL TEJAR", "SANTA ANA", "SAN CRISTOBAL", "CASIGANDA"
        ])
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Ej: 0991234567")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ej: correo@ejemplo.com")
        self.numero_conexion_input = QLineEdit()
        self.numero_conexion_input.setPlaceholderText("Número asignado por la empresa")
        self.estado_input = QComboBox()
        self.estado_input.addItems(["Activo", "Inactivo"])

        # Agregar campos al layout de rejilla
        grid_layout.addWidget(QLabel("Numero de medidor:"), 0, 0)
        grid_layout.addWidget(self.id_input, 0, 1)
        grid_layout.addWidget(QLabel("Cédula:"), 0, 2)
        grid_layout.addWidget(self.cliente_ci_input, 0, 3)

        grid_layout.addWidget(QLabel("Nombres:"), 1, 0)
        grid_layout.addWidget(self.nombre_cliente_input, 1, 1, 1, 3) # Ocupa 3 columnas

        grid_layout.addWidget(QLabel("Dirección:"), 2, 0)
        grid_layout.addWidget(self.direccion_input, 2, 1)
        grid_layout.addWidget(QLabel("Teléfono:"), 2, 2)
        grid_layout.addWidget(self.telefono_input, 2, 3)

        grid_layout.addWidget(QLabel("Email:"), 3, 0)
        grid_layout.addWidget(self.email_input, 3, 1)
        grid_layout.addWidget(QLabel("Número de Conexión:"), 3, 2)
        grid_layout.addWidget(self.numero_conexion_input, 3, 3)

        grid_layout.addWidget(QLabel("Estado:"), 4, 0)
        grid_layout.addWidget(self.estado_input, 4, 1)

        client_group.setLayout(grid_layout)
        main_layout.addWidget(client_group)

        # Layout para botones
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar Cliente") # Texto más descriptivo
        save_button.clicked.connect(self.save_client)
        
        limpiar_button = QPushButton("Limpiar Formulario") # Añadir botón limpiar
        limpiar_button.clicked.connect(self.clear_form) 
        
        button_layout.addStretch() # Empuja los botones a la derecha
        button_layout.addWidget(limpiar_button)
        button_layout.addWidget(save_button)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch() # Añade espacio flexible al final

        self.setLayout(main_layout)

    def save_client(self):
        """Registra un nuevo cliente en la base de datos."""
        client_data = {
            "id": self.id_input.text(),
            "cliente_ci": self.cliente_ci_input.text(),
            "nombre_cliente": self.nombre_cliente_input.text(),
            "direccion": self.direccion_input.currentText(),
            "telefono": self.telefono_input.text(),
            "email": self.email_input.text(),
            "numero_conexion": self.numero_conexion_input.text(),
            "estado": 1 if self.estado_input.currentText() == "Activo" else 0
        }

        # Validación de campos
        is_valid, message = self.client_controller.validate_client_data(client_data)
        if not is_valid:
            QMessageBox.warning(self, "Validación", message)
            return

        # Registrar cliente
        try:
            self.client_controller.create_client(client_data)

            # Registrar en el log
            if self.user_data:
                logger = get_logger()
                logger.log_crear_cliente(
                    self.user_data['name'],
                    self.user_data['role'],
                    client_data['nombre_cliente'],
                    client_data['cliente_ci']
                )

            QMessageBox.information(self, "Éxito", "Cliente registrado correctamente.")
            self.clear_form()
        except Exception as e:
            # Registrar error en el log
            if self.user_data:
                logger = get_logger()
                logger.log_error(
                    self.user_data['name'],
                    self.user_data['role'],
                    "CREAR_CLIENTE",
                    str(e)
                )
            QMessageBox.critical(self, "Error", f"No se pudo registrar el cliente: {e}")

    def clear_form(self):
        """Limpia los campos del formulario."""
        self.id_input.clear()
        self.cliente_ci_input.clear()
        self.nombre_cliente_input.clear()
        self.direccion_input.setCurrentIndex(0)
        self.telefono_input.clear()
        self.email_input.clear()
        self.numero_conexion_input.clear()
        self.estado_input.setCurrentIndex(0)
