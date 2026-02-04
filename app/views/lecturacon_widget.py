from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QPushButton, QComboBox, QHeaderView, QGroupBox,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from app.controllers.lecturacon_controller import LecturaController

class ConsultaLecturasWidget(QWidget):
    def __init__(self, db_path):
        super().__init__()
        self.controller = LecturaController(db_path)
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("Consulta de Lecturas")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Grupo de filtros
        filtros_group = QGroupBox("Filtros de Búsqueda")
        filtros_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        filtros_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(15)
        filtros_layout.setContentsMargins(15, 15, 15, 15)

        # Filtro por mes
        mes_label = QLabel("Mes:")
        mes_label.setFont(QFont("Arial", 10))
        self.mes_combo = QComboBox()
        self.mes_combo.setFont(QFont("Arial", 10))
        self.mes_combo.addItems(["Todos"] + [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.mes_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 120px;
            }
            QComboBox:hover {
                border: 1px solid #007bff;
            }
        """)
        filtros_layout.addWidget(mes_label)
        filtros_layout.addWidget(self.mes_combo)

        # Filtro por año
        anio_label = QLabel("Año:")
        anio_label.setFont(QFont("Arial", 10))
        self.anio_input = QLineEdit()
        self.anio_input.setFont(QFont("Arial", 10))
        self.anio_input.setPlaceholderText("Ej: 2024")
        self.anio_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 100px;
            }
            QLineEdit:hover {
                border: 1px solid #007bff;
            }
        """)
        filtros_layout.addWidget(anio_label)
        filtros_layout.addWidget(self.anio_input)

        # Filtro por dirección
        direccion_label = QLabel("Dirección:")
        direccion_label.setFont(QFont("Arial", 10))
        self.direccion_input = QLineEdit()
        self.direccion_input.setFont(QFont("Arial", 10))
        self.direccion_input.setPlaceholderText("Ej: Calle Principal")
        self.direccion_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 150px;
            }
            QLineEdit:hover {
                border: 1px solid #007bff;
            }
        """)
        filtros_layout.addWidget(direccion_label)
        filtros_layout.addWidget(self.direccion_input)

        # Filtro por nombre
        nombre_label = QLabel("Cliente:")
        nombre_label.setFont(QFont("Arial", 10))
        self.nombre_cliente_input = QLineEdit()
        self.nombre_cliente_input.setFont(QFont("Arial", 10))
        self.nombre_cliente_input.setPlaceholderText("Ej: Juan Pérez")
        self.nombre_cliente_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 150px;
            }
            QLineEdit:hover {
                border: 1px solid #007bff;
            }
        """)
        filtros_layout.addWidget(nombre_label)
        filtros_layout.addWidget(self.nombre_cliente_input)

        # Botón de búsqueda
        self.buscar_button = QPushButton("Buscar")
        self.buscar_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.buscar_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.buscar_button.clicked.connect(self.cargar_lecturas)
        filtros_layout.addWidget(self.buscar_button)

        filtros_group.setLayout(filtros_layout)
        main_layout.addWidget(filtros_group)

        # Grupo de tabla
        tabla_group = QGroupBox("Resultados")
        tabla_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        tabla_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        tabla_layout = QVBoxLayout()
        tabla_layout.setContentsMargins(15, 15, 15, 15)

        # Tabla de lecturas
        self.lecturas_table = QTableWidget()
        self.lecturas_table.setFont(QFont("Arial", 10))
        self.lecturas_table.setColumnCount(9)
        self.lecturas_table.setHorizontalHeaderLabels([
            "ID", "Numero medidor", "Lectura anterior", "Lectura actual", "Consumo",
            "Fecha lectura", "Usuario", "Direccion", "Cliente"
        ])
        self.lecturas_table.horizontalHeader().setStretchLastSection(True)
        self.lecturas_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lecturas_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #e9ecef;
                color: black;
            }
        """)
        tabla_layout.addWidget(self.lecturas_table)
        tabla_group.setLayout(tabla_layout)
        main_layout.addWidget(tabla_group)

        self.setLayout(main_layout)
        self.cargar_lecturas()  # Carga inicial de lecturas

    def cargar_lecturas(self):
        """Carga las lecturas en la tabla aplicando los filtros."""
        filtros = {}
        if self.mes_combo.currentText() != "Todos":
            # Convertir nombre del mes a número
            meses = {
                "Enero": "1", "Febrero": "2", "Marzo": "3", "Abril": "4",
                "Mayo": "5", "Junio": "6", "Julio": "7", "Agosto": "8",
                "Septiembre": "9", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
            }
            filtros["mes"] = meses[self.mes_combo.currentText()]
        if self.anio_input.text():
            filtros["año"] = self.anio_input.text()
        if self.direccion_input.text():
            filtros["direccion"] = self.direccion_input.text()
        if self.nombre_cliente_input.text():
            filtros["nombre_cliente"] = self.nombre_cliente_input.text()

        lecturas = self.controller.obtener_lecturas(filtros)
        self.lecturas_table.setRowCount(len(lecturas))
        for row_idx, lectura in enumerate(lecturas):
            for col_idx, dato in enumerate(lectura):
                item = QTableWidgetItem(str(dato))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.lecturas_table.setItem(row_idx, col_idx, item)
