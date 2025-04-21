from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from utilidades.rutas import obtener_ruta_absoluta


class VentanaContrato(QWidget):
    def __init__(self, html_path, tipo_operacion, callback_aceptar=None):
        super().__init__()
        self.setWindowTitle(
            f"Contrato de {'COMPRA' if tipo_operacion == 'compra' else 'VENTA'} - ReyBoxes")
        self.setFixedSize(850, 650)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setObjectName("ventana_contrato")
        self.callback_aceptar = callback_aceptar
        self.tipo_operacion = tipo_operacion  # 👈 ¡Guarda el tipo!

        layout = QVBoxLayout(self)

        self.vista_previa = QTextBrowser()
        self.vista_previa.setOpenExternalLinks(True)
        self.vista_previa.setStyleSheet(
            "background-color: white; padding: 10px; border: 1px solid gray;"
        )
        with open(html_path, "r", encoding="utf-8") as f:
            self.vista_previa.setHtml(f.read())
        layout.addWidget(self.vista_previa)

        botones = QHBoxLayout()
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setToolTip("Volver sin aceptar el contrato")
        self.boton_volver.clicked.connect(self.close)

        self.boton_aceptar = QPushButton("Aceptar contrato")
        self.boton_aceptar.setObjectName("boton_aceptar_contrato")
        self.boton_aceptar.setToolTip(
            "Aceptar el contrato y continuar con las acciones seleccionadas")
        self.boton_aceptar.clicked.connect(self.aceptar_contrato)

        botones.addStretch()
        botones.addWidget(self.boton_volver)
        botones.addWidget(self.boton_aceptar)
        layout.addLayout(botones)

    def aceptar_contrato(self):
        if self.callback_aceptar:
            self.callback_aceptar(self.tipo_operacion)  # ✅ Pasa el tipo
        self.close()
