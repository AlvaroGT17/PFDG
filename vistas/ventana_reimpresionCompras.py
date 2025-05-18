"""
Módulo para la ventana de reimpresión de contratos de compra.

Permite al usuario visualizar, reenviar o imprimir contratos PDF
almacenados previamente, clasificados por carpetas mensuales.

La interfaz presenta una tabla interactiva y botones de acción
para la gestión de los documentos desde la propia aplicación.
"""

import os
import webbrowser
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox, QToolButton
)
from utilidades.rutas import obtener_ruta_absoluta


class VentanaReimpresionCompras(QWidget):
    """
    Ventana gráfica para consultar, abrir, reenviar o imprimir
    documentos PDF correspondientes a contratos de compra.

    Atributos:
        nombre_usuario (str): Nombre del usuario activo.
        rol_usuario (str): Rol actual del usuario.
        volver_callback (function): Función que se ejecuta al pulsar "Volver".
        tabla (QTableWidget): Tabla donde se listan los documentos PDF.
        btn_enviar (QToolButton): Botón para reenviar documentos.
        btn_imprimir (QToolButton): Botón para imprimir documentos.
        btn_volver (QToolButton): Botón para volver a la pantalla anterior.
    """

    def __init__(self, nombre_usuario, rol_usuario, volver_callback, parent=None):
        """
        Inicializa la ventana de reimpresión de compras.

        Args:
            nombre_usuario (str): Nombre del usuario actual.
            rol_usuario (str): Rol del usuario actual.
            volver_callback (function): Función a ejecutar al pulsar "Volver".
            parent (QWidget, optional): Widget padre si se usa desde otra ventana.
        """
        super().__init__(parent)
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario
        self.volver_callback = volver_callback

        self.setWindowTitle("Reimpresión de compras")
        self.setMinimumSize(1000, 600)
        self.setObjectName("ventana_reimpresion")

        self.init_ui()
        self.cargar_documentos()

        ruta_css = obtener_ruta_absoluta("css/reimpresionCompras.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        """
        Construye y organiza los elementos gráficos de la interfaz.

        La interfaz incluye:
        - Título superior.
        - Tabla para mostrar documentos PDF por mes.
        - Botones con iconos para reenviar, imprimir o volver.
        """
        layout_principal = QVBoxLayout()

        titulo = QLabel("Reimpresión de compras")
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
        ruta_iconos = obtener_ruta_absoluta("img")

        self.btn_enviar = QToolButton()
        self.btn_enviar.setText("Enviar")
        self.btn_enviar.setIcon(QIcon(os.path.join(ruta_iconos, "enviar.png")))
        self.btn_enviar.setObjectName("btn-enviar")

        self.btn_imprimir = QToolButton()
        self.btn_imprimir.setText("Imprimir")
        self.btn_imprimir.setIcon(
            QIcon(os.path.join(ruta_iconos, "imprimir.png")))
        self.btn_imprimir.setObjectName("btn-imprimir")

        self.btn_volver = QToolButton()
        self.btn_volver.setText("Volver")
        self.btn_volver.setIcon(QIcon(os.path.join(ruta_iconos, "volver.png")))
        self.btn_volver.setObjectName("btn-volver")

        for btn in [self.btn_enviar, self.btn_imprimir, self.btn_volver]:
            btn.setIconSize(QSize(48, 48))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones.addWidget(self.btn_enviar)
        layout_botones.addWidget(self.btn_imprimir)
        layout_botones.addWidget(self.btn_volver)

        layout_principal.addLayout(layout_botones)
        self.setLayout(layout_principal)

        self.btn_volver.clicked.connect(self.volver_callback)

    def cargar_documentos(self):
        """
        Carga los archivos PDF ubicados en la carpeta `documentos/compras`.

        Recorre las carpetas mensuales, identifica documentos PDF y los
        muestra en la tabla junto a su carpeta (mes) de origen.
        """
        print("🔄 Cargando documentos de compras...")
        ruta_base = obtener_ruta_absoluta("documentos/compras")
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
        Abre el documento PDF de la fila seleccionada con la aplicación por defecto del sistema.

        Args:
            fila (int): Fila seleccionada en la tabla.
            columna (int): Columna seleccionada (no se utiliza).
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
