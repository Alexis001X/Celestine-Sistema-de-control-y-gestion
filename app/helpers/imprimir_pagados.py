import os
from PyQt6.QtGui import QPainter, QFont, QPageSize, QPageLayout, QPen
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt, QRectF

class ImprimirListado:
    def __init__(self, titulo, datos, mes):
        """
        Inicializa el componente de impresión.
        
        :param titulo: Título del documento (Lista de Pagados o Deudores).
        :param datos: Lista de registros obtenidos desde la tabla.
        :param mes: Mes seleccionado para el reporte.
        """
        self.titulo = titulo
        self.datos = datos
        self.mes = mes

    def generar_pdf(self, output_path="lista_registros.pdf"):
        """
        Genera un archivo PDF con la lista de pagados o deudores con mejoras gráficas.
        
        :param output_path: Ruta donde se guardará el PDF.
        """
        try:
            # Configurar el PDF Writer
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(output_path)
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)

            # Iniciar el pintor
            painter = QPainter(printer)

            # Establecer fuentes
            title_font = QFont("Arial", 14, QFont.Weight.Bold)
            header_font = QFont("Arial", 11, QFont.Weight.Bold)
            text_font = QFont("Arial", 10)

            # Configuración de la impresión
            x_margin = 50
            y_margin = 50
            row_height = 35  # Espaciado entre filas
            col_positions = [x_margin, x_margin + 120, x_margin + 350, x_margin + 480]  # Posiciones de las columnas

            # Dibujar título centrado
            painter.setFont(title_font)
            painter.drawText(x_margin + 130, y_margin, f"{self.titulo} - {self.mes}")
            y_margin += 50

            # Dibujar encabezados de los campos
            painter.setFont(header_font)
            headers = ["Medidor ID", "Nombre Cliente", "Monto Lectura", "Dirección"]
            for i, header in enumerate(headers):
                painter.drawText(col_positions[i] + 5, y_margin, header)

            y_margin += row_height  # Espaciado después del encabezado

            # Dibujar datos con líneas verticales como separadores
            painter.setFont(text_font)
            line_pen = QPen(Qt.GlobalColor.black, 1)  # Línea de separación delgada

            for row in self.datos:
                max_line_height = row_height  # Controla el tamaño máximo de la fila

                for i, dato in enumerate(row):
                    x_pos = col_positions[i] + 5

                    # Si es la columna "Nombre Cliente", dividir en múltiples líneas si es necesario
                    if i == 1:  # "Nombre Cliente"
                        max_width = col_positions[i + 1] - col_positions[i] - 10  # Ancho permitido antes de la línea
                        text_rect = QRectF(x_pos, y_margin, max_width, row_height * 3)  # Permitimos hasta 3 líneas
                        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWrapAnywhere, str(dato))

                        # Calcular la altura utilizada
                        text_height = painter.boundingRect(text_rect, Qt.TextFlag.TextWrapAnywhere, str(dato)).height()
                        max_line_height = max(max_line_height, text_height + 5)  # Ajustar altura de la fila
                    else:
                        painter.drawText(x_pos, y_margin, str(dato))

                # Dibujar líneas verticales entre columnas
                for x in col_positions[1:]:  # Evita la primera posición
                    painter.setPen(line_pen)
                    painter.drawLine(x, y_margin - row_height + 10, x, y_margin + max_line_height - 10)

                y_margin += max_line_height  # Ajustar margen en función de la altura de la fila

                # Evitar que los datos se salgan de la página
                if y_margin > printer.pageRect(QPrinter.Unit.Point).height() - 50:
                    printer.newPage()
                    y_margin = 50  # Reiniciar margen superior en la nueva página

            # Terminar el pintor
            painter.end()

            # Mostrar mensaje de éxito
            QMessageBox.information(None, "Éxito", f"Listado generado correctamente en: {output_path}")
            os.startfile(output_path)  # Abrir el PDF en el visor predeterminado
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo generar el PDF: {e}")
