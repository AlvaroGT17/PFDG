import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QLineEdit, QPushButton, QButtonGroup, QMessageBox
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCorreoConfirmacion(QDialog):
    """
    Diálogo modal para seleccionar el correo al que se enviará un contrato.

    Ofrece al usuario dos opciones:
    - Usar el correo por defecto del cliente.
    - Introducir un correo personalizado manualmente.

    Incluye validaciones básicas y aplica un estilo visual mediante archivo CSS externo.
    """

    def __init__(self, correo_defecto, parent=None):
        """
        Inicializa la ventana de confirmación de correo.

        Parámetros:
            correo_defecto (str): Dirección de correo predefinida del cliente.
            parent (QWidget, opcional): Ventana padre del diálogo.
        """
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
        """
        Verifica la opción seleccionada y valida el campo si se elige correo personalizado.

        Si la validación es correcta, se guarda la selección y se cierra el diálogo.
        En caso de error, muestra un mensaje al usuario.
        """
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
        """
        Intenta aplicar el archivo CSS para personalizar el diseño del diálogo.
        Si no se encuentra o falla, muestra un mensaje de error en consola.
        """
        try:
            ruta_css = os.path.join("css", "correo_confirmacion.css")
            with open(ruta_css, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"❌ No se pudo cargar el CSS de la ventana de correo: {e}")
