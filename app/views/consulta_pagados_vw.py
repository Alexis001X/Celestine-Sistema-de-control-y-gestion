# app/views/consulta_registros_y_deudas.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, 
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from app.controllers.consulta_pagados_contrl import ConsultaRegistrosYDeudasController
from app.helpers.imprimir_pagados import ImprimirListado

class ConsultaRegistrosYDeudas(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.controller = ConsultaRegistrosYDeudasController(db_path)
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica."""
        layout = QVBoxLayout()

        # Filtros superiores
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Mes Facturación:"))
        self.mes_facturacion_combo = QComboBox()
        self.mes_facturacion_combo.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        filter_layout.addWidget(self.mes_facturacion_combo)

        filter_layout.addWidget(QLabel("Dirección:"))
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Ingrese dirección")
        filter_layout.addWidget(self.direccion_input)

        layout.addLayout(filter_layout)

        # Botones de búsqueda
        button_layout = QHBoxLayout()
        self.buscar_pagados_btn = QPushButton("Buscar Pagados")
        self.buscar_pagados_btn.clicked.connect(self.mostrar_pagados)
        button_layout.addWidget(self.buscar_pagados_btn)

        self.buscar_deudores_btn = QPushButton("Buscar Deudores")
        self.buscar_deudores_btn.clicked.connect(self.mostrar_deudores)
        button_layout.addWidget(self.buscar_deudores_btn)

        self.buscar_total_deuda_btn = QPushButton("Total Facturas en Deuda")
        self.buscar_total_deuda_btn.clicked.connect(self.mostrar_deudores_por_totales)
        button_layout.addWidget(self.buscar_total_deuda_btn)

        layout.addLayout(button_layout)

        # Tabla de resultados
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Medidor ID", "Nombre Cliente", "Estado Factura", "Dirección"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.result_table)

        # Botones de impresión
        print_layout = QHBoxLayout()
        self.imprimir_pagados_btn = QPushButton("Imprimir Pagados")
        self.imprimir_pagados_btn.clicked.connect(self.imprimir_pagados)
        self.imprimir_pagados_btn.setEnabled(False)  # Inicialmente deshabilitado
        print_layout.addWidget(self.imprimir_pagados_btn)

        self.imprimir_deudores_btn = QPushButton("Imprimir Deudores")
        self.imprimir_deudores_btn.clicked.connect(self.imprimir_deudores)
        self.imprimir_deudores_btn.setEnabled(False)  # Inicialmente deshabilitado
        print_layout.addWidget(self.imprimir_deudores_btn)

        layout.addLayout(print_layout)
        self.setLayout(layout)

    def mostrar_pagados(self):
        """Obtiene y muestra los clientes que han pagado en un mes específico."""
        mes = self.mes_facturacion_combo.currentText()
        direccion = self.direccion_input.text()
        resultados = self.controller.buscar_pagados(mes, direccion)

        self.result_table.setRowCount(len(resultados))
        for row, factura in enumerate(resultados):
            for col, dato in enumerate(factura):
                item = QTableWidgetItem(str(dato) if dato is not None else "Sin registro")
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Hace la celda de solo lectura
                self.result_table.setItem(row, col, item)

        self.imprimir_pagados_btn.setEnabled(bool(resultados))  # Habilitar botón si hay datos

    def mostrar_deudores(self):
        """Obtiene y muestra los clientes sin facturas registradas en un mes específico."""
        mes = self.mes_facturacion_combo.currentText()
        direccion = self.direccion_input.text()
        resultados = self.controller.buscar_deudores(mes, direccion)

        self.result_table.setRowCount(len(resultados))
        for row, deudor in enumerate(resultados):
            for col, dato in enumerate(deudor):
                item = QTableWidgetItem(str(dato) if dato is not None else "Sin registro")
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Hace la celda de solo lectura
                self.result_table.setItem(row, col, item)

        self.imprimir_deudores_btn.setEnabled(bool(resultados))  # Habilitar botón si hay datos

    def mostrar_deudores_por_totales(self):
        """Obtiene y muestra los clientes con facturas en estado 'Deuda' y su cantidad de facturas en deuda."""
        direccion = self.direccion_input.text()
        resultados = self.controller.buscar_deudores_por_totales(direccion)

        self.result_table.setRowCount(len(resultados))
        for row, deudor in enumerate(resultados):
            facturas_en_deuda = int(deudor[2])  # Número de facturas en deuda

            # Determinar el color de la fila
            if facturas_en_deuda >= 6:
                color = QColor(255, 100, 100)  # Rojo para 6 o más facturas en deuda
            elif facturas_en_deuda >= 3:
                color = QColor(255, 255, 100)  # Amarillo para 3 a 5 facturas en deuda
            else:
                color = QColor(255, 255, 255)  # Blanco (sin color especial)

            for col, dato in enumerate(deudor):
                item = QTableWidgetItem(str(dato))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Hace la celda de solo lectura
                item.setBackground(color)  # Aplicar color de fondo
                self.result_table.setItem(row, col, item)

    def imprimir_pagados(self):
        """Llama al helper para imprimir la lista de pagados."""
        try:
            mes = self.mes_facturacion_combo.currentText()
            datos = [[self.result_table.item(row, col).text() for col in range(4)] for row in range(self.result_table.rowCount())]
            ImprimirListado("Lista de Pagados", datos, mes).generar_pdf()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF: {e}")

    def imprimir_deudores(self):
        """Llama al helper para imprimir la lista de deudores."""
        try:
            mes = self.mes_facturacion_combo.currentText()
            datos = [[self.result_table.item(row, col).text() for col in range(4)] for row in range(self.result_table.rowCount())]
            ImprimirListado("Lista de Deudores", datos, mes).generar_pdf()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF: {e}")
