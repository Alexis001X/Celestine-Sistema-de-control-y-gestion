# app/views/soporte_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextBrowser, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SoporteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica del soporte."""
        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title = QLabel("Manual de Usuario")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Contenedor de texto con las instrucciones
        instructions = QTextBrowser()
        instructions.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ccc; padding: 10px;")
        instructions.setText("""
        <h3>Instrucciones de Uso</h3>
        <p>Bienvenido al <b>Sistema de Facturación Celestine</b>. Este manual tiene como propósito guiarle en el uso correcto de las funcionalidades del sistema:</p>
        <ul>
            <li><b>Clientes:</b> Permite registrar y gestionar la información de los clientes.</li>
            <li><b>Lecturas:</b> Registre las lecturas de consumo de agua de cada cliente.</li>
            <li><b>Facturación:</b> Emita facturas con base en las lecturas registradas.</li>
            <li><b>Consulta:</b> Consulte facturas, lecturas y clientes previas de manera rápida.</li>
            <li><b>Soporte:</b> Revise este manual para resolver dudas sobre el uso del sistema.</li>
        </ul>
        <h3>Consejos</h3>
        <p>Para un correcto funcionamiento del sistema:</p>
        <ul>
            <li>Asegúrese de registrar correctamente los datos de los clientes.</li>
            <li>los registros de clientes deben contener datos unicos no repetidos.</li>
            <li>Verifique las lecturas de agua antes de guardarlas.</li>
            <li>Los datos como el calculo del consumo y el mes de facturacion son automaticos y no se pueden modificar.</li>
            <li>Si existen facturas anteriores en deuda recuerda que se podran cobrar en la siguiente facturacion.</li>
            <li>Si valores pendientes de pago recuerda pulsar el boton de actualizar pagos para evitar errores de facturacion.</li>
            <li>Consulte el reporte mensual para realizar cierres contables.</li>
        </ul>
        <h3>Importante</h3>
        <p>Politica de Privacidad: El sistema no almacena información personal de los clientes, solo datos relacionados con el consumo de agua y facturación.</p>
        <ul>
            <li>Este sistema se maneja unicamente en la memoria local del dispositivo y posee un sistema que permite indentificar manipulacion en el codigo fuente, por ello si se detecta manipulacion en el codigo fuente se establecera sanciones economicas adicionales por reparacion e infraccion de derechos de autor.</li>
            <li>Evita manipular la base de datos sin conocimiento previo, el sistema actual solo permite ingreso de datos no de manipulacion ni alteracion directa </li>
        </ul>
        """)
        instructions.setReadOnly(True)
        main_layout.addWidget(instructions)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("margin: 10px 0; border: 1px solid #ccc;")
        main_layout.addWidget(separator)

        # Información del desarrollador
        footer = QLabel()
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #555; font-size: 12px;")
        footer.setText("""
        <p><b>Desarrollado por:</b> Tnlgo. Alexis Mena</p>
        <p><b>White.SoftwareSolutions</b> | 2025</p>    
        <p><b>Sistema de Facturación Celestine</b> | Versión 1.2.0</p>
        <p>© 2025 | Todos los derechos reservados.</p>
        """)

        main_layout.addWidget(footer)

        # Configuración del layout principal
        self.setLayout(main_layout)
