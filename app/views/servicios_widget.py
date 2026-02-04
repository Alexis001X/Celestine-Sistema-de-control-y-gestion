from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QMessageBox, QGridLayout,
    QProgressDialog, QCheckBox, QDoubleSpinBox, QFrame, QGroupBox, QDateEdit
)
from datetime import datetime, timedelta

from PyQt6.QtCore import Qt, QDate
from app.controllers.servicios_controller import ServiciosController
from app.models.servicios import ServicioModel
from app.helpers.imprimir_servicios import ImprimirServicio

class ServiciosWidget(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.controller = ServiciosController(db_path)
        self.setup_ui()
        self.setup_connections()
        self.medidor_actual = None
        self.servicio_actual = None
        self.imprimir_servicio = None

    def setup_ui(self):
        """Inicializa la interfaz gráfica."""
        main_layout = QVBoxLayout()

        # Grupo de información del cliente
        cliente_group = QGroupBox("Información del Cliente")
        cliente_layout = QGridLayout()

        cliente_layout.addWidget(QLabel("Número de Conexión:"), 0, 0)
        self.medidor_id_input = QLineEdit()
        self.medidor_id_input.setPlaceholderText("Ingresa el número de conexión")
        self.medidor_id_input.textChanged.connect(self.cargar_datos_cliente)
        cliente_layout.addWidget(self.medidor_id_input, 0, 1)

        cliente_layout.addWidget(QLabel("Nombre Cliente:"), 0, 2)
        self.nombre_cliente_input = QLineEdit()
        self.nombre_cliente_input.setReadOnly(True)
        cliente_layout.addWidget(self.nombre_cliente_input, 0, 3)
        
        cliente_layout.addWidget(QLabel("CI:"), 1, 0)
        self.ci_cliente_input = QLineEdit()
        self.ci_cliente_input.setReadOnly(True)
        cliente_layout.addWidget(self.ci_cliente_input, 1, 1)

        cliente_layout.addWidget(QLabel("Dirección:"), 1, 2)
        self.direccion_cliente_input = QLineEdit()
        self.direccion_cliente_input.setReadOnly(True)
        cliente_layout.addWidget(self.direccion_cliente_input, 1, 3)

        cliente_layout.addWidget(QLabel("Teléfono:"), 2, 0)
        self.telefono_cliente_input = QLineEdit()
        self.telefono_cliente_input.setReadOnly(True)
        cliente_layout.addWidget(self.telefono_cliente_input, 2, 1)

        cliente_layout.addWidget(QLabel("Email:"), 2, 2)
        self.email_cliente_input = QLineEdit()
        self.email_cliente_input.setReadOnly(True)
        cliente_layout.addWidget(self.email_cliente_input, 2, 3)

        cliente_group.setLayout(cliente_layout)
        main_layout.addWidget(cliente_group)

        # Grupo de información del servicio
        servicio_group = QGroupBox("Información del Servicio")
        servicio_layout = QGridLayout()

        servicio_layout.addWidget(QLabel("Usuario Servicio:"), 0, 0)
        self.usuario_servicio_combo = QComboBox()
        self.usuario_servicio_combo.addItems(["SELECCIONE UNA OPCIÓN", "NUEVO MEDIDOR"])
        self.usuario_servicio_combo.currentTextChanged.connect(self.actualizar_monto_servicio)
        servicio_layout.addWidget(self.usuario_servicio_combo, 0, 1)

        servicio_layout.addWidget(QLabel("Monto Servicio:"), 0, 2)
        self.monto_servicio_input = QDoubleSpinBox()
        self.monto_servicio_input.setRange(0, 1000000)
        self.monto_servicio_input.setDecimals(2)
        self.monto_servicio_input.setSingleStep(10)
        self.monto_servicio_input.valueChanged.connect(self.actualizar_monto_servicio)
        servicio_layout.addWidget(self.monto_servicio_input, 0, 3)

        self.diferir_pago_check = QCheckBox("Diferir pago en partes")
        self.diferir_pago_check.setVisible(False)
        self.diferir_pago_check.stateChanged.connect(self.actualizar_pagos_diferidos)
        servicio_layout.addWidget(self.diferir_pago_check, 1, 0, 1, 2)

        servicio_layout.addWidget(QLabel("Próxima Fecha de Pago:"), 1, 2)
        self.fecha_pago_input = QDateEdit()
        self.fecha_pago_input.setCalendarPopup(True)
        self.fecha_pago_input.setDate(QDate.currentDate().addDays(20))
        self.fecha_pago_input.setVisible(False)
        servicio_layout.addWidget(self.fecha_pago_input, 1, 3)

        servicio_group.setLayout(servicio_layout)
        main_layout.addWidget(servicio_group)

        # Grupo de pagos
        pagos_group = QGroupBox("Información de Pagos")
        pagos_layout = QGridLayout()

        pagos_layout.addWidget(QLabel("Pago 1:"), 0, 0)
        self.pago_uno_input = QLineEdit()
        self.pago_uno_input.setReadOnly(True)
        self.pago_uno_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        pagos_layout.addWidget(self.pago_uno_input, 0, 1)

        self.pago_uno_check = QCheckBox("Pagado")
        self.pago_uno_check.setVisible(False)
        self.pago_uno_check.stateChanged.connect(self.actualizar_saldo_pendiente)
        pagos_layout.addWidget(self.pago_uno_check, 0, 2)

        pagos_layout.addWidget(QLabel("Pago 2:"), 0, 3)
        self.pago_dos_input = QLineEdit()
        self.pago_dos_input.setReadOnly(True)
        self.pago_dos_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        pagos_layout.addWidget(self.pago_dos_input, 0, 4)

        self.pago_dos_check = QCheckBox("Pagado")
        self.pago_dos_check.setVisible(False)
        self.pago_dos_check.stateChanged.connect(self.actualizar_saldo_pendiente)
        pagos_layout.addWidget(self.pago_dos_check, 0, 5)

        pagos_layout.addWidget(QLabel("Pago 3:"), 1, 0)
        self.pago_tres_input = QLineEdit()
        self.pago_tres_input.setReadOnly(True)
        self.pago_tres_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        pagos_layout.addWidget(self.pago_tres_input, 1, 1)

        self.pago_tres_check = QCheckBox("Pagado")
        self.pago_tres_check.setVisible(False)
        self.pago_tres_check.stateChanged.connect(self.actualizar_saldo_pendiente)
        pagos_layout.addWidget(self.pago_tres_check, 1, 2)

        pagos_layout.addWidget(QLabel("Pago 4:"), 1, 3)
        self.pago_cuatro_input = QLineEdit()
        self.pago_cuatro_input.setReadOnly(True)
        self.pago_cuatro_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        pagos_layout.addWidget(self.pago_cuatro_input, 1, 4)

        self.pago_cuatro_check = QCheckBox("Pagado")
        self.pago_cuatro_check.setVisible(False)
        self.pago_cuatro_check.stateChanged.connect(self.actualizar_saldo_pendiente)
        pagos_layout.addWidget(self.pago_cuatro_check, 1, 5)

        pagos_layout.addWidget(QLabel("Saldo Pendiente:"), 2, 0, 1, 2)
        self.saldo_pendiente_input = QLineEdit()
        self.saldo_pendiente_input.setReadOnly(True)
        self.saldo_pendiente_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.saldo_pendiente_input.setStyleSheet("background-color: #f0f0f0; font-weight: bold;")
        pagos_layout.addWidget(self.saldo_pendiente_input, 2, 2, 1, 4)

        pagos_group.setLayout(pagos_layout)
        main_layout.addWidget(pagos_group)

        # Botones
        button_layout = QHBoxLayout()
        self.registrar_button = QPushButton("Registrar Servicio")
        self.registrar_button.clicked.connect(self.registrar_servicio)
        
        self.limpiar_button = QPushButton("Limpiar Formulario")
        self.limpiar_button.clicked.connect(self.limpiar_formulario)

        self.imprimir_btn = QPushButton("Imprimir Comprobante")
        self.imprimir_btn.setEnabled(False)
        self.imprimir_btn.clicked.connect(self.imprimir_comprobante)

        button_layout.addWidget(self.registrar_button)
        button_layout.addWidget(self.limpiar_button)
        button_layout.addWidget(self.imprimir_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_connections(self):
        self.imprimir_btn.clicked.connect(self.imprimir_comprobante)

    def cargar_datos_cliente(self):
        numero_conexion = self.medidor_id_input.text()
        if numero_conexion:
            cliente = self.controller.obtener_datos_cliente(numero_conexion)
            if cliente:
                self.nombre_cliente_input.setText(cliente["nombre_cliente"])
                self.ci_cliente_input.setText(cliente["cliente_ci"])
                self.direccion_cliente_input.setText(cliente["direccion"])
                self.telefono_cliente_input.setText(cliente["telefono"])
                self.email_cliente_input.setText(cliente["email"])
                self.cargar_estado_pagos(numero_conexion)
            else:
                self.limpiar_campos_cliente()
        else:
            self.limpiar_campos_cliente()

    def cargar_estado_pagos(self, numero_conexion):
        servicios = self.controller.obtener_servicios_por_medidor(numero_conexion)
        if servicios:
            ultimo_servicio = servicios[-1]
            if ultimo_servicio["pago_uno"] > 0:
                self.pago_uno_check.setChecked(True)
                self.pago_uno_check.setEnabled(False)
            if ultimo_servicio["pago_dos"] > 0:
                self.pago_dos_check.setChecked(True)
                self.pago_dos_check.setEnabled(False)
            if ultimo_servicio["pago_tres"] > 0:
                self.pago_tres_check.setChecked(True)
                self.pago_tres_check.setEnabled(False)
            if ultimo_servicio["pago_cuatro"] > 0:
                self.pago_cuatro_check.setChecked(True)
                self.pago_cuatro_check.setEnabled(False)
            self.actualizar_saldo_pendiente()

    def limpiar_campos_cliente(self):
        self.nombre_cliente_input.clear()
        self.ci_cliente_input.clear()
        self.direccion_cliente_input.clear()
        self.telefono_cliente_input.clear()
        self.email_cliente_input.clear()

    def actualizar_monto_servicio(self):
        opcion_seleccionada = self.usuario_servicio_combo.currentText()
        
        es_nuevo_medidor = opcion_seleccionada == "NUEVO MEDIDOR"
        self.diferir_pago_check.setVisible(es_nuevo_medidor)
        self.fecha_pago_input.setVisible(es_nuevo_medidor)
        
        self.pago_uno_check.setVisible(es_nuevo_medidor)
        self.pago_dos_check.setVisible(es_nuevo_medidor)
        self.pago_tres_check.setVisible(es_nuevo_medidor)
        self.pago_cuatro_check.setVisible(es_nuevo_medidor)
        
        if opcion_seleccionada == "NUEVO MEDIDOR":
            self.monto_servicio_input.setValue(500.00)
            self.fecha_pago_input.setDate(QDate.currentDate().addDays(20))
            self.monto_servicio_input.setReadOnly(True)
        else:
            self.monto_servicio_input.setValue(0.00)
            self.monto_servicio_input.setReadOnly(True)
        
        self.actualizar_pagos_diferidos()
        self.actualizar_saldo_pendiente()

    def actualizar_pagos_diferidos(self):
        opcion_seleccionada = self.usuario_servicio_combo.currentText()
        
        if opcion_seleccionada == "NUEVO MEDIDOR" and self.diferir_pago_check.isChecked():
            self.pago_uno_input.setText("250.00")
            self.pago_dos_input.setText("100.00")
            self.pago_tres_input.setText("100.00")
            self.pago_cuatro_input.setText("50.00")
            
            if not self.pago_uno_check.isChecked():
                self.pago_uno_check.setEnabled(True)
                self.pago_dos_check.setEnabled(False)
                self.pago_tres_check.setEnabled(False)
                self.pago_cuatro_check.setEnabled(False)
            elif not self.pago_dos_check.isChecked():
                self.pago_uno_check.setEnabled(False)
                self.pago_dos_check.setEnabled(True)
                self.pago_tres_check.setEnabled(False)
                self.pago_cuatro_check.setEnabled(False)
            elif not self.pago_tres_check.isChecked():
                self.pago_uno_check.setEnabled(False)
                self.pago_dos_check.setEnabled(False)
                self.pago_tres_check.setEnabled(True)
                self.pago_cuatro_check.setEnabled(False)
            elif not self.pago_cuatro_check.isChecked():
                self.pago_uno_check.setEnabled(False)
                self.pago_dos_check.setEnabled(False)
                self.pago_tres_check.setEnabled(False)
                self.pago_cuatro_check.setEnabled(True)
        else:
            monto_total = self.monto_servicio_input.value()
            self.pago_uno_input.setText(f"{monto_total:.2f}")
            self.pago_dos_input.setText("0.00")
            self.pago_tres_input.setText("0.00")
            self.pago_cuatro_input.setText("0.00")
            self.pago_uno_check.setEnabled(True)
            self.pago_dos_check.setEnabled(False)
            self.pago_tres_check.setEnabled(False)
            self.pago_cuatro_check.setEnabled(False)
        
        self.actualizar_saldo_pendiente()

    def actualizar_saldo_pendiente(self):
        opcion_seleccionada = self.usuario_servicio_combo.currentText()
        
        if opcion_seleccionada == "NUEVO MEDIDOR":
            monto_total = 500.00
            saldo_pagado = 0.00
            
            try:
                if self.pago_uno_check.isChecked():
                    pago_uno = self.pago_uno_input.text().strip()
                    saldo_pagado += float(pago_uno) if pago_uno else 0.0
                if self.pago_dos_check.isChecked():
                    pago_dos = self.pago_dos_input.text().strip()
                    saldo_pagado += float(pago_dos) if pago_dos else 0.0
                if self.pago_tres_check.isChecked():
                    pago_tres = self.pago_tres_input.text().strip()
                    saldo_pagado += float(pago_tres) if pago_tres else 0.0
                if self.pago_cuatro_check.isChecked():
                    pago_cuatro = self.pago_cuatro_input.text().strip()
                    saldo_pagado += float(pago_cuatro) if pago_cuatro else 0.0
            except ValueError:
                QMessageBox.warning(self, "Error", "Los valores de pago deben ser números válidos.")
                return
            
            saldo_pendiente = monto_total - saldo_pagado
            self.saldo_pendiente_input.setText(f"${saldo_pendiente:.2f}")
            
            if saldo_pendiente == 0:
                self.saldo_pendiente_input.setStyleSheet("background-color: #d4edda; color: #155724; font-weight: bold;")
            elif saldo_pendiente > 0:
                self.saldo_pendiente_input.setStyleSheet("background-color: #fff3cd; color: #856404; font-weight: bold;")
        else:
            self.saldo_pendiente_input.clear()

    def registrar_servicio(self):
        try:
            numero_conexion = self.medidor_id_input.text()
            nombre_usuario = self.nombre_cliente_input.text()
            direccion_usuario = self.direccion_cliente_input.text()
            usuario_servicio = self.usuario_servicio_combo.currentText()
            monto_servicio = self.monto_servicio_input.value()
            
            pago_uno = float(self.pago_uno_input.text()) if self.pago_uno_check.isChecked() else 0.0
            pago_dos = float(self.pago_dos_input.text()) if self.pago_dos_check.isChecked() else 0.0
            pago_tres = float(self.pago_tres_input.text()) if self.pago_tres_check.isChecked() else 0.0
            pago_cuatro = float(self.pago_cuatro_input.text()) if self.pago_cuatro_check.isChecked() else 0.0

            if not numero_conexion or usuario_servicio != "NUEVO MEDIDOR" or monto_servicio <= 0:
                QMessageBox.warning(self, "Campos Vacíos", "Seleccione 'NUEVO MEDIDOR' y complete los datos requeridos.")
                return

            if usuario_servicio == "NUEVO MEDIDOR" and not any([
                self.pago_uno_check.isChecked(),
                self.pago_dos_check.isChecked(),
                self.pago_tres_check.isChecked(),
                self.pago_cuatro_check.isChecked()
            ]):
                QMessageBox.warning(self, "Pago Requerido", "Seleccione al menos un pago para registrar.")
                return

            datos_servicio = {
                "numero_medidor": numero_conexion,
                "nombre_usuario": nombre_usuario,
                "direccion_usuario": direccion_usuario,
                "usuario_servicio": usuario_servicio,
                "monto_servicio": monto_servicio,
                "pago_uno": pago_uno,
                "pago_dos": pago_dos,
                "pago_tres": pago_tres,
                "pago_cuatro": pago_cuatro
            }

            id_servicio = self.controller.registrar_servicio(datos_servicio)
            if id_servicio:
                QMessageBox.information(self, "Éxito", f"Pago registrado con ID: {id_servicio}")
                self.cargar_estado_pagos(numero_conexion)
                self.imprimir_btn.setEnabled(True)
                self.servicio_actual = {
                    "id_servicio": id_servicio,
                    "numero_medidor": numero_conexion,
                    "nombre_usuario": nombre_usuario,
                    "direccion_usuario": direccion_usuario,
                    "usuario_servicio": usuario_servicio,
                    "monto_servicio": monto_servicio,
                    "pago_uno": pago_uno,
                    "pago_dos": pago_dos,
                    "pago_tres": pago_tres,
                    "pago_cuatro": pago_cuatro
                }
            else:
                QMessageBox.critical(self, "Error", "Error al registrar el pago.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def limpiar_formulario(self):
        self.medidor_id_input.clear()
        self.limpiar_campos_cliente()
        self.usuario_servicio_combo.setCurrentIndex(0)
        self.monto_servicio_input.setValue(0.00)
        self.diferir_pago_check.setChecked(False)
        self.pago_uno_input.setText("0.00")
        self.pago_dos_input.setText("0.00")
        self.pago_tres_input.setText("0.00")
        self.pago_cuatro_input.setText("0.00")
        self.fecha_pago_input.setDate(QDate.currentDate().addDays(20))
        self.pago_uno_check.setChecked(False)
        self.pago_dos_check.setChecked(False)
        self.pago_tres_check.setChecked(False)
        self.pago_cuatro_check.setChecked(False)
        self.saldo_pendiente_input.clear()
        self.pago_uno_check.setEnabled(True)
        self.pago_dos_check.setEnabled(True)
        self.pago_tres_check.setEnabled(True)
        self.pago_cuatro_check.setEnabled(True)
        self.imprimir_btn.setEnabled(False)
        self.servicio_actual = None

    def calcular_total_pagado(self):
        total = 0.0
        if self.pago_uno_check.isChecked():
            total += float(self.pago_uno_input.text().replace(',', '.'))
        if self.pago_dos_check.isChecked():
            total += float(self.pago_dos_input.text().replace(',', '.'))
        if self.pago_tres_check.isChecked():
            total += float(self.pago_tres_input.text().replace(',', '.'))
        if self.pago_cuatro_check.isChecked():
            total += float(self.pago_cuatro_input.text().replace(',', '.'))
        return total

    def calcular_saldo_pendiente(self):
        return self.monto_servicio_input.value() - self.calcular_total_pagado()

    def imprimir_comprobante(self):
        if not self.servicio_actual:
            QMessageBox.warning(self, "Advertencia", "No hay servicio para imprimir.")
            return

        tipo_servicio = self.usuario_servicio_combo.currentText()
        monto_total = self.monto_servicio_input.value()
        total_pagado = self.calcular_total_pagado()
        saldo_pendiente = self.calcular_saldo_pendiente()

        datos_comprobante = {
            "Cliente": self.nombre_cliente_input.text(),
            "Cédula/ID": self.ci_cliente_input.text(),
            "Medidor": self.medidor_id_input.text(),
            "Dirección": self.direccion_cliente_input.text(),
            "Tipo de Servicio": tipo_servicio,
            "Numero de Comprobante": self.servicio_actual.get("id_servicio", ""),
            "Monto Total": monto_total,
            "Total Pagado": total_pagado,
            "Saldo Pendiente": saldo_pendiente,
            "Fecha Emisión": QDate.currentDate().toString("dd/MM/yyyy")
        }

        if tipo_servicio == "NUEVO MEDIDOR" and self.diferir_pago_check.isChecked():
            datos_comprobante.update({
                "Pago 1": float(self.pago_uno_input.text()),
                "Pago 1 Fecha": self.fecha_pago_input.date().toString("dd/MM/yyyy") if self.pago_uno_check.isChecked() else "",
                "Pago 2": float(self.pago_dos_input.text()),
                "Pago 2 Fecha": self.fecha_pago_input.date().toString("dd/MM/yyyy") if self.pago_dos_check.isChecked() else "",
                "Pago 3": float(self.pago_tres_input.text()),
                "Pago 3 Fecha": self.fecha_pago_input.date().toString("dd/MM/yyyy") if self.pago_tres_check.isChecked() else "",
                "Pago 4": float(self.pago_cuatro_input.text()),
                "Pago 4 Fecha": self.fecha_pago_input.date().toString("dd/MM/yyyy") if self.pago_cuatro_check.isChecked() else "",
                "Es Diferido": True
            })
        else:
            datos_comprobante.update({
                "Pago 1": monto_total if total_pagado > 0 else 0,
                "Pago 1 Fecha": self.fecha_pago_input.date().toString("dd/MM/yyyy") if total_pagado > 0 else "",
                "Es Diferido": False
            })

        self.imprimir_servicio = ImprimirServicio(datos_comprobante)
        self.imprimir_servicio.generar_pdf()