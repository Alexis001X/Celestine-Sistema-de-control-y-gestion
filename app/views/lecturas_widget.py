from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QMessageBox, QHBoxLayout, QGroupBox,
    QLabel, QFrame
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from app.controllers.lectura_controller import LecturaController
from datetime import datetime
from app.helpers.sistema_logs import get_logger


class LecturasWidget(QWidget):
    def __init__(self, db_path, user_data=None):
        super().__init__()
        self.controller = LecturaController(db_path)
        self.user_data = user_data  # Datos del usuario logueado
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("Registro de Lecturas")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Grupo de información del cliente
        cliente_group = QGroupBox("Información del Cliente")
        cliente_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        cliente_layout = QFormLayout()
        cliente_layout.setSpacing(10)
        cliente_layout.setContentsMargins(15, 15, 15, 15)

        # ID del cliente
        self.medidor_id_input = QLineEdit()
        self.medidor_id_input.setPlaceholderText("Ingresa el número del medidor")
        self.medidor_id_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }
        """)
        self.medidor_id_input.textChanged.connect(self.autocompletar_datos_cliente)
        cliente_layout.addRow("Número del medidor:", self.medidor_id_input)

        # Nombre del cliente (Solo lectura)
        self.nombre_cliente_display = QLineEdit()
        self.nombre_cliente_display.setReadOnly(True)
        self.nombre_cliente_display.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
        """)
        cliente_layout.addRow("Nombre del Cliente:", self.nombre_cliente_display)

        # Dirección del cliente (Solo lectura)
        self.direccion_display = QLineEdit()
        self.direccion_display.setReadOnly(True)
        self.direccion_display.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
        """)
        cliente_layout.addRow("Dirección:", self.direccion_display)

        cliente_group.setLayout(cliente_layout)
        main_layout.addWidget(cliente_group)

        # Grupo de información de lecturas
        lecturas_group = QGroupBox("Información de Lecturas")
        lecturas_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        lecturas_layout = QFormLayout()
        lecturas_layout.setSpacing(10)
        lecturas_layout.setContentsMargins(15, 15, 15, 15)

        # Lectura anterior (Solo lectura)
        self.lectura_anterior_entry = QLineEdit()
        self.lectura_anterior_entry.setReadOnly(True)
        self.lectura_anterior_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
        """)
        lecturas_layout.addRow("Lectura Anterior:", self.lectura_anterior_entry)

        # Lectura actual
        self.lectura_actual_entry = QLineEdit()
        self.lectura_actual_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }
        """)
        lecturas_layout.addRow("Lectura Actual:", self.lectura_actual_entry)

        # Fecha de lectura
        self.fecha_lectura_entry = QDateEdit(calendarPopup=True)
        self.fecha_lectura_entry.setDate(QDate.currentDate())
        self.fecha_lectura_entry.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QDateEdit:focus {
                border: 1px solid #007bff;
            }
        """)
        lecturas_layout.addRow("Fecha de Lectura:", self.fecha_lectura_entry)

        lecturas_group.setLayout(lecturas_layout)
        main_layout.addWidget(lecturas_group)

        # Botón de registro
        self.registrar_button = QPushButton("Registrar Lectura")
        self.registrar_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.registrar_button.clicked.connect(self.registrar_lectura)
        self.registrar_button.setFixedHeight(40)

        # Botón alineado al centro
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.registrar_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Establecer el layout principal
        self.setLayout(main_layout)

    def autocompletar_datos_cliente(self):
        """Autocompleta los campos de nombre, dirección y lectura anterior."""
        medidor_id = self.medidor_id_input.text()
        if medidor_id.isdigit():
            cliente = self.controller.obtener_cliente_y_direccion(medidor_id)
            if cliente:
                self.nombre_cliente_display.setText(cliente["nombre_cliente"])
                self.direccion_display.setText(cliente["direccion"])

                # Obtener la última lectura
                ultima_lectura = self.controller.obtener_ultima_lectura(medidor_id)
                if ultima_lectura is not None:
                    self.lectura_anterior_entry.setText(str(ultima_lectura))
                else:
                    self.lectura_anterior_entry.setText("0.0")
            else:
                # Limpiar campos si no se encuentra el cliente
                self.nombre_cliente_display.clear()
                self.direccion_display.clear()
                self.lectura_anterior_entry.clear()

    def registrar_lectura(self):
        """Registra una nueva lectura."""
        try:
            medidor_id = self.medidor_id_input.text()
            if not medidor_id.isdigit():
                QMessageBox.critical(self, "Error", "El ID del cliente debe ser un número válido.")
                return
            nombre_cliente = self.nombre_cliente_display.text()
            direccion = self.direccion_display.text()
            lectura_anterior = self.lectura_anterior_entry.text()
            lectura_actual = self.lectura_actual_entry.text()

            # Validar que todos los campos estén completos
            if not medidor_id or not lectura_actual or not lectura_anterior:
                QMessageBox.critical(self, "Error", "Todos los campos son obligatorios.")
                return

            medidor_id = int(medidor_id)
            lectura_anterior = float(lectura_anterior)
            lectura_actual = float(lectura_actual)

            # Validar que la lectura actual sea mayor o igual a la anterior
            if lectura_actual < lectura_anterior:
                QMessageBox.critical(self, "Error", "La lectura actual debe ser mayor o igual a la lectura anterior.")
                return

            # Calcular el consumo
            consumo = lectura_actual - lectura_anterior
            fecha_lectura = self.fecha_lectura_entry.date().toString("yyyy-MM-dd")

            # Registrar la lectura
            exito = self.controller.guardar_lectura(
                medidor_id, lectura_anterior, lectura_actual, consumo, 1,  # Usuario fijo por ahora
                fecha_lectura, direccion, nombre_cliente
            )
            if exito:
                # Registrar en el log
                if self.user_data:
                    logger = get_logger()
                    logger.log_crear_lectura(
                        self.user_data['name'],
                        self.user_data['role'],
                        medidor_id,
                        lectura_actual,
                        consumo
                    )

                QMessageBox.information(self, "Éxito", "Lectura registrada correctamente.")
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la lectura.")
        except Exception as e:
            # Registrar error en el log
            if self.user_data:
                logger = get_logger()
                logger.log_error(
                    self.user_data['name'],
                    self.user_data['role'],
                    "CREAR_LECTURA",
                    str(e)
                )
            print(f"Error al registrar la lectura: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error al registrar la lectura.")

    def limpiar_formulario(self):
        """Limpia los campos del formulario después del registro."""
        self.medidor_id_input.clear()
        self.nombre_cliente_display.clear()
        self.direccion_display.clear()
        self.lectura_anterior_entry.clear()
        self.lectura_actual_entry.clear()
