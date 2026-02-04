from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QMessageBox, QGridLayout,
    QProgressDialog, QCheckBox, QListWidget, QFrame, QSizePolicy, QDialog
)
from datetime import datetime
import sqlite3
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from app.controllers.factura_controller import FacturaController
from app.models.factura import FacturaModel
from app.helpers.imprimir_factura import ImprimirFactura
from app.helpers.recuperar_lecturas import RecuperarLecturas
from app.helpers.recuperar_factura_id import RecuperarFacturaID
from app.helpers.recuperar_saldo_pendiente import SaldoPendienteHelper
from app.helpers.actualizar_deudas import ActualizarDeudasHelper
from app.helpers.sistema_logs import get_logger

class FacturaEditWidget(QDialog):
    def __init__(self, db_path, factura_data, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.controller = FacturaController(db_path)
        self.factura_data = factura_data
        self.factura_id = factura_data.get("id")
        # Obtener el número de factura existente o generar uno si no tiene
        self.numero_factura = factura_data.get("numero_factura")
        if not self.numero_factura:
            # Si la factura antigua no tiene número, generarlo en formato antiguo
            self.numero_factura = f"001-001-{self.factura_id:09d}"
        self.setWindowTitle(f"Editar Factura {self.numero_factura}")
        self.setModal(True)
        self.showMaximized()  # Pantalla completa
        self.init_ui()
        self.cargar_datos_factura()

    def init_ui(self):
        """Inicializa la interfaz gráfica con diseño de dos columnas."""
        # Layout principal del widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Título de advertencia
        titulo_advertencia = QLabel("⚠️ EDICIÓN DE FACTURA - Esta acción reemplazará la factura existente")
        titulo_advertencia.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
            color: #d9534f;
            background-color: #f8d7da;
            padding: 10px;
            border: 2px solid #d9534f;
            border-radius: 5px;
        """)
        titulo_advertencia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo_advertencia)

        # Contenedor principal con dos columnas
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # ========== COLUMNA IZQUIERDA ==========
        left_column = QFrame()
        left_column.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        left_column.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(8)
        left_layout.setContentsMargins(15, 15, 15, 15)

        # --- DATOS DEL CLIENTE ---
        titulo_cliente = QLabel("DATOS DEL CLIENTE")
        titulo_cliente.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px;")
        left_layout.addWidget(titulo_cliente)

        form_cliente = QFormLayout()
        form_cliente.setSpacing(8)

        self.medidor_id_input = QLineEdit()
        self.medidor_id_input.setPlaceholderText("ID del medidor")
        self.medidor_id_input.setMinimumHeight(35)
        self.medidor_id_input.setReadOnly(True)
        form_cliente.addRow("ID Cliente:", self.medidor_id_input)

        self.nombre_cliente_input = QLineEdit()
        self.nombre_cliente_input.setReadOnly(True)
        self.nombre_cliente_input.setMinimumHeight(35)
        form_cliente.addRow("Nombre:", self.nombre_cliente_input)

        self.direccion_cliente_input = QLineEdit()
        self.direccion_cliente_input.setReadOnly(True)
        self.direccion_cliente_input.setMinimumHeight(35)
        form_cliente.addRow("Dirección:", self.direccion_cliente_input)

        self.cedula_cliente_input = QLineEdit()
        self.cedula_cliente_input.setReadOnly(True)
        self.cedula_cliente_input.setMinimumHeight(35)
        form_cliente.addRow("Cédula:", self.cedula_cliente_input)

        left_layout.addLayout(form_cliente)

        # --- DATOS DE LECTURA ---
        titulo_lectura = QLabel("DATOS DE LECTURA")
        titulo_lectura.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px; margin-top: 10px;")
        left_layout.addWidget(titulo_lectura)

        form_lectura = QFormLayout()
        form_lectura.setSpacing(8)

        self.lectura_id_input = QLineEdit()
        self.lectura_id_input.setReadOnly(True)
        self.lectura_id_input.setMinimumHeight(35)
        form_lectura.addRow("ID Lectura:", self.lectura_id_input)

        self.monto_lectura_input = QLineEdit()
        self.monto_lectura_input.setReadOnly(True)
        self.monto_lectura_input.setMinimumHeight(35)
        form_lectura.addRow("Consumo (m³):", self.monto_lectura_input)

        left_layout.addLayout(form_lectura)

        # --- TARIFAS Y MONTOS ---
        titulo_tarifas = QLabel("TARIFAS Y MONTOS")
        titulo_tarifas.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px; margin-top: 10px;")
        left_layout.addWidget(titulo_tarifas)

        form_tarifas = QFormLayout()
        form_tarifas.setSpacing(8)

        self.combobox_tarifa_basica = QComboBox()
        self.combobox_tarifa_basica.addItems(["Automatico","0–10 ($1.50)", "11–50 ($2.00)", "51–100 ($3.00)", "101+ ($3.00)"])
        self.combobox_tarifa_basica.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_tarifa_basica.setEnabled(False)
        self.combobox_tarifa_basica.setMinimumHeight(35)
        form_tarifas.addRow("Tarifa Básica:", self.combobox_tarifa_basica)

        self.combobox_tarifa_excedente = QComboBox()
        self.combobox_tarifa_excedente.addItems(["Automatico","(11-25)0.30 por unidad", "(26-50)0.40 por unidad", "(51-100)0.50 por unidad", "(101-+)0.75 por unidad"])
        self.combobox_tarifa_excedente.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_tarifa_excedente.setEnabled(False)
        self.combobox_tarifa_excedente.setMinimumHeight(35)
        form_tarifas.addRow("Tarifa Excedente:", self.combobox_tarifa_excedente)

        self.campo_monto_basico = QLineEdit()
        self.campo_monto_basico.setReadOnly(True)
        self.campo_monto_basico.setMinimumHeight(35)
        form_tarifas.addRow("Monto Básico:", self.campo_monto_basico)

        self.campo_monto_excedente = QLineEdit()
        self.campo_monto_excedente.setReadOnly(True)
        self.campo_monto_excedente.setMinimumHeight(35)
        form_tarifas.addRow("Monto Excedente:", self.campo_monto_excedente)

        self.campo_monto_total = QLineEdit()
        self.campo_monto_total.setReadOnly(True)
        self.campo_monto_total.setMinimumHeight(35)
        self.campo_monto_total.setStyleSheet("font-weight: bold; background-color: #d4edda;")
        form_tarifas.addRow("MONTO TOTAL:", self.campo_monto_total)

        left_layout.addLayout(form_tarifas)
        left_layout.addStretch()

        # ========== COLUMNA DERECHA ==========
        right_column = QFrame()
        right_column.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        right_column.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(8)
        right_layout.setContentsMargins(15, 15, 15, 15)

        # --- CONFIGURACIÓN DE FACTURA ---
        titulo_config = QLabel("CONFIGURACIÓN DE FACTURA")
        titulo_config.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px;")
        right_layout.addWidget(titulo_config)

        form_config = QFormLayout()
        form_config.setSpacing(8)

        self.combobox_mes_facturacion = QComboBox()
        self.combobox_mes_facturacion.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.combobox_mes_facturacion.setMinimumHeight(35)
        form_config.addRow("Mes Facturación:", self.combobox_mes_facturacion)

        self.combobox_estado = QComboBox()
        self.combobox_estado.addItems(["Deuda", "Pagado"])
        self.combobox_estado.setMinimumHeight(35)
        form_config.addRow("Estado:", self.combobox_estado)

        self.combobox_servicio = QComboBox()
        self.combobox_servicio.addItems(["DOMICILIARIA", "COMERCIAL", "INDUSTRIAL"])
        self.combobox_servicio.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_servicio.setMinimumHeight(35)
        form_config.addRow("Tipo Servicio:", self.combobox_servicio)

        self.combobox_tipo_pago = QComboBox()
        self.combobox_tipo_pago.addItems(["Efectivo", "Transferencia"])
        self.combobox_tipo_pago.setMinimumHeight(35)
        form_config.addRow("Tipo Pago:", self.combobox_tipo_pago)

        right_layout.addLayout(form_config)

        # --- SERVICIOS ADICIONALES ---
        titulo_servicios = QLabel("SERVICIOS ADICIONALES")
        titulo_servicios.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px; margin-top: 10px;")
        right_layout.addWidget(titulo_servicios)

        servicios_frame = QFrame()
        servicios_layout = QGridLayout(servicios_frame)
        servicios_layout.setSpacing(8)

        self.campos_adicionales = {}
        servicios_items = {
            "Traspaso": 30.00,
            "Medidor": 50.00,
            "Reconexión": 10.00,
            "Multas Mingas": 10.00,
            "Multas Sesiones": 10.00,
            "Conexion Nueva": 500.00
        }

        row = 0
        col = 0
        for campo, valor in servicios_items.items():
            checkbox = QCheckBox(f"{campo} (${valor:.2f})")
            checkbox.toggled.connect(self.actualizar_montos)
            checkbox.setMinimumHeight(30)
            servicios_layout.addWidget(checkbox, row, col)
            self.campos_adicionales[campo.lower()] = (checkbox, valor)
            col += 1
            if col > 1:
                col = 0
                row += 1

        right_layout.addWidget(servicios_frame)

        # --- MATERIALES ---
        materiales_frame = QFrame()
        materiales_layout = QHBoxLayout(materiales_frame)

        self.materiales_checkbox = QCheckBox("Materiales:")
        self.materiales_checkbox.toggled.connect(self.toggle_materiales)
        self.materiales_checkbox.setMinimumHeight(30)
        materiales_layout.addWidget(self.materiales_checkbox)

        self.materiales_input = QLineEdit()
        self.materiales_input.setPlaceholderText("Monto materiales")
        self.materiales_input.setEnabled(False)
        self.materiales_input.setMinimumHeight(35)
        self.materiales_input.textChanged.connect(self.actualizar_montos)
        materiales_layout.addWidget(self.materiales_input)

        right_layout.addWidget(materiales_frame)

        # --- OTROS SERVICIOS ---
        titulo_otros = QLabel("OTROS SERVICIOS")
        titulo_otros.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px; margin-top: 10px;")
        right_layout.addWidget(titulo_otros)

        otros_frame = QFrame()
        otros_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #4a86e8;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        otros_layout = QGridLayout(otros_frame)
        otros_layout.setSpacing(8)

        self.otros_servicios = {}
        otros_items = [
            ("Reubicacion", 30.00),
            ("Sanciones", 100.00),
            ("Multa carnet", 5.00),
            ("Carnet Nuevo", 1.00)
        ]

        for idx, (nombre, valor) in enumerate(otros_items):
            checkbox = QCheckBox(f"{nombre} (${valor:.2f})")
            checkbox.toggled.connect(self.actualizar_montos)
            checkbox.setMinimumHeight(30)
            row_pos = idx // 2
            col_pos = idx % 2
            otros_layout.addWidget(checkbox, row_pos, col_pos)
            self.otros_servicios[nombre.lower().replace(" ", "_")] = (checkbox, valor)

        right_layout.addWidget(otros_frame)
        right_layout.addStretch()

        # ========== COLUMNA DE BOTONES (TERCERA COLUMNA) ==========
        buttons_column = QFrame()
        buttons_column.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        buttons_column.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        buttons_layout = QVBoxLayout(buttons_column)
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(15, 15, 15, 15)

        # Título de la sección de acciones
        titulo_acciones = QLabel("ACCIONES")
        titulo_acciones.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: #e9ecef; padding: 8px; border-radius: 4px;")
        titulo_acciones.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addWidget(titulo_acciones)

        # Espaciador
        buttons_layout.addSpacing(15)

        # --- DESCUENTO TERCERA EDAD Y DISCAPACITADOS ---
        tercera_edad_frame = QFrame()
        tercera_edad_frame.setStyleSheet("""
            QFrame {
                background-color: #2980b9;
                border: 2px solid #1f5f8b;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        tercera_edad_layout = QVBoxLayout(tercera_edad_frame)
        tercera_edad_layout.setContentsMargins(15, 15, 15, 15)

        # Título del descuento
        titulo_descuento = QLabel("DESCUENTO ESPECIAL")
        titulo_descuento.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #ffffff;
                background-color: transparent;
                padding: 5px;
            }
        """)
        titulo_descuento.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tercera_edad_layout.addWidget(titulo_descuento)

        self.checkbox_tercera_edad = QCheckBox("Tercera Edad y\nDiscapacitados\n(50% descuento)")
        self.checkbox_tercera_edad.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
                border: 2px solid #ffffff;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #28a745;
                border: 2px solid #28a745;
            }
        """)
        self.checkbox_tercera_edad.stateChanged.connect(self.actualizar_montos)
        tercera_edad_layout.addWidget(self.checkbox_tercera_edad)

        buttons_layout.addWidget(tercera_edad_frame)

        buttons_layout.addStretch()

        # Botón Actualizar y Reimprimir
        self.actualizar_reimprimir_button = QPushButton("✓ Actualizar y\nReimprimir Factura")
        self.actualizar_reimprimir_button.clicked.connect(self.actualizar_y_reimprimir)
        self.actualizar_reimprimir_button.setMinimumHeight(80)
        self.actualizar_reimprimir_button.setMinimumWidth(180)
        self.actualizar_reimprimir_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #28a745;
                color: white;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
                border: 2px solid #1e7e34;
            }
        """)
        buttons_layout.addWidget(self.actualizar_reimprimir_button)

        # Espaciador entre botones
        buttons_layout.addSpacing(20)

        # Botón Cancelar
        self.cancelar_button = QPushButton("✕ Cancelar")
        self.cancelar_button.clicked.connect(self.reject)
        self.cancelar_button.setMinimumHeight(60)
        self.cancelar_button.setMinimumWidth(180)
        self.cancelar_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #6c757d;
                color: white;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #5a6268;
                border: 2px solid #545b62;
            }
        """)
        buttons_layout.addWidget(self.cancelar_button)

        buttons_layout.addStretch()

        # Información adicional
        info_label = QLabel("La factura se actualizará\ncon el mismo número:\n\n" + self.numero_factura)
        info_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #6c757d;
                background-color: #e9ecef;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        buttons_layout.addWidget(info_label)

        # Agregar las tres columnas al layout principal
        content_layout.addWidget(left_column, 2)  # Columna izquierda más ancha
        content_layout.addWidget(right_column, 2)  # Columna central más ancha
        content_layout.addWidget(buttons_column, 1)  # Columna de botones más estrecha
        main_layout.addWidget(content_widget)

    def cargar_datos_factura(self):
        """Carga los datos de la factura existente en el formulario."""
        # Datos del cliente
        self.medidor_id_input.setText(str(self.factura_data.get("medidor_id", "")))
        self.nombre_cliente_input.setText(self.factura_data.get("nombre_cliente", ""))
        self.direccion_cliente_input.setText(self.factura_data.get("direccion", ""))

        # Obtener la cédula del cliente desde la base de datos
        cliente = self.controller.obtener_cliente_por_id(self.factura_data.get("medidor_id", ""))
        if cliente:
            self.cedula_cliente_input.setText(cliente.get("cliente_ci", "No disponible"))

        # Datos de lectura
        self.lectura_id_input.setText(str(self.factura_data.get("lectura_id", "")))
        self.monto_lectura_input.setText(str(self.factura_data.get("monto_lectura", "0")))

        # Tarifas
        self.campo_monto_basico.setText(str(self.factura_data.get("tarifa_basica", "0")))
        self.campo_monto_excedente.setText(str(self.factura_data.get("tarifa_excedente", "0")))

        # Configuración
        mes = self.factura_data.get("mes_facturacion", "Enero")
        index_mes = self.combobox_mes_facturacion.findText(mes)
        if index_mes >= 0:
            self.combobox_mes_facturacion.setCurrentIndex(index_mes)

        estado = self.factura_data.get("estado", "Deuda")
        index_estado = self.combobox_estado.findText(estado)
        if index_estado >= 0:
            self.combobox_estado.setCurrentIndex(index_estado)

        servicio = self.factura_data.get("servicio", "DOMICILIARIA")
        index_servicio = self.combobox_servicio.findText(servicio)
        if index_servicio >= 0:
            self.combobox_servicio.setCurrentIndex(index_servicio)

        # Cargar checkbox de tercera edad
        tercera_edad = int(self.factura_data.get("tercera_edad", 0))
        if tercera_edad == 1:
            self.checkbox_tercera_edad.setChecked(True)

        # Cargar checkboxes de servicios adicionales
        if float(self.factura_data.get("traspaso", 0)) > 0:
            self.campos_adicionales["traspaso"][0].setChecked(True)
        if float(self.factura_data.get("medidor", 0)) > 0:
            self.campos_adicionales["medidor"][0].setChecked(True)
        if float(self.factura_data.get("reconexion", 0)) > 0:
            self.campos_adicionales["reconexión"][0].setChecked(True)
        if float(self.factura_data.get("multas_mingas", 0)) > 0:
            self.campos_adicionales["multas mingas"][0].setChecked(True)
        if float(self.factura_data.get("multas_sesiones", 0)) > 0:
            self.campos_adicionales["multas sesiones"][0].setChecked(True)
        if float(self.factura_data.get("conexion_nueva", 0)) > 0:
            self.campos_adicionales["conexion nueva"][0].setChecked(True)

        # Materiales
        materiales = float(self.factura_data.get("materiales", 0))
        if materiales > 0:
            self.materiales_checkbox.setChecked(True)
            self.materiales_input.setText(str(materiales))

        # Actualizar monto total
        self.actualizar_montos()

    def toggle_materiales(self):
        """Habilita o deshabilita el campo de materiales."""
        if self.materiales_checkbox.isChecked():
            self.materiales_input.setEnabled(True)
            self.materiales_input.setFocus()
        else:
            self.materiales_input.setEnabled(False)
            self.materiales_input.clear()
        self.actualizar_montos()

    def actualizar_montos(self):
        """Actualiza los montos basados en los valores seleccionados."""
        try:
            consumo = float(self.monto_lectura_input.text()) if self.monto_lectura_input.text() else 0
            tipo_servicio = self.combobox_servicio.currentText()

            if tipo_servicio == "DOMICILIARIA":
                monto_basico = 2.50
            elif tipo_servicio == "COMERCIAL":
                monto_basico = 3.50
            else:
                monto_basico = 4.50

            # Aplicar descuento del 50% si es tercera edad o discapacitado
            if self.checkbox_tercera_edad.isChecked():
                monto_basico = monto_basico * 0.50

            if consumo <= 10:
                monto_excedente = 0
            else:
                consumo_excedente = consumo - 10
                if consumo <= 50:
                    monto_excedente = consumo_excedente * 0.40
                elif consumo <= 100:
                    monto_excedente = consumo_excedente * 0.60
                else:
                    monto_excedente = consumo_excedente * 0.80

            total_adicionales = sum(
                valor for checkbox, valor in self.campos_adicionales.values()
                if checkbox.isChecked()
            )

            monto_otros = sum(
                valor for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            )

            monto_materiales = 0
            if self.materiales_checkbox.isChecked():
                try:
                    monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
                except ValueError:
                    monto_materiales = 0

            monto_total = monto_basico + monto_excedente + total_adicionales + monto_otros + monto_materiales

            self.campo_monto_basico.setText(f"{monto_basico:.2f}")
            self.campo_monto_excedente.setText(f"{monto_excedente:.2f}")
            self.campo_monto_total.setText(f"{monto_total:.2f}")

        except ValueError:
            self.campo_monto_basico.clear()
            self.campo_monto_excedente.clear()
            self.campo_monto_total.clear()

    def actualizar_factura(self):
        """Actualiza la factura existente en la base de datos."""
        # Confirmar la acción
        respuesta = QMessageBox.question(
            self,
            "Confirmar Actualización",
            f"¿Está seguro de que desea actualizar la factura #{self.factura_id}?\n\n"
            "Esta acción REEMPLAZARÁ la factura existente con el mismo código.\n"
            "Esta operación es irreversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        try:
            # Recolectar datos del formulario
            medidor_id = self.medidor_id_input.text()
            nombre_cliente = self.nombre_cliente_input.text()
            lectura_id = self.lectura_id_input.text()
            monto_lectura = float(self.monto_lectura_input.text()) if self.monto_lectura_input.text() else 0
            direccion_cliente = self.direccion_cliente_input.text()
            cliente_ci = self.cedula_cliente_input.text()

            tarifa_basica = float(self.campo_monto_basico.text()) if self.campo_monto_basico.text() else 0
            tarifa_excedente = float(self.campo_monto_excedente.text()) if self.campo_monto_excedente.text() else 0

            monto_total = float(self.campo_monto_total.text()) if self.campo_monto_total.text() else 0
            mes_facturacion = self.combobox_mes_facturacion.currentText()
            estado = self.combobox_estado.currentText()
            servicio = self.combobox_servicio.currentText()
            tipo_pago = self.combobox_tipo_pago.currentText()

            # Obtener valores de checkboxes
            traspaso = 30.00 if self.campos_adicionales["traspaso"][0].isChecked() else 0.00
            medidor = 50.00 if self.campos_adicionales["medidor"][0].isChecked() else 0.00
            reconexion = 10.00 if self.campos_adicionales["reconexión"][0].isChecked() else 0.00
            multas_sesiones = 10.00 if self.campos_adicionales["multas sesiones"][0].isChecked() else 0.00
            multas_mingas = 10.00 if self.campos_adicionales["multas mingas"][0].isChecked() else 0.00
            conexion_nueva = 500.00 if self.campos_adicionales["conexion nueva"][0].isChecked() else 0.00

            # Obtener estado de tercera edad / discapacitados
            tercera_edad = 1 if self.checkbox_tercera_edad.isChecked() else 0

            monto_otros = sum(
                valor for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            )

            monto_materiales = 0
            if self.materiales_checkbox.isChecked():
                try:
                    monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
                except ValueError:
                    monto_materiales = 0

            # Validar campos obligatorios
            if not medidor_id or not nombre_cliente or not lectura_id or not monto_total:
                QMessageBox.warning(self, "Campos Vacíos", "Por favor, llena todos los campos obligatorios.")
                return

            # Preparar datos para actualización
            factura_data = {
                "id": self.factura_id,
                "medidor_id": medidor_id,
                "nombre_cliente": nombre_cliente,
                "lectura_id": lectura_id,
                "monto_lectura": monto_lectura,
                "mes_facturacion": mes_facturacion,
                "monto_total": monto_total,
                "estado": estado,
                "servicio": servicio,
                "traspaso": traspaso,
                "medidor": medidor,
                "reconexion": reconexion,
                "multas_sesiones": multas_sesiones,
                "multas_mingas": multas_mingas,
                "conexion_nueva": conexion_nueva,
                "otros": monto_otros,
                "tarifa_basica": tarifa_basica,
                "tarifa_excedente": tarifa_excedente,
                "direccion": direccion_cliente,
                "materiales": monto_materiales,
                "tercera_edad": tercera_edad
            }

            # Actualizar en la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                UPDATE facturas
                SET medidor_id = :medidor_id,
                    nombre_cliente = :nombre_cliente,
                    lectura_id = :lectura_id,
                    monto_lectura = :monto_lectura,
                    mes_facturacion = :mes_facturacion,
                    monto_total = :monto_total,
                    estado = :estado,
                    servicio = :servicio,
                    traspaso = :traspaso,
                    medidor = :medidor,
                    reconexion = :reconexion,
                    multas_sesiones = :multas_sesiones,
                    multas_mingas = :multas_mingas,
                    conexion_nueva = :conexion_nueva,
                    otros = :otros,
                    tarifa_basica = :tarifa_basica,
                    tarifa_excedente = :tarifa_excedente,
                    direccion = :direccion,
                    materiales = :materiales,
                    tercera_edad = :tercera_edad
                WHERE id = :id
            """

            cursor.execute(query, factura_data)
            conn.commit()
            conn.close()

            # Registrar en el log
            if self.parent() and hasattr(self.parent(), 'user_data'):
                logger = get_logger()
                logger.log_editar_factura(
                    self.parent().user_data['name'],
                    self.parent().user_data['role'],
                    self.factura_id,
                    nombre_cliente,
                    monto_total
                )

            QMessageBox.information(
                self,
                "Éxito",
                f"Factura #{self.factura_id} actualizada exitosamente.\n\nLa factura ha sido reemplazada con los nuevos datos."
            )
            self.accept()

        except Exception as e:
            # Registrar error en el log
            if self.parent() and hasattr(self.parent(), 'user_data'):
                logger = get_logger()
                logger.log_error(
                    self.parent().user_data['name'],
                    self.parent().user_data['role'],
                    "EDITAR_FACTURA",
                    str(e)
                )
            QMessageBox.critical(self, "Error", f"Error al actualizar la factura: {str(e)}")

    def actualizar_y_reimprimir(self):
        """Actualiza la factura y luego la reimprime."""
        # Confirmar la acción
        respuesta = QMessageBox.question(
            self,
            "Confirmar Actualización y Reimpresión",
            f"¿Está seguro de que desea actualizar y reimprimir la factura #{self.factura_id}?\n\n"
            "Esta acción REEMPLAZARÁ la factura existente y generará un nuevo PDF.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        try:
            # Primero actualizar
            # Recolectar datos
            medidor_id = self.medidor_id_input.text()
            nombre_cliente = self.nombre_cliente_input.text()
            lectura_id = self.lectura_id_input.text()
            monto_lectura = float(self.monto_lectura_input.text()) if self.monto_lectura_input.text() else 0
            direccion_cliente = self.direccion_cliente_input.text()
            cliente_ci = self.cedula_cliente_input.text()

            tarifa_basica = float(self.campo_monto_basico.text()) if self.campo_monto_basico.text() else 0
            tarifa_excedente = float(self.campo_monto_excedente.text()) if self.campo_monto_excedente.text() else 0

            monto_total = float(self.campo_monto_total.text()) if self.campo_monto_total.text() else 0
            mes_facturacion = self.combobox_mes_facturacion.currentText()
            estado = self.combobox_estado.currentText()
            servicio = self.combobox_servicio.currentText()
            tipo_pago = self.combobox_tipo_pago.currentText()

            traspaso = 30.00 if self.campos_adicionales["traspaso"][0].isChecked() else 0.00
            medidor = 50.00 if self.campos_adicionales["medidor"][0].isChecked() else 0.00
            reconexion = 10.00 if self.campos_adicionales["reconexión"][0].isChecked() else 0.00
            multas_sesiones = 10.00 if self.campos_adicionales["multas sesiones"][0].isChecked() else 0.00
            multas_mingas = 10.00 if self.campos_adicionales["multas mingas"][0].isChecked() else 0.00
            conexion_nueva = 500.00 if self.campos_adicionales["conexion nueva"][0].isChecked() else 0.00

            # Obtener estado de tercera edad / discapacitados
            tercera_edad = 1 if self.checkbox_tercera_edad.isChecked() else 0

            monto_otros = sum(
                valor for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            )

            monto_materiales = 0
            if self.materiales_checkbox.isChecked():
                try:
                    monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
                except ValueError:
                    monto_materiales = 0

            # Obtener lecturas
            helper_lecturas = RecuperarLecturas(self.db_path)
            lecturas = helper_lecturas.recuperar_lecturas_por_medidor(medidor_id)
            lectura_anterior = lecturas.get("lectura_anterior", "No disponible") if lecturas else "No disponible"
            lectura_actual = lecturas.get("lectura_actual", "No disponible") if lecturas else "No disponible"

            # Validar
            if not medidor_id or not nombre_cliente or not lectura_id or not monto_total:
                QMessageBox.warning(self, "Campos Vacíos", "Por favor, llena todos los campos obligatorios.")
                return

            # Actualizar en BD
            factura_data_update = {
                "id": self.factura_id,
                "medidor_id": medidor_id,
                "nombre_cliente": nombre_cliente,
                "lectura_id": lectura_id,
                "monto_lectura": monto_lectura,
                "mes_facturacion": mes_facturacion,
                "monto_total": monto_total,
                "estado": estado,
                "servicio": servicio,
                "traspaso": traspaso,
                "medidor": medidor,
                "reconexion": reconexion,
                "multas_sesiones": multas_sesiones,
                "multas_mingas": multas_mingas,
                "conexion_nueva": conexion_nueva,
                "otros": monto_otros,
                "tarifa_basica": tarifa_basica,
                "tarifa_excedente": tarifa_excedente,
                "direccion": direccion_cliente,
                "materiales": monto_materiales,
                "tercera_edad": tercera_edad
            }

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                UPDATE facturas
                SET medidor_id = :medidor_id,
                    nombre_cliente = :nombre_cliente,
                    lectura_id = :lectura_id,
                    monto_lectura = :monto_lectura,
                    mes_facturacion = :mes_facturacion,
                    monto_total = :monto_total,
                    estado = :estado,
                    servicio = :servicio,
                    traspaso = :traspaso,
                    medidor = :medidor,
                    reconexion = :reconexion,
                    multas_sesiones = :multas_sesiones,
                    multas_mingas = :multas_mingas,
                    conexion_nueva = :conexion_nueva,
                    otros = :otros,
                    tarifa_basica = :tarifa_basica,
                    tarifa_excedente = :tarifa_excedente,
                    direccion = :direccion,
                    materiales = :materiales,
                    tercera_edad = :tercera_edad
                WHERE id = :id
            """

            cursor.execute(query, factura_data_update)
            conn.commit()
            conn.close()

            # Ahora reimprimir
            servicios_otros = [
                checkbox.text()
                for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            ]

            factura_data_print = {
                "Numero de Factura": self.numero_factura,  # Usar el número de factura existente
                "Cliente": nombre_cliente,
                "Cédula/ID": cliente_ci,
                "Medidor": medidor_id,
                "Barrio": direccion_cliente,
                "Lectura Actual": int(float(lectura_actual)) if lectura_actual != "No disponible" else 0,
                "Lectura Anterior": int(float(lectura_anterior)) if lectura_anterior != "No disponible" else 0,
                "Consumo Mensual(m³)": int(monto_lectura),
                "Tarifa Básica": f"${tarifa_basica:.2f}",
                "Tarifa Excedente": f"${tarifa_excedente:.2f}",
                "Traspaso": f"${traspaso:.2f}",
                "Medidor nuevo": f"${medidor:.2f}",
                "Reconexión": f"${reconexion:.2f}",
                "Multas sesiones": f"${multas_sesiones:.2f}",
                "Multas mingas": f"${multas_mingas:.2f}",
                "Conexion nueva": f"${conexion_nueva:.2f}",
                "Materiales": f"${monto_materiales:.2f}",
                "Monto Otros": f"${monto_otros:.2f}",
                "Saldo Pendiente": "$0.00",
                "Monto Total": f"${monto_total:.2f}",
                "Estado": estado,
                "Mes Facturación": mes_facturacion,
                "Fecha Emisión": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Tipo de pago": tipo_pago
            }

            impresor = ImprimirFactura(factura_data_print)
            impresor.servicios_otros = servicios_otros
            impresor.generar_pdf()

            # Registrar en el log
            if self.parent() and hasattr(self.parent(), 'user_data'):
                logger = get_logger()
                logger.log_editar_factura(
                    self.parent().user_data['name'],
                    self.parent().user_data['role'],
                    self.factura_id,
                    nombre_cliente,
                    monto_total
                )
                # También registrar la reimpresión
                logger.log_reimprimir_factura(
                    self.parent().user_data['name'],
                    self.parent().user_data['role'],
                    self.factura_id,
                    nombre_cliente
                )

            QMessageBox.information(
                self,
                "Éxito",
                f"Factura #{self.factura_id} actualizada y reimpresa exitosamente."
            )
            self.accept()

        except Exception as e:
            # Registrar error en el log
            if self.parent() and hasattr(self.parent(), 'user_data'):
                logger = get_logger()
                logger.log_error(
                    self.parent().user_data['name'],
                    self.parent().user_data['role'],
                    "EDITAR_FACTURA",
                    str(e)
                )
            QMessageBox.critical(self, "Error", f"Error al actualizar y reimprimir: {str(e)}")
