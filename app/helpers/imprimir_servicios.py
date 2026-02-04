from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from PyQt6.QtWidgets import QMessageBox
import os
import sys
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class ImprimirServicio:
    def __init__(self, servicio_data):
        """Inicializa el componente con los datos del servicio."""
        self.servicio_data = servicio_data

    def generar_pdf(self):
        """Genera el PDF del comprobante de servicio."""
        try:
            # Crear el documento PDF
            doc = SimpleDocTemplate("comprobante_servicio.pdf", pagesize=A4)
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]
            style_heading = styles["Heading1"]
            style_heading.alignment = 1  # Centrado

            # Logo
            logo_path = "app/resources/LOGO JAAPC.png"
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=100, height=100)
                elements.append(logo)

            # Título
            elements.append(Paragraph("COMPROBANTE DE SERVICIO", style_heading))
            elements.append(Spacer(1, 12))

            # Información del servicio
            data = [
                ["Cliente:", self.servicio_data["Cliente"]],
                ["Cédula/ID:", self.servicio_data["Cédula/ID"]],
                ["Medidor:", self.servicio_data["Medidor"]],
                ["Dirección:", self.servicio_data["Dirección"]],
                ["Tipo de Servicio:", self.servicio_data["Tipo de Servicio"]],
                ["Número de Comprobante:", self.servicio_data["Numero de Comprobante"]],
                ["Fecha de Emisión:", self.servicio_data["Fecha Emisión"]]
            ]

            # Tabla de información
            table = Table(data, colWidths=[150, 300])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

            # Detalles de pago
            if self.servicio_data["Es Diferido"]:
                # Para pagos diferidos
                pago_data = [
                    ["Pago", "Monto", "Fecha", "Estado"],
                    ["Pago 1", f"${self.servicio_data['Pago 1']:.2f}", self.servicio_data["Pago 1 Fecha"], "Pagado" if self.servicio_data["Pago 1 Fecha"] else "Pendiente"],
                    ["Pago 2", f"${self.servicio_data['Pago 2']:.2f}", self.servicio_data["Pago 2 Fecha"], "Pagado" if self.servicio_data["Pago 2 Fecha"] else "Pendiente"],
                    ["Pago 3", f"${self.servicio_data['Pago 3']:.2f}", self.servicio_data["Pago 3 Fecha"], "Pagado" if self.servicio_data["Pago 3 Fecha"] else "Pendiente"],
                    ["Pago 4", f"${self.servicio_data['Pago 4']:.2f}", self.servicio_data["Pago 4 Fecha"], "Pagado" if self.servicio_data["Pago 4 Fecha"] else "Pendiente"]
                ]
            else:
                # Para pagos únicos
                pago_data = [
                    ["Pago", "Monto", "Fecha", "Estado"],
                    ["Pago Total", f"${self.servicio_data['Monto Total']:.2f}", self.servicio_data["Pago 1 Fecha"], "Pagado" if self.servicio_data["Pago 1 Fecha"] else "Pendiente"]
                ]

            # Tabla de pagos
            pago_table = Table(pago_data, colWidths=[100, 100, 100, 100])
            pago_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ]))
            elements.append(pago_table)
            elements.append(Spacer(1, 12))

            # Totales
            total_data = [
                ["Monto Total:", f"${self.servicio_data['Monto Total']:.2f}"],
                ["Total Pagado:", f"${self.servicio_data['Total Pagado']:.2f}"],
                ["Saldo Pendiente:", f"${self.servicio_data['Saldo Pendiente']:.2f}"]
            ]

            # Tabla de totales
            total_table = Table(total_data, colWidths=[200, 200])
            total_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(total_table)

            # Generar el PDF
            doc.build(elements)

            # Abrir el PDF generado
            os.startfile("comprobante_servicio.pdf")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al generar el PDF: {str(e)}") 