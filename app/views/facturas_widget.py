from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QMessageBox, QGridLayout,
    QProgressDialog, QCheckBox, QListWidget, QScrollArea, QFrame, QSizePolicy
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
from app.helpers.secuencia_facturacion import get_secuencia_facturacion

class FacturasWidget(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.controller = FacturaController(db_path)
        self.parent_window = parent  # Guardar referencia al parent para acceder a user_data
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica."""
        # Layout principal del widget
        main_layout = QVBoxLayout(self)

        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Widget contenedor para el formulario
        form_widget = QFrame()
        form_widget.setFrameStyle(QFrame.Shape.NoFrame)

        # Grid para el formulario dentro del widget contenedor
        form_layout = QGridLayout(form_widget)
        form_layout.setSpacing(8)  # Espaciado reducido entre elementos
        form_layout.setContentsMargins(15, 15, 15, 15)  # Márgenes reducidos del formulario

        # Sección 1: Datos del Cliente
        titulo_cliente = QLabel("DATOS DEL CLIENTE")
        titulo_cliente.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_cliente, 0, 0, 1, 4)

        form_layout.addWidget(QLabel("ID Cliente:"), 1, 0)
        self.medidor_id_input = QLineEdit()
        self.medidor_id_input.setPlaceholderText("Ingresa el numero de medidor")
        self.medidor_id_input.setMinimumHeight(35)
        self.medidor_id_input.textChanged.connect(self.cargar_datos_cliente)
        form_layout.addWidget(self.medidor_id_input, 1, 1)

        form_layout.addWidget(QLabel("Nombre Cliente:"), 1, 2)
        self.nombre_cliente_input = QLineEdit()
        self.nombre_cliente_input.setReadOnly(True)
        self.nombre_cliente_input.setMinimumHeight(35)
        form_layout.addWidget(self.nombre_cliente_input, 1, 3)

        form_layout.addWidget(QLabel("Dirección:"), 2, 0)
        self.direccion_cliente_input = QLineEdit()
        self.direccion_cliente_input.setReadOnly(True)
        self.direccion_cliente_input.setMinimumHeight(35)
        form_layout.addWidget(self.direccion_cliente_input, 2, 1)

        form_layout.addWidget(QLabel("Número de Cédula:"), 2, 2)
        self.cedula_cliente_input = QLineEdit()
        self.cedula_cliente_input.setReadOnly(True)
        self.cedula_cliente_input.setMinimumHeight(35)
        form_layout.addWidget(self.cedula_cliente_input, 2, 3)

        # Sección 2: Datos de Lectura
        titulo_lectura = QLabel("DATOS DE LECTURA")
        titulo_lectura.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_lectura, 3, 0, 1, 4)

        form_layout.addWidget(QLabel("ID Lectura:"), 4, 0)
        self.lectura_id_input = QLineEdit()
        self.lectura_id_input.setReadOnly(True)
        self.lectura_id_input.setMinimumHeight(35)
        form_layout.addWidget(self.lectura_id_input, 4, 1)

        form_layout.addWidget(QLabel("Monto Lectura (m³):"), 4, 2)
        self.monto_lectura_input = QLineEdit()
        self.monto_lectura_input.setReadOnly(True)
        self.monto_lectura_input.setMinimumHeight(35)
        form_layout.addWidget(self.monto_lectura_input, 4, 3)

        # Sección 3: Tarifas y Montos
        titulo_tarifas = QLabel("TARIFAS Y MONTOS")
        titulo_tarifas.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_tarifas, 5, 0, 1, 4)

        form_layout.addWidget(QLabel("Tarifa Básica:"), 6, 0)
        self.combobox_tarifa_basica = QComboBox()
        self.combobox_tarifa_basica.addItems(["Automatico","0–10 ($1.50)", "11–50 ($2.00)", "51–100 ($3.00)", "101+ ($3.00)"])
        self.combobox_tarifa_basica.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_tarifa_basica.setEnabled(False)
        self.combobox_tarifa_basica.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_tarifa_basica, 6, 1)

        form_layout.addWidget(QLabel("Tarifa Excedente:"), 6, 2)
        self.combobox_tarifa_excedente = QComboBox()
        self.combobox_tarifa_excedente.addItems(["Automatico","(11-25)0.30 por unidad", "(26-50)0.40 por unidad", "(51-100)0.50 por unidad", "(101-+)0.75 por unidad"])
        self.combobox_tarifa_excedente.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_tarifa_excedente.setEnabled(False)
        self.combobox_tarifa_excedente.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_tarifa_excedente, 6, 3)

        form_layout.addWidget(QLabel("Monto Básico:"), 7, 0)
        self.campo_monto_basico = QLineEdit()
        self.campo_monto_basico.setReadOnly(True)
        self.campo_monto_basico.setMinimumHeight(35)
        form_layout.addWidget(self.campo_monto_basico, 7, 1)

        form_layout.addWidget(QLabel("Monto Excedente:"), 7, 2)
        self.campo_monto_excedente = QLineEdit()
        self.campo_monto_excedente.setReadOnly(True)
        self.campo_monto_excedente.setMinimumHeight(35)
        form_layout.addWidget(self.campo_monto_excedente, 7, 3)

        form_layout.addWidget(QLabel("Monto Total:"), 8, 0)
        self.campo_monto_total = QLineEdit()
        self.campo_monto_total.setReadOnly(True)
        self.campo_monto_total.setMinimumHeight(35)
        form_layout.addWidget(self.campo_monto_total, 8, 1)

        # Sección 4: Configuración de Factura
        titulo_config = QLabel("CONFIGURACIÓN DE FACTURA")
        titulo_config.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_config, 9, 0, 1, 4)

        form_layout.addWidget(QLabel("Mes de Facturación:"), 10, 0)
        self.combobox_mes_facturacion = QComboBox()
        self.combobox_mes_facturacion.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.combobox_mes_facturacion.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_mes_facturacion, 10, 1)

        form_layout.addWidget(QLabel("Estado:"), 10, 2)
        self.combobox_estado = QComboBox()
        self.combobox_estado.addItems(["Deuda", "Pagado"])
        self.combobox_estado.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_estado, 10, 3)

        form_layout.addWidget(QLabel("Servicio:"), 11, 0)
        self.combobox_servicio = QComboBox()
        self.combobox_servicio.addItems(["DOMICILIARIA", "COMERCIAL", "INDUSTRIAL"])
        self.combobox_servicio.currentIndexChanged.connect(self.actualizar_montos)
        self.combobox_servicio.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_servicio, 11, 1)

        form_layout.addWidget(QLabel("Tipo de pago:"), 11, 2)
        self.combobox_tipo_pago = QComboBox()
        self.combobox_tipo_pago.addItems(["Efectivo", "Transferencia"])
        self.combobox_tipo_pago.setMinimumHeight(35)
        form_layout.addWidget(self.combobox_tipo_pago, 11, 3)

        # Sección de Campos Adicionales
        titulo_servicios = QLabel("SERVICIOS ADICIONALES")
        titulo_servicios.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_servicios, 12, 0, 1, 4)

        # Campos adicionales con checkbox - organizados en 2 filas de 3 columnas
        self.campos_adicionales = {}
        servicios_items = [
            ("Traspaso", 30.00),
            ("Medidor", 50.00),
            ("Reconexión", 10.00),
            ("Multas Mingas", 10.00),
            ("Multas Sesiones", 10.00),
            ("Conexion Nueva", 500.00)
        ]

        servicios_row_start = 13
        for idx, (campo, valor) in enumerate(servicios_items):
            checkbox = QCheckBox(f"{campo} (${valor:.2f})")
            checkbox.toggled.connect(self.actualizar_montos)
            checkbox.setMinimumHeight(30)

            # Distribuir en 2 filas, 3 columnas cada una
            row_offset = idx // 3
            col_pos = idx % 3
            form_layout.addWidget(checkbox, servicios_row_start + row_offset, col_pos)
            self.campos_adicionales[campo.lower()] = (checkbox, valor)

        # Campo de Materiales con checkbox y textbox
        # Los 6 items ocupan filas 13-14 (2 filas de 3 columnas), entonces materiales va en fila 15
        row = 15
        form_layout.addWidget(QLabel("Materiales:"), row, 0)
        materiales_layout = QHBoxLayout()
        self.materiales_checkbox = QCheckBox("Activar:")
        self.materiales_checkbox.toggled.connect(self.toggle_materiales)
        self.materiales_input = QLineEdit()
        self.materiales_input.setPlaceholderText("Ingrese el monto de materiales")
        self.materiales_input.setEnabled(False)
        self.materiales_input.setMinimumHeight(35)
        self.materiales_input.textChanged.connect(self.actualizar_montos)

        materiales_layout.addWidget(self.materiales_checkbox)
        materiales_layout.addWidget(self.materiales_input)
        form_layout.addLayout(materiales_layout, row, 1, 1, 3)

        # Sección Otros Servicios
        row += 1
        titulo_otros = QLabel("OTROS SERVICIOS")
        titulo_otros.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_otros, row, 0, 1, 4)
        row += 1

        # Crear checkboxes para otros servicios en lugar de lista
        self.otros_servicios = {}
        otros_layout = QGridLayout()
        otros_items = [
            ("Reubicacion", 30.00),
            ("Sanciones", 100.00),
            ("Multa carnet", 5.00),
            ("Carnet Nuevo", 1.00)
        ]

        col = 0
        for nombre, valor in otros_items:
            checkbox = QCheckBox(f"{nombre} (${valor:.2f})")
            checkbox.toggled.connect(self.actualizar_montos)
            otros_layout.addWidget(checkbox, 0, col)
            self.otros_servicios[nombre.lower().replace(" ", "_")] = (checkbox, valor)
            col += 1

        otros_widget = QWidget()
        otros_widget.setLayout(otros_layout)
        form_layout.addWidget(otros_widget, row, 0, 1, 4)

        # Checkbox Tercera Edad y Discapacitados - Destacado al final
        row += 1
        separador = QLabel("")
        separador.setMinimumHeight(10)
        form_layout.addWidget(separador, row, 0, 1, 4)

        row += 1
        self.checkbox_tercera_edad = QCheckBox("✓ Tercera Edad y Discapacitados (50% descuento en tarifa base)")
        self.checkbox_tercera_edad.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                color: #ffffff;
                background-color: #2980b9;
                padding: 10px;
                border-radius: 5px;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.checkbox_tercera_edad.stateChanged.connect(self.actualizar_montos)
        form_layout.addWidget(self.checkbox_tercera_edad, row, 0, 1, 4)

        # Información de Deuda
        row += 1
        titulo_deuda = QLabel("INFORMACIÓN DE DEUDA")
        titulo_deuda.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px;")
        form_layout.addWidget(titulo_deuda, row, 0, 1, 4)
        row += 1
        form_layout.addWidget(QLabel("Total Deuda:"), row, 0)
        self.campo_total_deuda = QLineEdit()
        self.campo_total_deuda.setReadOnly(True)
        self.campo_total_deuda.setMinimumHeight(30)  # Reducido de 35 a 30
        self.campo_total_deuda.setMaximumWidth(120)  # Ancho máximo reducido
        form_layout.addWidget(self.campo_total_deuda, row, 1)

        # Label para mostrar el número de facturas en deuda
        self.label_facturas_deuda = QLabel("")
        self.label_facturas_deuda.setWordWrap(True)  # Permitir salto de línea
        form_layout.addWidget(self.label_facturas_deuda, row, 2, 1, 2)

        # Checkbox para incluir saldo pendiente
        row += 1
        self.checkbox_saldo_pendiente = QCheckBox("Incluir saldo pendiente")
        self.checkbox_saldo_pendiente.setChecked(True)
        self.checkbox_saldo_pendiente.setEnabled(False)
        form_layout.addWidget(self.checkbox_saldo_pendiente, row, 0, 1, 2)

        # Fin del formulario (sin botones)
        # Los botones ahora estarán fuera del área de scroll

        # Configurar el scroll area
        scroll_area.setWidget(form_widget)

        # Configurar tamaño mínimo para el área de scroll
        scroll_area.setMinimumHeight(500)  # Altura reducida para dar espacio a botones
        form_widget.setMinimumHeight(600)  # Altura del formulario sin botones

        # Agregar espacio adicional al final del formulario
        espaciador_final = QLabel("")
        espaciador_final.setMinimumHeight(15)
        form_layout.addWidget(espaciador_final, row + 1, 0, 1, 4)

        # Agregar el área de scroll al layout principal
        main_layout.addWidget(scroll_area)

        # Crear barra de botones fija fuera del scroll
        buttons_frame = QFrame()
        buttons_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 0px;
                margin: 0px;
            }
        """)

        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)

        # Crear los botones
        self.registrar_button = QPushButton("Registrar Factura")
        self.registrar_button.clicked.connect(self.registrar_factura)
        self.registrar_button.setMinimumHeight(30)
        self.registrar_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        self.imprimir_button = QPushButton("Imprimir Factura")
        self.imprimir_button.setEnabled(False)
        self.imprimir_button.clicked.connect(self.imprimir_factura)
        self.imprimir_button.setMinimumHeight(30)
        self.imprimir_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
            }
        """)

        self.actualizar_deudas_button = QPushButton("Actualizar Estado Deudas")
        self.actualizar_deudas_button.clicked.connect(self.actualizar_deudas)
        self.actualizar_deudas_button.setMinimumHeight(30)
        self.actualizar_deudas_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #ffc107;
                color: #212529;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)

        # Agregar botones al layout
        buttons_layout.addWidget(self.registrar_button)
        buttons_layout.addWidget(self.imprimir_button)
        buttons_layout.addWidget(self.actualizar_deudas_button)

        # Agregar la barra de botones al layout principal
        main_layout.addWidget(buttons_frame)

        # Configurar política de tamaño del widget principal
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        

    
    def cargar_datos_cliente(self):
        """Carga el nombre del cliente, su lectura_id, el consumo y la dirección."""
        medidor_id = self.medidor_id_input.text()
        if (medidor_id.isdigit()):
            cliente = self.controller.obtener_cliente_por_id(medidor_id)
            if cliente:
                self.nombre_cliente_input.setText(cliente["nombre_cliente"])
                self.cedula_cliente_input.setText(cliente.get("cliente_ci", "No disponible"))  # Asigna directamente al campo de la UI
                
                # Obtener datos de lectura, incluyendo dirección
                lectura = self.controller.obtener_lectura_por_cliente_id(medidor_id)
                if lectura:
                    self.lectura_id_input.setText(str(lectura["id"]))
                    self.monto_lectura_input.setText(f"{lectura['consumo']:.2f}")
                    self.direccion_cliente_input.setText(lectura["direccion"])  # Establecer dirección
                    
                    # Cargar información de deuda
                    self.cargar_informacion_deuda(medidor_id)
                    
                    self.actualizar_montos()  # Actualizar montos al cargar datos
                else:
                    self.lectura_id_input.clear()
                    self.monto_lectura_input.clear()
                    self.direccion_cliente_input.clear()
                    self.campo_monto_basico.clear()
                    self.campo_monto_excedente.clear()
                    self.campo_monto_total.clear()
                    self.campo_total_deuda.clear()
                    self.label_facturas_deuda.clear()
            else:
                # Limpiar campos si no existe el cliente
                self.nombre_cliente_input.clear()
                self.cedula_cliente_input.clear()
                self.monto_lectura_input.clear()
                self.direccion_cliente_input.clear()
                self.campo_monto_basico.clear()
                self.campo_monto_excedente.clear()
                self.campo_monto_total.clear()
                self.campo_total_deuda.clear()
                self.label_facturas_deuda.clear()
        else:
            # Limpiar campos si el medidor no es válido
            self.nombre_cliente_input.clear()
            self.lectura_id_input.clear()
            self.monto_lectura_input.clear()
            self.direccion_cliente_input.clear()
            self.campo_total_deuda.clear()
            self.label_facturas_deuda.clear()
            
    def cargar_informacion_deuda(self, medidor_id):
        """Carga la información de deuda del cliente y la muestra en la interfaz."""
        try:
            helper_saldo = SaldoPendienteHelper(self.controller.db_path)
            saldo_pendiente = helper_saldo.obtener_saldo_pendiente(medidor_id)

            # Obtener el número de facturas en deuda usando una consulta directa
            conn = sqlite3.connect(self.controller.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM facturas WHERE medidor_id = ? AND estado = 'Deuda'", (medidor_id,))
            num_facturas_deuda = cursor.fetchone()[0]
            conn.close()

            # Actualizar el campo de deuda
            self.campo_total_deuda.setText(f"${saldo_pendiente:.2f}")

            # Cambiar el color según si hay deuda o no
            palette = self.campo_total_deuda.palette()
            if saldo_pendiente > 0:
                palette.setColor(QPalette.ColorRole.Text, QColor("red"))
                self.label_facturas_deuda.setText(f"El cliente tiene {num_facturas_deuda} factura(s) en deuda")
                self.label_facturas_deuda.setStyleSheet("color: red;")
            else:
                palette.setColor(QPalette.ColorRole.Text, QColor("green"))
                self.label_facturas_deuda.setText("El cliente no tiene deudas pendientes")
                self.label_facturas_deuda.setStyleSheet("color: green;")

            self.campo_total_deuda.setPalette(palette)

            # Guardar el valor para usar en el cálculo del monto total
            self.saldo_pendiente = saldo_pendiente

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar información de deuda: {e}")

    def toggle_materiales(self):
        """Habilita o deshabilita el campo de materiales según el checkbox."""
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
            # Obtener el consumo actual
            consumo = float(self.monto_lectura_input.text()) if self.monto_lectura_input.text() else 0

            # Obtener el tipo de servicio seleccionado
            tipo_servicio = self.combobox_servicio.currentText()

            # Establecer monto básico según el tipo de servicio
            if tipo_servicio == "DOMICILIARIA":
                monto_basico = 2.50
            elif tipo_servicio == "COMERCIAL":
                monto_basico = 3.50
            else:  # INDUSTRIAL
                monto_basico = 4.50

            # Aplicar descuento del 50% si es tercera edad o discapacitado
            if self.checkbox_tercera_edad.isChecked():
                monto_basico = monto_basico * 0.50

            # Calcular monto excedente según el consumo
            if consumo <= 10:
                monto_excedente = 0
            else:
                consumo_excedente = consumo - 10
                if consumo <= 50:  # 11-50 m³
                    monto_excedente = consumo_excedente * 0.40
                elif consumo <= 100:  # 51-100 m³
                    monto_excedente = consumo_excedente * 0.60
                else:  # >100 m³
                    monto_excedente = consumo_excedente * 0.80

            # Calcular total de campos adicionales
            total_adicionales = sum(
                valor for checkbox, valor in self.campos_adicionales.values()
                if checkbox.isChecked()
            )

            # Calcular el valor de las opciones seleccionadas en "Otros"
            monto_otros = sum(
                valor for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            )

            # Calcular el valor de materiales
            monto_materiales = 0
            if self.materiales_checkbox.isChecked():
                try:
                    monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
                except ValueError:
                    monto_materiales = 0

            # Calcular monto total
            monto_total = monto_basico + monto_excedente + total_adicionales + monto_otros + monto_materiales

            # Actualizar campos
            self.campo_monto_basico.setText(f"{monto_basico:.2f}")
            self.campo_monto_excedente.setText(f"{monto_excedente:.2f}")
            self.campo_monto_total.setText(f"{monto_total:.2f}")

        except ValueError:
            # Si hay algún error en los cálculos, limpiar los campos
            self.campo_monto_basico.clear()
            self.campo_monto_excedente.clear()
            self.campo_monto_total.clear()

    def registrar_factura(self):
        """Registra una nueva factura en la base de datos."""
        try:
            medidor_id = self.medidor_id_input.text()
            nombre_cliente = self.nombre_cliente_input.text()
            lectura_id = self.lectura_id_input.text()
            monto_lectura = float(self.monto_lectura_input.text()) if self.monto_lectura_input.text() else 0
            direccion_cliente = self.direccion_cliente_input.text()
            cliente_ci = self.cedula_cliente_input.text() # Se obtiene si existe, si no, se asigna vacío

            tarifa_basica = float(self.campo_monto_basico.text()) if self.campo_monto_basico.text() else 0
            tarifa_excedente = float(self.campo_monto_excedente.text()) if self.campo_monto_excedente.text() else 0

            monto_total = float(self.campo_monto_total.text()) if self.campo_monto_total.text() else 0
            mes_facturacion = self.combobox_mes_facturacion.currentText()
            estado = self.combobox_estado.currentText()
            servicio = self.combobox_servicio.currentText()
            tipo_pago = self.combobox_tipo_pago.currentText()

            # Obtener valores de los checkboxes
            traspaso = 30.00 if self.campos_adicionales["traspaso"][0].isChecked() else 0.00
            self.traspaso = traspaso
            medidor = 50.00 if self.campos_adicionales["medidor"][0].isChecked() else 0.00
            self.medidor = medidor
            reconexion = 10.00 if self.campos_adicionales["reconexión"][0].isChecked() else 0.00
            self.reconexion = reconexion
            multas_sesiones = 10.00 if self.campos_adicionales["multas sesiones"][0].isChecked() else 0.00
            self.multas_sesiones = multas_sesiones
            multas_mingas = 10.00 if self.campos_adicionales["multas mingas"][0].isChecked() else 0.00
            self.multas_mingas = multas_mingas
            conexion_nueva = 500.00 if self.campos_adicionales["conexion nueva"][0].isChecked() else 0.00
            self.conexion_nueva = conexion_nueva

            # Calcular el valor de los checkboxes "Otros"
            monto_otros = sum(
                valor for checkbox, valor in self.otros_servicios.values()
                if checkbox.isChecked()
            )

            # Obtener el valor de materiales
            monto_materiales = 0
            if self.materiales_checkbox.isChecked():
                try:
                    monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
                except ValueError:
                    monto_materiales = 0
            
            # Obtener el saldo pendiente (ahora siempre incluido)
            saldo_pendiente = getattr(self, 'saldo_pendiente', 0.00)

            # Obtener estado de tercera edad / discapacitados
            tercera_edad = 1 if self.checkbox_tercera_edad.isChecked() else 0

             # Obtener datos de lectura actual y lectura anterior con el helper
            helper_lecturas = RecuperarLecturas(self.controller.db_path)
            lecturas = helper_lecturas.recuperar_lecturas_por_medidor(medidor_id)

            if not lecturas:
                QMessageBox.warning(self, "Advertencia", "No se encontraron lecturas para este cliente.")
                return

            self.lectura_anterior = lecturas.get("lectura_anterior", "No disponible")
            self.lectura_actual = lecturas.get("lectura_actual", "No disponible")

            # Validar que los campos obligatorios estén llenos
            if not medidor_id or not nombre_cliente or not lectura_id or not monto_total:
                QMessageBox.warning(self, "Campos Vacíos", "Por favor, llena todos los campos obligatorios antes de registrar la factura.")
                return

            # Obtener el número de factura de la nueva secuencia 001-010 ANTES de registrar
            secuencia = get_secuencia_facturacion(self.controller.db_path)
            self.numero_factura = secuencia.obtener_siguiente_numero()

            if not self.numero_factura:
                QMessageBox.critical(self, "Error", "No se pudo generar el número de factura.")
                return

            # Crear diccionario de datos para la factura
            factura_data = {
                "medidor_id": medidor_id,
                "nombre_cliente": nombre_cliente,
                "cliente_ci": cliente_ci,
                "lectura_id": lectura_id,
                "lectura_anterior": self.lectura_anterior,
                "lectura_actual": self.lectura_actual,
                "monto_lectura": monto_lectura,
                "mes_facturacion": mes_facturacion,
                "monto_total": monto_total,
                "fecha_emision": datetime.now().strftime("%Y-%m-%d"),
                "estado": estado,
                "servicio": servicio,
                "tipo_pago": tipo_pago,
                "traspaso": traspaso,
                "medidor": medidor,
                "reconexion": reconexion,
                "multas_sesiones": multas_sesiones,
                "multas_mingas": multas_mingas,
                "conexion_nueva": conexion_nueva,  # Cambiar la clave a "carnet_multas"
                "otros": monto_otros,
                "tarifa_basica": tarifa_basica,
                "tarifa_excedente": tarifa_excedente,
                "direccion": direccion_cliente,
                "saldo_pendiente": saldo_pendiente,
                "materiales": monto_materiales,
                "numero_factura": self.numero_factura,  # Agregar el número de factura
                "tercera_edad": tercera_edad  # Agregar descuento tercera edad
            }

            # Registrar factura en la base de datos
            factura_id = self.controller.registrar_factura(factura_data)
            if factura_id:
                # Llamar al helper para obtener el ID de la última factura
                helper_id = RecuperarFacturaID(self.controller.db_path)
                self.factura_id = helper_id.obtener_id_factura()

                # Registrar en el log
                if self.parent_window and hasattr(self.parent_window, 'user_data'):
                    logger = get_logger()
                    logger.log_crear_factura(
                        self.parent_window.user_data['name'],
                        self.parent_window.user_data['role'],
                        self.factura_id,
                        nombre_cliente,
                        monto_total
                    )

                # Habilitar botón de imprimir y mostrar mensaje de éxito
                self.imprimir_button.setEnabled(True)
                QMessageBox.information(self, "Éxito", f"Factura registrada exitosamente.\nNúmero: {self.numero_factura}")
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la factura. Por favor, inténtalo nuevamente.")
        except Exception as e:
            # Registrar error en el log
            if self.parent_window and hasattr(self.parent_window, 'user_data'):
                logger = get_logger()
                logger.log_error(
                    self.parent_window.user_data['name'],
                    self.parent_window.user_data['role'],
                    "CREAR_FACTURA",
                    str(e)
                )
            QMessageBox.critical(self, "Error", f"Ocurrió un error al registrar la factura: {e}")
     
    def actualizar_deudas(self):
        """Actualiza el estado de las facturas anteriores si la última está pagada."""
        try:
            medidor_id = self.medidor_id_input.text()
            if not medidor_id:
                QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un número de medidor.")
                return

            helper = ActualizarDeudasHelper(self.controller.db_path)
            resultado = helper.actualizar_facturas_pagadas(medidor_id)
            
            # Mostrar el resultado al usuario
            QMessageBox.information(self, "Actualización de Deudas", resultado)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar deudas: {e}")
            
    def guardar_respaldo_pdf(self, factura_data, servicios_otros):
        """Guarda un respaldo PDF de la factura en el escritorio en la carpeta facturas_respaldo."""
        try:
            # Obtener ruta al escritorio
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            carpeta_respaldo = os.path.join(escritorio, "facturas_respaldo")
            if not os.path.exists(carpeta_respaldo):
                os.makedirs(carpeta_respaldo)

            # Construir nombre de archivo
            nombre_cliente = factura_data.get("Cliente", "cliente").replace(" ", "_")
            fecha_emision = factura_data.get("Fecha Emisión", "").split(" ")[0].replace("-", "")
            mes_facturacion = factura_data.get("Mes Facturación", "mes")
            nombre_archivo = f"{nombre_cliente}_{fecha_emision}_{mes_facturacion}.pdf"
            ruta_pdf = os.path.join(carpeta_respaldo, nombre_archivo)

            # Generar el PDF de respaldo
            impresor = ImprimirFactura(factura_data)
            impresor.servicios_otros = servicios_otros
            impresor.generar_pdf(ruta_pdf)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el respaldo PDF: {e}")
    def imprimir_factura(self):
        """Prepara los datos y genera la factura en PDF."""
        # Calcular el valor de las opciones seleccionadas en "Otros"
        monto_otros = sum(
            valor for checkbox, valor in self.otros_servicios.values()
            if checkbox.isChecked()
        )

        # Obtener los nombres y valores de los servicios seleccionados en "Otros"
        servicios_otros = [
            checkbox.text()
            for checkbox, valor in self.otros_servicios.values()
            if checkbox.isChecked()
        ]

        # Obtener el valor de materiales para el PDF
        monto_materiales = 0
        if self.materiales_checkbox.isChecked():
            try:
                monto_materiales = float(self.materiales_input.text()) if self.materiales_input.text() else 0
            except ValueError:
                monto_materiales = 0

        factura_data = {
            "Numero de Factura": self.numero_factura,  # Usar el número de la nueva secuencia
            "Cliente": self.nombre_cliente_input.text(),
            "Cédula/ID": self.cedula_cliente_input.text(),
            "Medidor": self.medidor_id_input.text(),
            "Barrio": self.direccion_cliente_input.text(),
            "Lectura Actual": int(float(self.lectura_actual)),
            "Lectura Anterior": int(float(self.lectura_anterior)),
            "Consumo Mensual(m³)": int(float(self.monto_lectura_input.text() or 0)),
            "Tarifa Básica": f"${self.campo_monto_basico.text()}",
            "Tarifa Excedente": f"${self.campo_monto_excedente.text()}",
            "Traspaso": f"${self.traspaso:.2f}",
            "Medidor nuevo": f"${self.medidor:.2f}",
            "Reconexión": f"${self.reconexion:.2f}",
            "Multas sesiones": f"${self.multas_sesiones:.2f}",
            "Multas mingas": f"${self.multas_mingas:.2f}",
            "Conexion nueva": f"${self.conexion_nueva:.2f}",
            "Materiales": f"${monto_materiales:.2f}",
            "Monto Otros": f"${monto_otros:.2f}",  # Solo se muestra la suma total
            "Saldo Pendiente": f"${getattr(self, 'saldo_pendiente', 0.00):.2f}",
            "Monto Total": f"${self.campo_monto_total.text()}",
            "Estado": self.combobox_estado.currentText(),
            "Mes Facturación": self.combobox_mes_facturacion.currentText(),
            "Fecha Emisión": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Tipo de pago": self.combobox_tipo_pago.currentText()
        }

        impresor = ImprimirFactura(factura_data)
        impresor.servicios_otros = servicios_otros  # Pasar los servicios seleccionados al impresor
        impresor.generar_pdf()
        self.guardar_respaldo_pdf(factura_data, servicios_otros)
        # Mostrar mensaje de éxito
        # Colocar una opcion que recupera un dato de la factura anterior que sera saldo
        # pendiente y solo llenar ese campo con el monto total de la factura anterior
        # solo si la factura anterior tenga el estado de deuda si no lo tiene el valor es 0
        # Edicion de funcion de editar facturas mediante roles, contador puede editar, recaudador solo ingresar
