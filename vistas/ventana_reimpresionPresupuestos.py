"""
Módulo para la ventana de reimpresión de presupuestos en formato PDF.

Permite a los usuarios consultar, abrir, reenviar o imprimir documentos generados
durante la creación de presupuestos, accediendo a ellos por carpetas organizadas por mes.

La interfaz presenta una tabla con todos los archivos PDF detectados y herramientas
para su gestión visual.
"""

import os
import webbrowser
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox, QToolButton
)
from utilidades.rutas import obtener_ruta_absoluta


class VentanaReimpresionPresupuestos(QWidget):
    """
    Ventana para gestionar la reimpresión de presupuestos en PDF.

    Esta interfaz ofrece funciones para:
    - Mostrar todos los presupuestos disponibles.
    - Reenviar presupuestos seleccionados.
    - Imprimirlos o abrirlos con doble clic.
    - Volver al menú anterior con un callback personalizado.

    Atributos:
        nombre_usuario (str): Nombre del usuario activo.
        rol_usuario (str): Rol del usuario (ej. "Administrador").
        volver_callback (function): Función ejecutada al pulsar el botón "Volver".
        tabla (QTableWidget): Tabla que muestra los documentos PDF.
        btn_enviar (QToolButton): Botón para enviar documentos.
        btn_imprimir (QToolButton): Botón para imprimir documentos.
        btn_volver (QToolButton): Botón para volver a la ventana anterior.
    """

    def __init__(self, nombre_usuario, rol_usuario, volver_callback, parent=None):
        """
        Constructor de la ventana de reimpresión.

        Configura los estilos, estructura visual y carga automática de documentos PDF.

        Args:
            nombre_usuario (str): Nombre del usuario que accede a la ventana.
            rol_usuario (str): Rol del usuario actual.
            volver_callback (function): Función que se ejecuta al hacer clic en "Volver".
            parent (QWidget, optional): Widget padre (usualmente None).
        """
        super().__init__(parent)
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario
        self.volver_callback = volver_callback

        self.setWindowTitle("Reimpresión de presupuestos")
        self.setMinimumSize(1000, 600)

        self.init_ui()
        self.cargar_documentos()

        ruta_css = obtener_ruta_absoluta("css/reimpresionPresupuestos.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        """
        Configura y organiza todos los elementos gráficos de la ventana.

        Incluye:
        - Título superior con estilo.
        - Tabla para mostrar los documentos PDF.
        - Botones para enviar, imprimir o volver, con iconos integrados.
        """
        layout_principal = QVBoxLayout()

        titulo = QLabel("Reimpresión de presupuestos")
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

        self.btn_enviar = QToolButton()
        self.btn_enviar.setText("Enviar")

        self.btn_imprimir = QToolButton()
        self.btn_imprimir.setText("Imprimir")

        self.btn_volver = QToolButton()
        self.btn_volver.setText("Volver")

        ruta_iconos = obtener_ruta_absoluta("img")
        self.btn_enviar.setIcon(QIcon(os.path.join(ruta_iconos, "enviar.png")))
        self.btn_imprimir.setIcon(
            QIcon(os.path.join(ruta_iconos, "imprimir.png")))
        self.btn_volver.setIcon(QIcon(os.path.join(ruta_iconos, "volver.png")))

        for btn in [self.btn_enviar, self.btn_imprimir, self.btn_volver]:
            btn.setIconSize(QSize(48, 48))
            btn.setStyleSheet("text-align: center;")
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones.addWidget(self.btn_enviar)
        layout_botones.addWidget(self.btn_imprimir)
        layout_botones.addWidget(self.btn_volver)

        layout_principal.addLayout(layout_botones)
        self.setLayout(layout_principal)

        self.btn_volver.clicked.connect(self.volver_callback)

    def cargar_documentos(self):
        """
        Carga y lista todos los documentos PDF disponibles en la carpeta de presupuestos.

        Escanea la ruta `documentos/presupuestos` en busca de archivos PDF,
        y los agrupa según el nombre de la carpeta contenedora, que representa el mes.
        """
        print("🔄 Cargando documentos de presupuestos...")
        ruta_base = obtener_ruta_absoluta("documentos/presupuestos")
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
            columna (int): Índice de la columna (no utilizado, pero requerido por la señal).
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
