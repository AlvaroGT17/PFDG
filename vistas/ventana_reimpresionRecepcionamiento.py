from PySide6.QtWidgets import (
    QWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox
)
from PySide6.QtCore import Qt, QSize
import os
import webbrowser
from datetime import datetime
from utilidades.rutas import obtener_ruta_absoluta
from PySide6.QtGui import QIcon


class VentanaReimpresionRecepcionamiento(QWidget):
    def __init__(self, nombre_usuario, rol_usuario, volver_callback):
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
        layout_principal = QVBoxLayout()

        # Título
        titulo = QLabel("Reimpresión de recepcionamientos")
        titulo.setObjectName("titulo-reimpresion")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        # Tabla
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

        # Doble clic sobre la fila para abrir el PDF
        self.tabla.cellDoubleClicked.connect(self.abrir_documento_seleccionado)

        # Botones
        layout_botones = QHBoxLayout()

        self.btn_enviar = QToolButton()
        self.btn_imprimir = QToolButton()
        self.btn_volver = QToolButton()

        self.btn_enviar.setText("Enviar")
        self.btn_imprimir.setText("Imprimir")
        self.btn_volver.setText("Volver")

        ruta_iconos = obtener_ruta_absoluta("img")

        self.btn_enviar.setIcon(
            QIcon(os.path.join(ruta_iconos, "enviar.png")))
        self.btn_imprimir.setIcon(
            QIcon(os.path.join(ruta_iconos, "imprimir.png")))
        self.btn_volver.setIcon(
            QIcon(os.path.join(ruta_iconos, "volver.png")))

        self.btn_enviar.setIconSize(QSize(48, 48))
        self.btn_imprimir.setIconSize(QSize(48, 48))
        self.btn_volver.setIconSize(QSize(48, 48))

        self.btn_enviar.setStyleSheet("text-align: center;")
        self.btn_enviar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.btn_imprimir.setStyleSheet("text-align: center;")
        self.btn_imprimir.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.btn_volver.setStyleSheet("text-align: center;")
        self.btn_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.btn_enviar.setObjectName("btn-enviar")
        self.btn_imprimir.setObjectName("btn-imprimir")
        self.btn_volver.setObjectName("btn-volver")

        layout_botones.addWidget(self.btn_enviar)
        layout_botones.addWidget(self.btn_imprimir)
        layout_botones.addWidget(self.btn_volver)

        layout_principal.addLayout(layout_botones)
        self.setLayout(layout_principal)

        # Conexión del botón volver
        self.btn_volver.clicked.connect(self.volver_callback)

    def cargar_documentos(self):
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
