# app/views/login_window.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QFrame, QHBoxLayout)
import sys
import os
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QPixmap
from app.controllers.auth_controller import AuthController
from app.helpers.sistema_logs import get_logger

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.app = QApplication.instance()
        icon_path = self.app.get_resource_path("app/resources/CelestineICO.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Sistema de Facturación de Agua Celestine - Login")
        self.setFixedSize(900, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(50)

        # === LADO IZQUIERDO: LOGO Y NOMBRE ===
        left_side = QVBoxLayout()
        left_side.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo_label = QLabel()
        logo_path = self.app.get_resource_path("app/resources/Celestine.png")
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_side.addWidget(logo_label)

        # Título del sistema
        title_label = QLabel("Sistema de Facturación\nde Agua Celestine")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2980b9;
            text-align: center;
            line-height: 1.3;
            margin-top: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        left_side.addWidget(title_label)

        # Subtítulo
        subtitle_label = QLabel("JAAPC - Mejía")
        subtitle_label.setStyleSheet("font-size: 16px; color: #555; text-align: center; margin-top: 10px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_side.addWidget(subtitle_label)

        # === LADO DERECHO: FORMULARIO DE LOGIN ===
        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Mensaje de bienvenida
        welcome_label = QLabel("Bienvenido")
        welcome_label.setStyleSheet("font-size: 30px; font-weight: bold; color: #2980b9; margin-bottom: 5px;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_side.addWidget(welcome_label)

        # Mensaje para credenciales
        message_label = QLabel("Por favor, introduzca sus credenciales para iniciar sesión")
        message_label.setStyleSheet("font-size: 15px; color: #555; margin-bottom: 5px;")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_side.addWidget(message_label)

        # Frame para el formulario
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 35px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """)
        form_frame.setMaximumWidth(360)
        form_frame.setMinimumWidth(340)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(18)

        # Campo usuario
        user_label = QLabel("Usuario:")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_label.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 2px; font-size: 14px;")
        form_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        self.username_input.setMinimumHeight(45)
        # Conectar Enter en el campo de usuario para hacer login
        self.username_input.returnPressed.connect(self.attempt_login)
        form_layout.addWidget(self.username_input)

        # Campo contraseña
        password_label = QLabel("Contraseña:")
        password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password_label.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 2px; font-size: 14px;")
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        # Conectar Enter en el campo de contraseña para hacer login
        self.password_input.returnPressed.connect(self.attempt_login)
        form_layout.addWidget(self.password_input)

        # Botón login
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setMinimumHeight(50)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1f5f99;
            }
        """)
        self.login_button.clicked.connect(self.attempt_login)
        form_layout.addWidget(self.login_button)

        right_side.addWidget(form_frame)
        right_side.addStretch()

        # Agregar los lados al layout principal (logo izquierda, formulario derecha)
        main_layout.addLayout(left_side, 1)
        main_layout.addLayout(right_side, 1)

        self.setLayout(main_layout)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_data = AuthController.login(username, password)
        if user_data:
            # Registrar login exitoso en el log
            logger = get_logger()
            logger.log_login(user_data['name'], user_data['role'])

            self.login_successful.emit(user_data)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña inválidas. Inténtelo de nuevo.")
