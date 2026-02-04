from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTableWidget, 
    QTableWidgetItem, QPushButton, QHeaderView
)
from PyQt6.QtCore import Qt
import sqlite3

class ConsultaClientesWidget(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica."""
        main_layout = QVBoxLayout()

        # Filtros - Primera fila
        filter_layout1 = QHBoxLayout()

        # Filtro por ID
        filter_layout1.addWidget(QLabel("ID Cliente:"))
        self.id_filter = QLineEdit()
        self.id_filter.setPlaceholderText("Buscar por ID")
        self.id_filter.textChanged.connect(self.filtrar_datos)
        filter_layout1.addWidget(self.id_filter)

        # Filtro por CI/RUC
        filter_layout1.addWidget(QLabel("CI / RUC:"))
        self.ci_filter = QLineEdit()
        self.ci_filter.setPlaceholderText("Buscar por CI/RUC")
        self.ci_filter.textChanged.connect(self.filtrar_datos)
        filter_layout1.addWidget(self.ci_filter)

        main_layout.addLayout(filter_layout1)

        # Filtros - Segunda fila
        filter_layout2 = QHBoxLayout()

        # Filtro por nombre
        filter_layout2.addWidget(QLabel("Nombre:"))
        self.nombre_filter = QLineEdit()
        self.nombre_filter.setPlaceholderText("Buscar por Nombre")
        self.nombre_filter.textChanged.connect(self.filtrar_datos)
        filter_layout2.addWidget(self.nombre_filter)

        # Filtro por dirección
        filter_layout2.addWidget(QLabel("Dirección:"))
        self.direccion_filter = QLineEdit()
        self.direccion_filter.setPlaceholderText("Buscar por Dirección")
        self.direccion_filter.textChanged.connect(self.filtrar_datos)
        filter_layout2.addWidget(self.direccion_filter)

        # Botón de actualizar
        self.actualizar_button = QPushButton("Actualizar")
        self.actualizar_button.clicked.connect(self.cargar_datos)
        filter_layout2.addWidget(self.actualizar_button)

        main_layout.addLayout(filter_layout2)

        # Tabla para mostrar los datos
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Número de columnas
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombres del cliente", "CI", "Dirección", "Teléfono", "Email", "Número de conexión"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos desde la base de datos a la tabla."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion FROM clientes"
            cursor.execute(query)
            clientes = cursor.fetchall()
            conn.close()

            self.mostrar_datos(clientes)
        except sqlite3.Error as e:
            print(f"Error al cargar los datos: {e}")

    def mostrar_datos(self, clientes):
        """Muestra los datos en la tabla."""
        self.table.setRowCount(0)  # Limpia la tabla
        for row_number, cliente in enumerate(clientes):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(cliente):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def filtrar_datos(self):
        """Filtra los datos según los valores ingresados en los filtros."""
        id_cliente = self.id_filter.text().strip()
        ci_cliente = self.ci_filter.text().strip()
        nombre = self.nombre_filter.text().strip().lower()
        direccion = self.direccion_filter.text().strip().lower()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT id, nombre_cliente, cliente_ci, direccion, telefono, email, numero_conexion
                FROM clientes
                WHERE 
                    (id LIKE ? OR ? = '') AND
                    (cliente_ci LIKE ? OR ? = '') AND
                    (LOWER(nombre_cliente) LIKE ? OR ? = '') AND
                    (LOWER(direccion) LIKE ? OR ? = '')
            """
            cursor.execute(query, (
                f"%{id_cliente}%", id_cliente,
                f"%{ci_cliente}%", ci_cliente,
                f"%{nombre}%", nombre,
                f"%{direccion}%", direccion
            ))
            clientes = cursor.fetchall()
            conn.close()

            self.mostrar_datos(clientes)
        except sqlite3.Error as e:
            print(f"Error al filtrar los datos: {e}")
