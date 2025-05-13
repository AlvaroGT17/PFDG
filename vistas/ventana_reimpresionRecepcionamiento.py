"""
Módulo para la ventana de reimpresión de recepcionamientos en formato PDF.

Esta interfaz permite visualizar una tabla con los documentos generados
durante el proceso de recepcionamiento, y ofrece opciones para reenviarlos,
imprimirlos o abrirlos desde el sistema de archivos.
"""

import os
import webbrowser
from datetime import datetime
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox
)
from utilidades.rutas import obtener_ruta_absoluta


class VentanaReimpresionRecepcionamiento(QWidget):
    """
    Ventana de PySide6 que permite la gestión visual de documentos PDF
    generados en recepcionamientos anteriores.

    Aporta funcionalidades para abrir, reenviar e imprimir dichos documentos.
    """

    def __init__(self, nombre_usuario, rol_usuario, volver_callback):
        """
        Inicializa la ventana con la información del usuario y función de retorno.

        :param nombre_usuario: Nombre del usuario activo.
        :param rol_usuario: Rol actual del usuario.
        :param volver_callback: Función a ejecutar al pulsar "Volver".
        """
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario
        self.volver_callback = volver_callback

        self.setWindowTitle("Reimpresión de recepcionamientos")
        self.setMinimumSize(1000, 600)

        self.init_ui()
        self.cargar_documentos()

        ruta_css = obtener_ruta_absoluta("css/reimpresionRecepcionamiento.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        """
        Construye y organiza los componentes visuales de la interfaz.
        """
        layout_principal = QVBoxLayout()

        titulo = QLabel("Reimpresión de recepcionamientos")
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
        self.btn_imprimir = QToolButton()
        self.btn_volver = QToolButton()

        self.btn_enviar.setText("Enviar")
        self.btn_imprimir.setText("Imprimir")
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

        self.btn_enviar.setObjectName("btn-enviar")
        self.btn_imprimir.setObjectName("btn-imprimir")
        self.btn_volver.setObjectName("btn-volver")

        layout_botones.addWidget(self.btn_enviar)
        layout_botones.addWidget(self.btn_imprimir)
        layout_botones.addWidget(self.btn_volver)

        layout_principal.addLayout(layout_botones)
        self.setLayout(layout_principal)

        self.btn_volver.clicked.connect(self.volver_callback)

    def cargar_documentos(self):
        """
        Escanea la carpeta `documentos/recepcionamientos` en busca de archivos PDF,
        organizándolos por carpeta (normalmente con nombre de mes).
        """
        print("🔄 Cargando documentos de recepcionamiento...")
        ruta_base = obtener_ruta_absoluta("documentos/recepcionamientos")
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
                    try:
                        fecha = datetime.strptime(nombre_carpeta, "%Y-%m")
                        mes_legible = fecha.strftime("%B %Y").capitalize()
                    except ValueError:
                        mes_legible = nombre_carpeta.capitalize()

                    filas.append((mes_legible, archivo, ruta_completa))

        self.tabla.setRowCount(len(filas))
        for fila_idx, (mes, nombre_archivo, ruta) in enumerate(filas):
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(mes))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre_archivo))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(ruta))

    def abrir_documento_seleccionado(self, fila, columna):
        """
        Abre el documento PDF asociado a la fila seleccionada de la tabla.

        :param fila: Índice de la fila seleccionada.
        :param columna: Índice de la columna seleccionada (no se utiliza).
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
