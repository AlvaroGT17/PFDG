"""
Módulo de interfaz gráfica para la reimpresión de documentos de ventas.

Contiene la clase VentanaReimpresionVentas, que permite al usuario visualizar
una lista de contratos de venta generados, con opciones para enviarlos por correo,
imprimirlos o abrirlos directamente desde la aplicación.

Los documentos se cargan dinámicamente desde la carpeta de ventas, agrupados por mes.
La interfaz está diseñada para facilitar la gestión y reutilización de documentos PDF.
"""

import os
import webbrowser
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox
)
from utilidades.rutas import obtener_ruta_absoluta


class VentanaReimpresionVentas(QWidget):
    """
    Ventana gráfica para consultar y gestionar documentos de ventas en PDF.

    Esta interfaz permite al usuario:
    - Visualizar una tabla de documentos agrupados por mes.
    - Abrir documentos directamente desde la aplicación.
    - Reenviar o imprimir los documentos seleccionados.
    - Volver a la pantalla anterior mediante una función callback.

    Atributos:
        nombre_usuario (str): Nombre del usuario actual.
        rol_usuario (str): Rol del usuario actual.
        volver_callback (function): Función que se ejecuta al pulsar el botón "Volver".
        tabla (QTableWidget): Tabla principal que muestra los documentos cargados.
        btn_enviar (QPushButton): Botón para reenviar el documento.
        btn_imprimir (QPushButton): Botón para imprimir el documento.
        btn_volver (QPushButton): Botón para volver a la ventana anterior.
    """

    def __init__(self, nombre_usuario, rol_usuario, volver_callback):
        """
        Constructor de la ventana.

        Configura la ventana, su estilo, y carga los documentos PDF desde el directorio definido.

        Args:
            nombre_usuario (str): Nombre del usuario activo.
            rol_usuario (str): Rol del usuario (usado para posibles permisos).
            volver_callback (function): Función que se ejecuta al pulsar el botón "Volver".
        """
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario
        self.volver_callback = volver_callback

        self.setWindowTitle("Reimpresión de ventas")
        self.setMinimumSize(1000, 600)
        self.setObjectName("ventana_reimpresion")

        self.init_ui()
        self.cargar_documentos()

        ruta_css = obtener_ruta_absoluta("css/reimpresionVentas.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        """
        Crea y organiza los elementos visuales de la interfaz gráfica.

        Incluye:
        - Título superior.
        - Tabla para mostrar los documentos PDF encontrados.
        - Botones inferiores para reenviar, imprimir o volver.
        """
        layout_principal = QVBoxLayout()

        titulo = QLabel("Reimpresión de ventas")
        titulo.setObjectName("titulo-reimpresion")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(
            ["Mes", "Nombre del Documento", "Ruta"])
        self.tabla.setColumnHidden(2, True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        layout_principal.addWidget(self.tabla)

        self.tabla.cellDoubleClicked.connect(self.abrir_documento_seleccionado)

        layout_botones = QHBoxLayout()
        self.btn_enviar = QPushButton("  Enviar")
        self.btn_imprimir = QPushButton("  Imprimir")
        self.btn_volver = QPushButton("  Volver")

        ruta_iconos = obtener_ruta_absoluta("img")
        self.btn_enviar.setIcon(QIcon(os.path.join(ruta_iconos, "enviar.png")))
        self.btn_imprimir.setIcon(
            QIcon(os.path.join(ruta_iconos, "imprimir.png")))
        self.btn_volver.setIcon(QIcon(os.path.join(ruta_iconos, "volver.png")))

        for btn in [self.btn_enviar, self.btn_imprimir, self.btn_volver]:
            btn.setIconSize(QSize(48, 48))
            btn.setStyleSheet("text-align: center;")
            btn.setFixedHeight(90)

        layout_botones.addWidget(self.btn_enviar)
        layout_botones.addWidget(self.btn_imprimir)
        layout_botones.addWidget(self.btn_volver)

        layout_principal.addLayout(layout_botones)
        self.setLayout(layout_principal)

        self.btn_volver.clicked.connect(self.volver_callback)

    def cargar_documentos(self):
        """
        Carga todos los documentos PDF desde la carpeta de ventas y los agrega a la tabla.

        Recorre recursivamente las subcarpetas de la ruta 'documentos/ventas',
        agrupando los archivos por nombre de carpeta (usado como nombre de mes).

        Si no se encuentra la carpeta base, se imprime un aviso por consola.
        """
        print("🔄 Cargando documentos de ventas...")
        ruta_base = obtener_ruta_absoluta("documentos/ventas")
        if not os.path.exists(ruta_base):
            print("❌ Carpeta no encontrada:", ruta_base)
            return

        filas = []
        for raiz, _, archivos in os.walk(ruta_base):
            for archivo in archivos:
                if archivo.lower().endswith(".pdf"):
                    ruta_completa = os.path.join(raiz, archivo)
                    print(f"📄 Documento detectado: {ruta_completa}")
                    nombre_carpeta = os.path.basename(
                        os.path.dirname(ruta_completa))
                    mes_legible = nombre_carpeta.replace("_", " ").capitalize()
                    filas.append((mes_legible, archivo, ruta_completa))

        self.tabla.setRowCount(len(filas))
        for fila_idx, (mes, nombre_archivo, ruta) in enumerate(filas):
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(mes))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre_archivo))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(ruta))

    def abrir_documento_seleccionado(self, fila, columna):
        """
        Abre el documento PDF correspondiente a la fila seleccionada al hacer doble clic.

        Args:
            fila (int): Índice de la fila seleccionada.
            columna (int): Índice de la columna donde se ha hecho doble clic.
        """
        ruta_item = self.tabla.item(fila, 2)
        if ruta_item:
            ruta = ruta_item.text()
            if os.path.exists(ruta):
                try:
                    webbrowser.open_new(ruta)
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"No se pudo abrir el documento:\n{str(e)}")
            else:
                QMessageBox.warning(self, "No encontrado",
                                    "El archivo seleccionado no existe.")
