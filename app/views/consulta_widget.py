from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QGroupBox, QHBoxLayout,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QPushButton
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor, QIcon
from app.controllers.consulta_controller import ConsultaController
from app.helpers.imprimir_factura import ImprimirFactura
from app.views.factura_edit import FacturaEditWidget

class ConsultaWidget(QWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.controller = ConsultaController(db_path)
        self.selected_factura = None
        self.resultados_totales = []  # Almacena todos los resultados de la búsqueda
        self.pagina_actual = 0  # Página actual para la paginación
        self.registros_por_pagina = 2  # Limitar a 2 registros por página
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica mejorada."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título de la sección
        title_label = QLabel("Consulta de Facturas")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Grupo de filtros
        filtros_group = QGroupBox("Filtros de búsqueda")
        filtros_layout = QGridLayout()
        filtros_layout.setSpacing(10)
        filtros_group.setMaximumHeight(200)  # Limitar altura del grupo de filtros

        # Filtros por fechas con valores predeterminados
        filtros_layout.addWidget(QLabel("Fecha Inicio:"), 0, 0)
        self.fecha_inicio_input = QDateEdit()
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate().addMonths(-1))
        filtros_layout.addWidget(self.fecha_inicio_input, 0, 1)

        filtros_layout.addWidget(QLabel("Fecha Fin:"), 0, 2)
        self.fecha_fin_input = QDateEdit()
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(QDate.currentDate())
        filtros_layout.addWidget(self.fecha_fin_input, 0, 3)

        # Filtro por mes
        filtros_layout.addWidget(QLabel("Mes:"), 1, 0)
        self.mes_input = QComboBox()
        self.mes_input.addItems([
            "Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.mes_input.setCurrentText("Todos")
        filtros_layout.addWidget(self.mes_input, 1, 1)

        # Filtro por dirección
        filtros_layout.addWidget(QLabel("Dirección:"), 1, 2)
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Ingrese dirección...")
        filtros_layout.addWidget(self.direccion_input, 1, 3)

        # Filtro por nombre
        filtros_layout.addWidget(QLabel("Nombre o Apellido:"), 2, 0)
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese nombre o apellido...")
        filtros_layout.addWidget(self.nombre_input, 2, 1)

        # Layout para botones de búsqueda y limpiar filtros
        buttons_layout = QHBoxLayout()
        
        # Botón limpiar filtros
        self.limpiar_button = QPushButton("Limpiar Filtros")
        self.limpiar_button.setIcon(QIcon.fromTheme("edit-clear"))
        self.limpiar_button.clicked.connect(self.limpiar_filtros)
        buttons_layout.addWidget(self.limpiar_button)
        
        # Espaciador para separar los botones
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Botón para buscar
        self.buscar_button = QPushButton("Buscar Facturas")
        self.buscar_button.setIcon(QIcon.fromTheme("system-search"))
        self.buscar_button.clicked.connect(self.buscar_facturas)
        self.buscar_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(self.buscar_button)
        
        filtros_layout.addLayout(buttons_layout, 2, 2, 1, 2)
        filtros_group.setLayout(filtros_layout)
        main_layout.addWidget(filtros_group)

        # Grupo de resultados
        resultados_group = QGroupBox("Resultados")
        resultados_layout = QVBoxLayout()
        resultados_layout.setSpacing(8)  # Reducir el espaciado entre elementos

        # Tabla de resultados con estilo mejorado
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente ID", "Nombre Cliente", "Lectura ID", "Mes", "Monto Total", 
            "Fecha Emisión", "Estado"
        ])
        
        # Configura el aspecto de la tabla
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #4a86e8; color: white; font-weight: bold; }")

        # Ajuste de altura para mostrar 2 filas exactamente
        # Calculamos el alto para 2 filas + encabezado + un pequeño margen
        row_height = 30  # Altura estimada por fila en píxeles
        header_height = 30  # Altura estimada del encabezado
        margin = 5  # Margen adicional
        table_height = (row_height * 2) + header_height + margin
        self.table.setFixedHeight(table_height)
        
        # Conectar evento de selección
        self.table.itemSelectionChanged.connect(self.on_factura_selected)
        
        resultados_layout.addWidget(self.table)
        
        # Controles de paginación
        paginacion_layout = QHBoxLayout()
        
        # Etiqueta para mostrar información de paginación
        self.info_paginacion_label = QLabel("Sin resultados")
        paginacion_layout.addWidget(self.info_paginacion_label)
        
        # Añadir espaciador para empujar los botones a la derecha
        paginacion_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Botones de navegación
        self.btn_primera = QPushButton("«")
        self.btn_anterior = QPushButton("‹")
        self.btn_siguiente = QPushButton("›")
        self.btn_ultima = QPushButton("»")
        
        self.btn_primera.setFixedWidth(40)
        self.btn_anterior.setFixedWidth(40)
        self.btn_siguiente.setFixedWidth(40)
        self.btn_ultima.setFixedWidth(40)
        
        # Mejorar el espaciado vertical de los botones
        for btn in [self.btn_primera, self.btn_anterior, self.btn_siguiente, self.btn_ultima]:
            btn.setFixedHeight(30)
            btn.setStyleSheet("margin: 2px;")
        
        self.btn_primera.clicked.connect(lambda: self.cambiar_pagina(0))
        self.btn_anterior.clicked.connect(lambda: self.cambiar_pagina(self.pagina_actual - 1))
        self.btn_siguiente.clicked.connect(lambda: self.cambiar_pagina(self.pagina_actual + 1))
        self.btn_ultima.clicked.connect(lambda: self.cambiar_pagina(-1))  # -1 indicará la última página
        
        # Añadir botones al layout de paginación
        paginacion_layout.addWidget(self.btn_primera)
        paginacion_layout.addWidget(self.btn_anterior)
        paginacion_layout.addWidget(self.btn_siguiente)
        paginacion_layout.addWidget(self.btn_ultima)
        
        # Añadir el layout de paginación al layout principal de resultados
        resultados_layout.addLayout(paginacion_layout)
        
        # Inicialmente deshabilitamos los botones de paginación
        self.actualizar_controles_paginacion()
        
        # Botones para reimprimir y editar factura seleccionada
        botones_acciones_layout = QHBoxLayout()

        self.reimprimir_button = QPushButton("Reimprimir Factura Seleccionada")
        self.reimprimir_button.setIcon(QIcon.fromTheme("document-print"))
        self.reimprimir_button.clicked.connect(self.reimprimir_factura)
        self.reimprimir_button.setEnabled(False)  # Deshabilitado hasta que se seleccione una factura
        self.reimprimir_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        self.editar_button = QPushButton("Editar y Reimprimir")
        self.editar_button.setIcon(QIcon.fromTheme("document-edit"))
        self.editar_button.clicked.connect(self.editar_factura)
        self.editar_button.setEnabled(False)  # Deshabilitado hasta que se seleccione una factura
        self.editar_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        botones_acciones_layout.addWidget(self.reimprimir_button)
        botones_acciones_layout.addWidget(self.editar_button)
        resultados_layout.addLayout(botones_acciones_layout)
        resultados_group.setLayout(resultados_layout)
        main_layout.addWidget(resultados_group)

        self.setLayout(main_layout)
        self.setMinimumSize(900, 580)  # Reducir ligeramente la altura mínima

    def buscar_facturas(self):
        """Obtiene los datos filtrados y los muestra en la tabla."""
        # Desactivar los botones de acción al realizar una nueva búsqueda
        self.reimprimir_button.setEnabled(False)
        self.editar_button.setEnabled(False)
        self.selected_factura = None
        
        filtros = {
            "fecha_inicio": self.fecha_inicio_input.date().toString("yyyy-MM-dd") if not self.fecha_inicio_input.date().isNull() else None,
            "fecha_fin": self.fecha_fin_input.date().toString("yyyy-MM-dd") if not self.fecha_fin_input.date().isNull() else None,
            "mes": self.mes_input.currentText() if self.mes_input.currentText() != "Todos" else None,
            "direccion": self.direccion_input.text() if self.direccion_input.text() else None,
            "nombre": self.nombre_input.text() if self.nombre_input.text() else None
        }

        # Obtener resultados completos de la búsqueda
        self.resultados_totales = self.controller.filtrar_facturas(filtros)
        
        # Reiniciar a la primera página
        self.pagina_actual = 0
        
        # Actualizar la visualización con los resultados
        if self.resultados_totales:
            # Mostrar la primera página
            self.mostrar_pagina_actual()
            # Mostrar un mensaje de éxito
            QMessageBox.information(self, "Búsqueda Exitosa", f"Se encontraron {len(self.resultados_totales)} facturas.")
        else:
            # Limpiar la tabla si no hay resultados
            self.table.clearContents()
            self.table.setRowCount(0)
            self.info_paginacion_label.setText("Sin resultados")
            self.actualizar_controles_paginacion()
            QMessageBox.warning(self, "Sin Resultados", "No se encontraron facturas con los filtros aplicados.")
    
    def mostrar_pagina_actual(self):
        """Muestra la página actual de resultados en la tabla."""
        # Calcular el índice de inicio y fin para la página actual
        inicio = self.pagina_actual * self.registros_por_pagina
        fin = min(inicio + self.registros_por_pagina, len(self.resultados_totales))
        
        # Obtener los registros para la página actual
        registros_pagina = self.resultados_totales[inicio:fin]
        
        # Limpiar y configurar la tabla
        self.table.clearContents()
        self.table.setRowCount(len(registros_pagina))
        
        # Ajustar altura de filas para que sean uniformes
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, 30)  # Altura fija de 30 píxeles por fila
        
        # Llenar la tabla con los datos de la página actual
        for row, factura in enumerate(registros_pagina):
            # Aplicar color de fondo según el estado de la factura
            estado = str(factura[7])  # Asumiendo que el estado está en la columna 7
            row_color = QColor("#ffffff")  # Blanco por defecto
            
            if estado.lower() == "pagado":
                row_color = QColor("#e6ffe6")  # Verde claro para pagados
            elif estado.lower() == "pendiente":
                row_color = QColor("#fff0e6")  # Naranja claro para pendientes
            elif estado.lower() == "vencido":
                row_color = QColor("#ffe6e6")  # Rojo claro para vencidos
            
            for col, dato in enumerate(factura):
                item = QTableWidgetItem(str(dato))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)  # Solo lectura
                item.setBackground(row_color)
                self.table.setItem(row, col, item)
        
        # Actualizar la etiqueta de información de paginación
        total_paginas = self.calcular_total_paginas()
        self.info_paginacion_label.setText(
            f"Mostrando {inicio + 1}-{fin} de {len(self.resultados_totales)} facturas (Página {self.pagina_actual + 1} de {total_paginas})"
        )
        
        # Actualizar los controles de paginación
        self.actualizar_controles_paginacion()
    
    def cambiar_pagina(self, nueva_pagina):
        """Cambia a la página especificada."""
        # Si se pasa -1, ir a la última página
        if nueva_pagina == -1:
            nueva_pagina = self.calcular_total_paginas() - 1
        
        # Verificar que la página esté dentro de los límites
        total_paginas = self.calcular_total_paginas()
        if 0 <= nueva_pagina < total_paginas:
            self.pagina_actual = nueva_pagina
            self.mostrar_pagina_actual()
            
            # Reiniciar selección al cambiar de página
            self.selected_factura = None
            self.reimprimir_button.setEnabled(False)
            self.editar_button.setEnabled(False)
    
    def calcular_total_paginas(self):
        """Calcula el número total de páginas."""
        total_registros = len(self.resultados_totales)
        return max(1, (total_registros + self.registros_por_pagina - 1) // self.registros_por_pagina)
    
    def actualizar_controles_paginacion(self):
        """Actualiza el estado de los controles de paginación."""
        tiene_resultados = len(self.resultados_totales) > 0
        total_paginas = self.calcular_total_paginas()
        
        # Habilitar o deshabilitar botones según la posición actual
        self.btn_primera.setEnabled(tiene_resultados and self.pagina_actual > 0)
        self.btn_anterior.setEnabled(tiene_resultados and self.pagina_actual > 0)
        self.btn_siguiente.setEnabled(tiene_resultados and self.pagina_actual < total_paginas - 1)
        self.btn_ultima.setEnabled(tiene_resultados and self.pagina_actual < total_paginas - 1)
    
    def on_factura_selected(self):
        """Maneja la selección de una factura en la tabla."""
        selected_rows = self.table.selectedItems()
        if selected_rows:
            selected_row = self.table.currentRow()

            # Obtener todos los datos de la factura seleccionada
            factura_data = {}
            for col in range(self.table.columnCount()):
                header = self.table.horizontalHeaderItem(col).text()
                value = self.table.item(selected_row, col).text()
                factura_data[header] = value

            # Guardar los datos de la factura seleccionada
            self.selected_factura = factura_data

            # Habilitar los botones de reimpresión y edición
            self.reimprimir_button.setEnabled(True)
            self.editar_button.setEnabled(True)
        else:
            self.selected_factura = None
            self.reimprimir_button.setEnabled(False)
            self.editar_button.setEnabled(False)
    
    def reimprimir_factura(self):
        """Reimprime la factura seleccionada."""
        if self.selected_factura:
            try:
                # Obtener el ID de la factura seleccionada
                factura_id = int(self.selected_factura["ID"])
                
                # Obtener los datos completos de la factura desde la base de datos
                # (esto debe implementarse en el controlador)
                factura_completa = self.controller.obtener_factura_completa(factura_id)
                
                if factura_completa:
                    # Llamar al componente de impresión
                    ImprimirFactura(factura_completa)
                    QMessageBox.information(self, "Reimpresión", "Factura reenviada a impresión correctamente.")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo obtener los datos completos de la factura.")
            except Exception as e:
                QMessageBox.critical(self, "Error de Impresión", f"Ocurrió un error al reimprimir la factura: {str(e)}")
        else:
            QMessageBox.warning(self, "Selección Requerida", "Por favor, seleccione una factura para reimprimir.")
    
    def limpiar_filtros(self):
        """Limpia todos los filtros de búsqueda."""
        self.fecha_inicio_input.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_fin_input.setDate(QDate.currentDate())
        self.mes_input.setCurrentText("Todos")
        self.direccion_input.clear()
        self.nombre_input.clear()
        
        # Limpiar la tabla y reiniciar los datos de paginación
        self.table.clearContents()
        self.table.setRowCount(0)
        self.resultados_totales = []
        self.pagina_actual = 0
        self.info_paginacion_label.setText("Sin resultados")
        self.actualizar_controles_paginacion()
        
        # Reiniciar selección
        self.selected_factura = None
        self.reimprimir_button.setEnabled(False)
        self.editar_button.setEnabled(False)

    def editar_factura(self):
        """Abre el diálogo de edición para la factura seleccionada."""
        if self.selected_factura:
            try:
                # Obtener el ID de la factura seleccionada
                factura_id = int(self.selected_factura["ID"])

                # Obtener los datos completos de la factura desde la base de datos
                factura_completa = self.controller.obtener_factura_completa(factura_id)

                if factura_completa:
                    # Abrir el diálogo de edición
                    dialog = FacturaEditWidget(self.controller.model.db_path, factura_completa, self)
                    resultado = dialog.exec()

                    # Si se aceptó el diálogo (se guardó la factura), refrescar la búsqueda
                    if resultado:
                        self.buscar_facturas()
                        QMessageBox.information(
                            self,
                            "Actualización Completada",
                            "La factura ha sido actualizada exitosamente.\nLos resultados se han actualizado."
                        )
                else:
                    QMessageBox.warning(self, "Error", "No se pudo obtener los datos completos de la factura.")
            except Exception as e:
                QMessageBox.critical(self, "Error de Edición", f"Ocurrió un error al editar la factura: {str(e)}")
        else:
            QMessageBox.warning(self, "Selección Requerida", "Por favor, seleccione una factura para editar.")