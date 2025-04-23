import os
from PySide6.QtGui import QIcon
from utilidades.rutas import obtener_ruta_absoluta
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QRadioButton,
    QLineEdit, QPushButton, QButtonGroup, QMessageBox
)


class VentanaCorreoConfirmacion(QDialog):
    def __init__(self, correo_defecto, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enviar contrato por correo")
        self.setMinimumWidth(400)
        self.correo_seleccionado = None
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.aplicar_estilos_personalizados()

        layout = QVBoxLayout()

        mensaje = QLabel("¿A qué correo deseas enviar el contrato?")
        layout.addWidget(mensaje)

        self.grupo_botones = QButtonGroup(self)

        self.radio_defecto = QRadioButton(
            f"Usar correo del cliente ({correo_defecto})")
        self.radio_personalizado = QRadioButton("Usar correo personalizado")

        self.grupo_botones.addButton(self.radio_defecto)
        self.grupo_botones.addButton(self.radio_personalizado)

        layout.addWidget(self.radio_defecto)
        layout.addWidget(self.radio_personalizado)

        self.input_personalizado = QLineEdit()
        self.input_personalizado.setPlaceholderText(
            "Introduce el correo personalizado...")
        self.input_personalizado.setEnabled(False)
        layout.addWidget(self.input_personalizado)

        self.radio_personalizado.toggled.connect(
            lambda checked: self.input_personalizado.setEnabled(checked))

        boton_ok = QPushButton("Enviar")
        boton_ok.clicked.connect(self.aceptar_envio)
        layout.addWidget(boton_ok)

        self.setLayout(layout)

    def aceptar_envio(self):
        if self.radio_defecto.isChecked():
            self.correo_seleccionado = "DEFECTO"
            self.accept()
        elif self.radio_personalizado.isChecked():
            correo = self.input_personalizado.text().strip()
            if not correo:
                QMessageBox.warning(self, "Correo vacío",
                                    "Debes introducir un correo personalizado.")
                return
            self.correo_seleccionado = correo
            self.accept()
        else:
            QMessageBox.warning(self, "Sin selección",
                                "Debes seleccionar una opción para continuar.")

    def aplicar_estilos_personalizados(self):
        try:
            ruta_css = os.path.join("css", "correo_confirmacion.css")
            with open(ruta_css, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"❌ No se pudo cargar el CSS de la ventana de correo: {e}")
