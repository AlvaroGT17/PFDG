"""
Módulo para la ventana de reimpresión de recepcionamientos en formato PDF.

Esta interfaz permite visualizar una tabla con los documentos generados
durante el proceso de recepcionamiento, y ofrece opciones para reenviarlos,
imprimirlos o abrirlos desde el sistema de archivos.

Los archivos se agrupan por carpetas, habitualmente con nombres de mes (por ejemplo, "2024-09"),
y se muestran en una tabla interactiva con opciones accesibles al usuario.
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
    Ventana gráfica para gestionar documentos PDF de recepcionamientos.

    Esta ventana permite:
    - Listar documentos agrupados por mes.
    - Abrir los archivos con doble clic.
    - Enviarlos o imprimirlos con botones accesibles.
    - Volver a la pantalla anterior mediante un callback.

    Atributos:
        nombre_usuario (str): Nombre del usuario actual.
        rol_usuario (str): Rol asignado al usuario (p.ej., Administrador).
        volver_callback (function): Función a ejecutar al pulsar el botón "Volver".
        tabla (QTableWidget): Tabla que muestra los documentos encontrados.
        btn_enviar (QToolButton): Botón para reenviar el documento seleccionado.
        btn_imprimir (QToolButton): Botón para imprimir el documento.
        btn_volver (QToolButton): Botón para volver al menú anterior.
    """

    def __init__(self, nombre_usuario, rol_usuario, volver_callback):
        """
        Constructor de la ventana.

        Configura los elementos gráficos, aplica estilos y carga los documentos disponibles.

        Args:
            nombre_usuario (str): Nombre del usuario activo en la sesión.
            rol_usuario (str): Rol del usuario actual (por ejemplo, "Administrativo").
            volver_callback (function): Función a ejecutar al pulsar el botón de volver.
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
        Construye y organiza todos los componentes visuales de la interfaz.

        Incluye:
        - Un título centrado.
        - Una tabla con columnas: mes, nombre de archivo, ruta (oculta).
        - Tres botones: Enviar, Imprimir y Volver, con iconos y estilo.
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
        Escanea recursivamente la carpeta `documentos/recepcionamientos` para localizar
        archivos PDF y cargarlos en la tabla.

        Los documentos se agrupan visualmente por el nombre de la carpeta superior (que suele ser un mes en formato YYYY-MM).
        Si el nombre puede convertirse en una fecha, se muestra como "Mes Año" (ej.: "Marzo 2024").
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
        Intenta abrir el documento PDF asociado a la fila seleccionada con la aplicación predeterminada del sistema.

        Args:
            fila (int): Índice de la fila seleccionada en la tabla.
            columna (int): Índice de la columna donde se hizo doble clic (no se usa).
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
                QMessageBox.warning(
                    self, "No encontrado", "El archivo seleccionado no existe.")
