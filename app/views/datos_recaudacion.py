from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, 
    QMessageBox, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from app.controllers.recaudacion_controller import RecaudacionController
from app.helpers import backup_helper

class DatosRecaudacion(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.controller = RecaudacionController(db_path)
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica y muestra el gráfico."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("Datos de Recaudación")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Grupo de filtros
        filtros_group = QGroupBox("Filtros")
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

        filtro_layout = QHBoxLayout()
        filtro_layout.setSpacing(15)
        filtro_layout.setContentsMargins(15, 15, 15, 15)

        # Año
        anio_label = QLabel("Año:")
        anio_label.setFont(QFont("Arial", 10))
        self.combo_anio = QComboBox()
        self.combo_anio.setFont(QFont("Arial", 10))
        self.combo_anio.addItems(self.controller.obtener_años_disponibles())
        self.combo_anio.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #007bff;
            }
        """)
        self.combo_anio.currentIndexChanged.connect(self.actualizar_grafico)
        filtro_layout.addWidget(anio_label)
        filtro_layout.addWidget(self.combo_anio)

        # Dirección
        direccion_label = QLabel("Dirección:")
        direccion_label.setFont(QFont("Arial", 10))
        self.combo_direccion = QComboBox()
        self.combo_direccion.setFont(QFont("Arial", 10))
        self.combo_direccion.addItems(["Todas"] + self.controller.obtener_direcciones_disponibles())
        self.combo_direccion.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1px solid #007bff;
            }
        """)
        self.combo_direccion.currentIndexChanged.connect(self.actualizar_grafico)
        filtro_layout.addWidget(direccion_label)
        filtro_layout.addWidget(self.combo_direccion)

        # Agregar botón de Cierre de Caja
        self.btn_cierre_caja = QPushButton("Cierre de Caja")
        self.btn_cierre_caja.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.btn_cierre_caja.clicked.connect(self.realizar_cierre_caja)
        
        # Agregar el botón al layout de filtros
        filtro_layout.addWidget(self.btn_cierre_caja)

        filtros_group.setLayout(filtro_layout)
        main_layout.addWidget(filtros_group)

        # Grupo del gráfico
        grafico_group = QGroupBox("Gráfico de Recaudación")
        grafico_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        grafico_group.setStyleSheet("""
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

        grafico_layout = QVBoxLayout()
        grafico_layout.setContentsMargins(15, 15, 15, 15)

        # Crear el gráfico
        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        grafico_layout.addWidget(self.canvas)

        grafico_group.setLayout(grafico_layout)
        main_layout.addWidget(grafico_group)

        # Botón de respaldo
        self.boton_respaldo = QPushButton("Generar Respaldo de Base de Datos")
        self.boton_respaldo.setFont(QFont("Arial", 10))
        self.boton_respaldo.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.boton_respaldo.clicked.connect(self.generar_respaldo)
        self.boton_respaldo.setFixedHeight(40)

        # Layout para los botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.boton_respaldo)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Datos de Recaudación")

        # Cargar gráfico por defecto
        self.actualizar_grafico()

    def generar_respaldo(self):
        """Solicita confirmación y genera el respaldo si el usuario lo aprueba."""
        respuesta = QMessageBox.question(
            self, "Generar Backup",
            "Es recomendable generar respaldos al finalizar la jornada de recaudación.\n\n¿Generar backup ahora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            backup_helper.crear_backup(self.db_path)
            QMessageBox.information(self, "Respaldo Exitoso", "✔ Backup generado correctamente.")
        else:
            QMessageBox.information(self, "Cancelado", "❌ Respaldo cancelado.")

    def actualizar_grafico(self):
        """Genera un gráfico de barras con los datos filtrados."""
        anio = self.combo_anio.currentText()
        direccion = self.combo_direccion.currentText()
        datos = self.controller.obtener_datos_recaudacion(anio, direccion)

        # Definir los 12 meses con valores iniciales de 0
        meses_map = {
            "Enero": 0, "Febrero": 0, "Marzo": 0, "Abril": 0,
            "Mayo": 0, "Junio": 0, "Julio": 0, "Agosto": 0,
            "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0
        }

        # Llenar con los datos obtenidos
        for mes, cantidad in datos:
            meses_map[mes] = cantidad

        # Extraer datos en orden
        meses = list(meses_map.keys())
        cantidades = list(meses_map.values())

        # Limpiar el gráfico antes de redibujar
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Crear gráfico de barras con mejor estilo
        barras = ax.bar(meses, cantidades, 
                       color=['#3498db' if c > 0 else '#d5dbdb' for c in cantidades],
                       alpha=0.8,
                       width=0.7)

        # Agregar etiquetas en las barras
        for barra in barras:
            height = barra.get_height()
            if height > 0:  # Solo mostrar etiquetas para barras con valores
                ax.text(barra.get_x() + barra.get_width()/2, height + 0.2, 
                        str(int(height)), 
                        ha='center', va='bottom', 
                        fontsize=10, fontweight='bold', 
                        color='#2c3e50')

        # Personalizar el gráfico
        ax.set_xlabel("Mes", fontsize=12, fontweight="bold", color="#2c3e50")
        ax.set_ylabel("Facturas Pagadas", fontsize=12, fontweight="bold", color="#2c3e50")
        ax.set_title(f"Facturas Pagadas en {anio} ({direccion})", 
                    fontsize=14, fontweight="bold", color="#2c3e50", pad=20)
        
        # Configurar ejes
        ax.set_xticks(range(len(meses)))
        ax.set_xticklabels(meses, rotation=45, fontsize=10, color="#2c3e50")
        # Eliminar los valores del eje Y
        ax.set_yticks([])
        ax.tick_params(axis='y', colors='#2c3e50')

        # Personalizar el fondo y las líneas
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ddd')
        ax.spines['bottom'].set_color('#ddd')
        ax.grid(axis='y', linestyle='--', alpha=0.7, color='#ddd')

        # Ajustar el layout
        self.figure.tight_layout()

        # Actualizar gráfico en la interfaz
        self.canvas.draw()

    def realizar_cierre_caja(self):
        """Realiza el cierre de caja del mes actual."""
        # Mostrar mensaje de confirmación
        reply = QMessageBox.question(
            self,
            "Confirmar Cierre de Caja",
            "¿Está seguro que desea realizar el cierre de caja del mes actual?\n"
            "Esta acción marcará como deuda las facturas no registradas.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Llamar al controlador para realizar el cierre de caja
            success, message = self.controller.realizar_cierre_caja()
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                # Actualizar la tabla después del cierre
                self.actualizar_tabla()
            else:
                QMessageBox.warning(self, "Error", message)
