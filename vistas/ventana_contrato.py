"""
Módulo para la visualización de contratos de compraventa en formato HTML.

Esta ventana permite al usuario visualizar un contrato generado previamente
y tomar una decisión: aceptarlo (lo que puede desencadenar una acción adicional)
o cancelarlo cerrando la ventana. El contrato se carga desde un archivo HTML.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from utilidades.rutas import obtener_ruta_absoluta


class VentanaContrato(QWidget):
    """
    Ventana para mostrar un contrato de compra o venta en formato HTML.

    Permite al usuario visualizar el contenido del contrato generado, aceptar su contenido
    o cancelar la operación. Al aceptar, se puede ejecutar una acción personalizada
    mediante una función de callback.

    Atributos:
        vista_previa (QTextBrowser): Visor del contenido HTML del contrato.
        boton_aceptar (QPushButton): Botón para aceptar el contrato.
        boton_volver (QPushButton): Botón para cerrar la ventana sin aceptar.
        callback_aceptar (func): Función que se ejecuta si el contrato es aceptado.
        tipo_operacion (str): Tipo de contrato: "compra" o "venta".
    """

    def __init__(self, html_path, tipo_operacion, callback_aceptar=None):
        """
        Inicializa la ventana de contrato.

        Args:
            html_path (str): Ruta al archivo HTML que contiene el contrato.
            tipo_operacion (str): Indica si es un contrato de "compra" o "venta".
            callback_aceptar (function, optional): Función que se ejecutará si se acepta el contrato.
                                                   Recibe el tipo de operación como argumento.
        """
        super().__init__()
        self.setWindowTitle(
            f"Contrato de {'COMPRA' if tipo_operacion == 'compra' else 'VENTA'} - ReyBoxes")
        self.setFixedSize(850, 650)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setObjectName("ventana_contrato")
        self.callback_aceptar = callback_aceptar
        self.tipo_operacion = tipo_operacion

        layout = QVBoxLayout(self)

        # Visor del contrato
        self.vista_previa = QTextBrowser()
        self.vista_previa.setOpenExternalLinks(True)
        self.vista_previa.setStyleSheet(
            "background-color: white; padding: 10px; border: 1px solid gray;"
        )
        with open(html_path, "r", encoding="utf-8") as f:
            self.vista_previa.setHtml(f.read())
        layout.addWidget(self.vista_previa)

        # Botones de acción
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
        """
        Ejecuta la función callback si fue proporcionada y cierra la ventana.

        La función callback recibe como argumento el tipo de operación: "compra" o "venta".
        """
        if self.callback_aceptar:
            self.callback_aceptar(self.tipo_operacion)
        self.close()
