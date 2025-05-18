"""
Módulo de interfaz para visualizar el historial de fichajes en el sistema ReyBoxes.

Permite mostrar registros de entrada y salida de empleados en una tabla,
y ofrece funcionalidades para exportar los datos a formatos CSV y PDF.
Incluye un botón para volver a la pantalla principal del sistema.

La interfaz está diseñada para adaptarse tanto a usuarios comunes como a administradores.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QToolButton
from utilidades.rutas import obtener_ruta_absoluta


class VentanaHistorial(QWidget):
    """
    Ventana que muestra el historial de fichajes del sistema ReyBoxes.

    Esta interfaz está diseñada tanto para usuarios comunes como para administradores.
    Permite visualizar una tabla con registros de fichajes, así como exportarlos a CSV o PDF.
    También incluye un botón para regresar al menú principal.

    Atributos:
        es_admin (bool): Determina si el usuario tiene privilegios de administrador.
        tabla (QTableWidget): Tabla que contiene los registros de fichajes.
        boton_csv (QToolButton): Botón para exportar el historial a CSV.
        boton_pdf (QToolButton): Botón para exportar el historial a PDF.
        boton_volver (QToolButton): Botón para regresar a la ventana anterior.
    """

    def __init__(self, es_admin=False):
        """
        Inicializa la ventana de historial de fichajes.

        Args:
            es_admin (bool): Indica si el usuario tiene rol de administrador (afecta el comportamiento futuro).
        """
        super().__init__()
        self.es_admin = es_admin
        self.setWindowTitle("Historial de Fichajes")
        self.setFixedSize(800, 580)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setObjectName("ventana_historial")

        ruta_css = obtener_ruta_absoluta("css/historial.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.inicializar_ui()

    def inicializar_ui(self):
        """
        Configura y construye la interfaz gráfica:
        - Título de la ventana.
        - Tabla de fichajes con encabezados y estilo personalizado.
        - Botones para exportar a CSV, exportar a PDF y volver al menú.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titulo = QLabel("Historial de Fichajes")
        titulo.setObjectName("titulo_historial")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(
            ["Fecha y hora", "Tipo", "Empleado"])
        self.tabla.setObjectName("tabla_fichajes")
        self.tabla.verticalHeader().setVisible(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setColumnWidth(0, 200)
        self.tabla.setColumnWidth(1, 150)
        self.tabla.setColumnWidth(2, 150)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        layout.addWidget(self.tabla)

        # Botón Exportar CSV
        self.boton_csv = QToolButton()
        self.boton_csv.setText("Exportar CSV")
        self.boton_csv.setObjectName("boton_exportar_csv")
        self.boton_csv.setIcon(QIcon(obtener_ruta_absoluta("img/csv.png")))
        self.boton_csv.setIconSize(QSize(48, 48))
        self.boton_csv.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Botón Exportar PDF
        self.boton_pdf = QToolButton()
        self.boton_pdf.setText("Exportar PDF")
        self.boton_pdf.setObjectName("boton_exportar_pdf")
        self.boton_pdf.setIcon(QIcon(obtener_ruta_absoluta("img/pdf.png")))
        self.boton_pdf.setIconSize(QSize(48, 48))
        self.boton_pdf.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Botón Volver
        self.boton_volver = QToolButton()
        self.boton_volver.setText("Volver")
        self.boton_volver.setObjectName("boton_volver")
        self.boton_volver.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_volver.setIconSize(QSize(48, 48))
        self.boton_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(30)
        layout_botones.addStretch()
        layout_botones.addWidget(self.boton_csv)
        layout_botones.addWidget(self.boton_pdf)
        layout_botones.addWidget(self.boton_volver)
        layout_botones.addStretch()

        layout.addLayout(layout_botones)

    def cargar_datos(self, fichajes):
        """
        Carga los registros de fichajes en la tabla.

        Args:
            fichajes (list): Lista de tuplas con (fecha_hora, tipo, empleado).
                             `fecha_hora` debe ser un objeto datetime.
        """
        self.tabla.setRowCount(len(fichajes))
        for fila, fichaje in enumerate(fichajes):
            fecha_hora = QTableWidgetItem(
                fichaje[0].strftime("%Y-%m-%d %H:%M:%S"))
            tipo = QTableWidgetItem(fichaje[1])
            empleado = QTableWidgetItem(fichaje[2])

            self.tabla.setItem(fila, 0, fecha_hora)
            self.tabla.setItem(fila, 1, tipo)
            self.tabla.setItem(fila, 2, empleado)

            # Colores por tipo de fichaje
            if fichaje[1] == "ENTRADA":
                color = QColor("#fff8cc")  # amarillo claro
            elif fichaje[1] == "SALIDA":
                color = QColor("#e0f0ff")  # azul claro
            else:
                color = None

            if color:
                for col in range(3):
                    self.tabla.item(fila, col).setBackground(color)
