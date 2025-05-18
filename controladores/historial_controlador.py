"""
Controlador del historial de fichajes de empleados.

Este módulo permite:
- Visualizar los fichajes realizados por el usuario o todos los empleados (modo administrador).
- Exportar el historial como CSV o como informe PDF.
- Agrupar los datos por usuario con información del periodo registrado.

Requiere:
- `reportlab` para la generación de PDFs.
- `VentanaHistorial` como interfaz gráfica.
- Funciones del modelo para obtener datos de fichajes.
"""
import csv
import os
from datetime import datetime

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

from modelos.historial_consultas import obtener_fichajes_personales, obtener_fichajes_globales, obtener_nombre_usuario
from utilidades.rutas import obtener_ruta_absoluta
from vistas.ventana_historial import VentanaHistorial
from utilidades.canvas_con_paginas import NumeroPaginasCanvas


class HistorialControlador(QObject):
    """
    Controlador de la ventana de historial de fichajes.

    Muestra los fichajes del usuario o de todos los empleados (si es administrador),
    permitiendo su exportación a CSV o PDF.
    """

    def __init__(self, usuario_id, es_admin=False):
        """
        Inicializa el controlador con los parámetros del usuario.

        Args:
            usuario_id (int): ID del usuario actual.
            es_admin (bool): Indica si el usuario tiene permisos de administrador.
        """
        super().__init__()
        self.usuario_id = usuario_id
        self.es_admin = es_admin
        self.ventana = VentanaHistorial(es_admin=es_admin)
        self.ventana.boton_csv.clicked.connect(self.exportar_csv)
        self.ventana.boton_pdf.clicked.connect(self.exportar_pdf)
        self.ventana.boton_volver.clicked.connect(self.ventana.close)
        self.cargar_datos()

    def mostrar(self):
        """Muestra la ventana de historial."""
        self.ventana.show()

    def cargar_datos(self):
        """
        Carga los datos de fichajes desde la base de datos.
        Si es administrador, obtiene todos los registros.
        En caso contrario, carga solo los registros del usuario actual.
        """
        if self.es_admin:
            # Administrador: obtiene todos los fichajes
            self.fichajes = obtener_fichajes_globales()
        else:
            # Usuario normal: obtiene su nombre real y sus propios fichajes
            nombre_usuario = obtener_nombre_usuario(self.usuario_id)
            fichajes_personales = obtener_fichajes_personales(self.usuario_id)
            # Se añaden el nombre real en lugar de "Tú"
            self.fichajes = [(f[0], f[1], nombre_usuario)
                             for f in fichajes_personales]

        # Carga los datos en la tabla
        self.ventana.cargar_datos(self.fichajes)

    def exportar_csv(self):
        """
        Exporta los datos visibles en la tabla a un archivo CSV.

        Abre un cuadro de diálogo para seleccionar la ubicación y nombre del archivo.
        Muestra mensajes de éxito o error mediante QMessageBox.
        """
        ruta, _ = QFileDialog.getSaveFileName(
            self.ventana,
            "Guardar CSV",
            "historial_fichajes.csv",
            "Archivos CSV (*.csv)"
        )

        if not ruta:
            return  # Cancelado

        try:
            with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo, delimiter=";")
                writer.writerow(["Fecha y hora", "Tipo", "Empleado"])

                for fila in range(self.ventana.tabla.rowCount()):
                    fecha = self.ventana.tabla.item(fila, 0).text()
                    tipo = self.ventana.tabla.item(fila, 1).text()
                    empleado = self.ventana.tabla.item(fila, 2).text()
                    writer.writerow([fecha, tipo, empleado])

            QMessageBox.information(
                self.ventana, "Exportación CSV", "✅ Historial exportado correctamente como CSV.")
        except Exception as e:
            QMessageBox.critical(
                self.ventana, "Error", f"❌ Error al exportar CSV:\n{e}")

    def exportar_pdf(self):
        """
        Genera un informe PDF con los datos de fichajes cargados.

        El informe contiene:
        - Encabezado con logo y datos de empresa.
        - Agrupación por usuario (si es administrador).
        - Tabla con los fichajes.
        - Pie de página con número de página y datos corporativos.
        """
        try:
            ruta, _ = QFileDialog.getSaveFileName(
                self.ventana, "Guardar PDF", "historial_fichajes.pdf", "PDF Files (*.pdf)"
            )
            if not ruta:
                return

            doc = SimpleDocTemplate(
                ruta, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=100, bottomMargin=50)
            elementos = []
            estilos = getSampleStyleSheet()

            # Cabecera
            ruta_logo = obtener_ruta_absoluta("img/logo.jpg")
            logo = Image(ruta_logo, width=4*cm, height=4*cm)

            datos_empresa = Paragraph(
                "<b>ReyBoxes</b><br/>"
                "Pol.Ind. Cabanillas 1<br/>"
                "C/Fco. Medina y Mendoza P.1 Nv65<br/>"
                "C.P. 19171 Cabanillas (Guadalajara)", estilos["Normal"]
            )

            encabezado = [[logo, datos_empresa]]
            tabla_encabezado = Table(encabezado, colWidths=[4.5*cm, 12*cm])
            tabla_encabezado.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]))
            elementos.append(tabla_encabezado)
            elementos.append(Spacer(1, 12))

            titulo = Paragraph(
                "<b>INFORME DE CONTROL DE FICHAJE DE EMPLEADOS</b>", estilos["Heading2"])
            elementos.append(titulo)
            elementos.append(Spacer(1, 12))

            if self.es_admin:
                # Agrupar por nombre
                empleados = {}
                for f in self.fichajes:
                    empleados.setdefault(f[2], []).append(f)

                for nombre, fichajes in empleados.items():
                    periodo = self.obtener_periodo(fichajes)
                    parrafo = Paragraph(
                        f"<b>Nombre del trabajador:</b> {nombre} &nbsp;&nbsp;&nbsp;&nbsp;"
                        f"<b>Periodo del informe:</b> {periodo}", estilos["Normal"])
                    elementos.append(parrafo)
                    elementos.append(Spacer(1, 6))
                    elementos.append(self.crear_tabla_fichajes(fichajes))
                    elementos.append(Spacer(1, 12))
            else:
                periodo = self.obtener_periodo(self.fichajes)
                parrafo = Paragraph(
                    f"<b>Nombre del trabajador:</b> Tú &nbsp;&nbsp;&nbsp;&nbsp;"
                    f"<b>Periodo del informe:</b> {periodo}", estilos["Normal"])
                elementos.append(parrafo)
                elementos.append(Spacer(1, 6))
                elementos.append(self.crear_tabla_fichajes(self.fichajes))

            def pie_pagina(canvas, doc):
                canvas.saveState()
                canvas.setStrokeColor(colors.HexColor("#d90429"))
                canvas.setLineWidth(1)
                canvas.line(30, 50, A4[0] - 30, 50)

                canvas.setFont("Helvetica", 9)
                canvas.drawString(
                    30, 35, "ReyBoxes - Taller mecánica y mantenimiento")
                canvas.drawRightString(
                    A4[0] - 30, 35, f"Pag {doc.page} / {doc.page}")
                canvas.restoreState()

            doc.build(elementos, canvasmaker=NumeroPaginasCanvas)

            QMessageBox.information(
                self.ventana, "Exportación PDF", "✅ Informe PDF generado correctamente.")

        except Exception as e:
            QMessageBox.critical(
                self.ventana, "Error", f"❌ Error al generar PDF:\n{e}")

    def crear_tabla_fichajes(self, datos):
        """
        Crea una tabla `reportlab` con los datos de fichajes.

        Args:
            datos (list): Lista de tuplas (fecha, tipo, nombre).

        Returns:
            Table: Objeto tabla listo para ser insertado en el PDF.
        """
        estilos = getSampleStyleSheet()
        filas = [["Fecha y hora", "Tipo", "Empleado"]] + [[
            r[0].strftime("%Y-%m-%d %H:%M:%S"), r[1], r[2]
        ] for r in datos]

        tabla = Table(filas, repeatRows=1, hAlign='LEFT',
                      colWidths=[6.5*cm, 3.5*cm, 5*cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d90429")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.whitesmoke, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        return tabla

    def obtener_periodo(self, datos):
        """
        Calcula el periodo mínimo y máximo de fechas de fichajes.

        Args:
            datos (list): Lista de registros de fichajes.

        Returns:
            str: Periodo en formato 'de DD/MM/YYYY a DD/MM/YYYY'.
        """
        if not datos:
            return "-"
        fechas = [r[0] for r in datos]
        return f"de {min(fechas).strftime('%d/%m/%Y')} a {max(fechas).strftime('%d/%m/%Y')}"
