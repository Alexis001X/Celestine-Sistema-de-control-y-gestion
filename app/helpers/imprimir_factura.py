from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyQt6.QtWidgets import QMessageBox
import os
import sys

class ImprimirFactura:
    def __init__(self, factura_data):
        """Inicializa el componente con los datos de la factura."""
        self.factura_data = factura_data
        # Extraer servicios_otros del diccionario de datos
        self.servicios_otros = self.factura_data.get("Servicios Otros", [])

    def generar_pdf(self, output_path="factura.pdf"):
        """Genera un archivo PDF en formato A4 con dos facturas en la misma hoja."""
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            mitad_altura = height / 2  # Mitad de la hoja para la segunda factura
            margen = 30  # Margen alrededor de la factura

            def dibujar_factura(y_offset):
                """Dibuja una factura en la posición dada."""
                # Calcular la altura disponible para esta factura
                altura_factura = height / 2 - 2 * margen
                ancho_factura = width - 2 * margen
                
                # Dibujar el borde de la factura
                c.setLineWidth(1)
                c.rect(margen, y_offset - altura_factura - margen, ancho_factura, altura_factura)
                
                # Encabezado dentro del contenedor
                c.setFillColor(colors.black)

                # Título de la factura (dentro del contenedor)
                c.setFont("Helvetica-Bold", 14)
                c.drawCentredString(width / 2, y_offset - 45, "JUNTA ADMINISTRADORA DE AGUA POTABLE")
                c.setFont("Helvetica-Bold", 12)
                c.drawCentredString(width / 2, y_offset - 65, "CALICANTO - JAAPC - Mejía")
                
                # Añadir línea decorativa debajo del encabezado
                c.setLineWidth(2)
                c.line(margen + 5, y_offset - 85, width - margen - 5, y_offset - 85)
                c.setLineWidth(1)

                # Información del cliente en formato de tabla
                y_cliente = y_offset - 105
                c.setFont("Helvetica-Bold", 11)
                
                # Dibujar rectángulo para la sección de datos del cliente sin fondo
                altura_datos_cliente = 80
                c.setFillColor(colors.black)
                c.rect(margen + 5, y_cliente - altura_datos_cliente, ancho_factura - 10, altura_datos_cliente, fill=0, stroke=1)
                
                # Columna izquierda de datos del cliente
                c.setFont("Helvetica-Bold", 9)
                c.drawString(margen + 15, y_cliente - 20, "Consumidor:")
                c.drawString(margen + 15, y_cliente - 40, "Cédula:")
                c.drawString(margen + 15, y_cliente - 60, "Codigo de Medidor:")
                
                # Columna derecha de datos del cliente
                c.drawString(width / 2, y_cliente - 20, "Barrio:")
                c.drawString(width / 2, y_cliente - 40, "Mes Facturación:")
                c.drawString(width / 2, y_cliente - 60, "Número de Comprobante:")
                
                # Valores de los datos del cliente justificados a la derecha
                c.setFont("Helvetica", 9)
                mitad_ancho = width / 2  # Definir mitad_ancho aquí para asegurar que esté disponible
                x_valor_izq = mitad_ancho - 15  # Posición para alinear a la derecha, columna izquierda
                x_valor_der = width - margen - 15  # Posición para alinear a la derecha, columna derecha
                
                # Valores columna izquierda, justificados a la derecha
                c.drawRightString(x_valor_izq, y_cliente - 20, f"{self.factura_data.get('Cliente', 'No especificado')}")
                c.drawRightString(x_valor_izq, y_cliente - 40, f"{self.factura_data.get('Cédula/ID', 'No disponible')}")
                c.drawRightString(x_valor_izq, y_cliente - 60, f"{self.factura_data.get('Medidor', 'No especificado')}")
                
                # Valores columna derecha, justificados a la derecha
                c.drawRightString(x_valor_der, y_cliente - 20, f"{self.factura_data.get('Barrio', 'No especificado')}")
                c.drawRightString(x_valor_der, y_cliente - 40, f"{self.factura_data.get('Mes Facturación', 'No especificado')}")
                c.drawRightString(x_valor_der, y_cliente - 60, f"{self.factura_data.get('Numero de Factura', 'No especificado')}")

                # Sección de montos
                y_montos = y_cliente - altura_datos_cliente - 15
                c.setFont("Helvetica-Bold", 11)
                c.drawString(margen + 10, y_montos, "DETALLE DE FACTURACIÓN")
                
                # División para los montos
                y_tabla = y_montos - 15
                # Aumentamos la altura de la tabla para acomodar más campos
                altura_tabla_montos = 130  # Aumentada de 100 a 140
                c.setFillColor(colors.black)
                c.rect(margen + 5, y_tabla - altura_tabla_montos, ancho_factura - 10, altura_tabla_montos, fill=0, stroke=1)
                
                # Línea divisoria vertical en la tabla de montos
                mitad_ancho = width / 2
                c.line(mitad_ancho, y_tabla, mitad_ancho, y_tabla - altura_tabla_montos)
                
                # Detalles de los montos en dos columnas
                line_height = 15
                x_left_label = margen + 15
                x_left_value = mitad_ancho - 40
                x_right_label = mitad_ancho + 15
                x_right_value = width - margen - 40
                
                # Encabezados de la tabla de montos
                c.setFont("Helvetica-Bold", 9)
                c.drawString(x_left_label, y_tabla - line_height, "CONCEPTO")
                c.drawString(x_left_value - 40, y_tabla - line_height, "VALOR")
                c.drawString(x_right_label, y_tabla - line_height, "CONCEPTO")
                c.drawString(x_right_value - 40, y_tabla - line_height, "VALOR")
                
                # Línea debajo de los encabezados que llega hasta el final de la caja
                c.line(margen + 5, y_tabla - line_height - 5, width - margen - 5, y_tabla - line_height - 5)
                
                # Campos de montos a la izquierda (6 campos)
                y = y_tabla - 2 * line_height - 5
                montos_izquierda = [
                    "Lectura Actual", 
                    "Lectura Anterior", 
                    "Consumo Mensual(m³)", 
                    "Tarifa Básica", 
                    "Tarifa Excedente", 
                    "Traspaso"
                ]
                for key in montos_izquierda:
                    c.setFont("Helvetica", 9)
                    c.drawString(x_left_label, y, f"{key}:")
                    
                    # Formato especial para los valores monetarios
                    if key in ["Tarifa Básica", "Tarifa Excedente", "Monto Traspaso"]:
                        valor = self.factura_data.get(key, "$0.00")
                    else:
                        valor = self.factura_data.get(key, "0")
                    
                    c.drawRightString(x_left_value, y, f"{valor}")
                    y -= line_height
                
                # Campos de montos a la derecha (6 campos)
                y = y_tabla - 2 * line_height - 5
                montos_derecha = [
                    "Medidor nuevo",
                    "Reconexión",
                    "Multas sesiones",
                    "Multas mingas",
                    "Conexion nueva",
                    "Materiales"
                ]
                for key in montos_derecha:
                    c.setFont("Helvetica", 9)
                    c.drawString(x_right_label, y, f"{key}:")
                    valor = self.factura_data.get(key, "$0.00")
                    c.drawRightString(x_right_value, y, f"{valor}")
                    y -= line_height
                
                # Sección de otros montos y monto total
                y_otros = y_tabla - altura_tabla_montos - 3  # Reducido el espacio entre cajas
                
                # Eliminada línea divisoria antes de la sección final
                
                # Sección final: otros montos y monto total con altura reducida sin fondo
                altura_seccion_final = 40  # Reducida la altura de la sección final
                c.setFillColor(colors.black)
                c.rect(margen + 5, y_otros - altura_seccion_final, ancho_factura - 10, altura_seccion_final, fill=0, stroke=1)
                
                # Línea divisoria vertical en la sección final
                c.line(mitad_ancho, y_otros, mitad_ancho, y_otros - altura_seccion_final)
                
                # Otros montos cobrados (izquierda)
                c.setFont("Helvetica-Bold", 9)
                c.drawString(x_left_label, y_otros - 15, "OTROS MONTOS COBRADOS:")
                c.setFont("Helvetica", 8)
                servicios_otros_str = ", ".join(self.servicios_otros) if self.servicios_otros else "Ninguno"
                # Dividir el texto de servicios otros en líneas de máximo 30 caracteres
                lineas_servicios = []
                palabras = servicios_otros_str.split(", ")
                linea_actual = ""
                for palabra in palabras:
                    if len(linea_actual + palabra) < 30:
                        linea_actual += palabra + ", " if linea_actual else palabra
                    else:
                        lineas_servicios.append(linea_actual)
                        linea_actual = palabra
                if linea_actual:
                    lineas_servicios.append(linea_actual)
                    
                for i, linea in enumerate(lineas_servicios):
                    c.drawString(x_left_label, y_otros - 30 - (i * 10), linea)
                
                # Monto total (derecha)
                c.setFont("Helvetica-Bold", 11)
                c.drawString(x_right_label, y_otros - 20, "MONTO TOTAL:")
                c.setFont("Helvetica-Bold", 12)
                c.drawRightString(x_right_value, y_otros - 20, f"{self.factura_data.get('Monto Total', '0.00')}")
                
                # Fecha de emisión centrada debajo de las cajas
                c.setFont("Helvetica", 9)
                c.drawCentredString(width / 2, y_otros - altura_seccion_final - 15, f"Fecha de Emisión: {self.factura_data.get('Fecha Emisión', 'No especificada')}")

            # Dibujar las dos facturas en la hoja
            dibujar_factura(height)
            dibujar_factura(mitad_altura)
            c.save()

            QMessageBox.information(None, "Éxito", f"Factura generada en: {output_path}")
            os.startfile(output_path)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo generar el PDF: {e}")