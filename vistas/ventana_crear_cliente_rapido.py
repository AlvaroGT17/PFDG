from PySide6.QtWidgets import (
    QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCrearClienteRapido(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Nuevo cliente rápido")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(420, 320)
        self.setWindowModality(Qt.ApplicationModal)
        # Sin botón de cerrar ❌
        self.setWindowFlags(Qt.Window | Qt.MSWindowsFixedSizeDialogHint)
        self.setObjectName("ventana_crear_cliente_rapido")

        self.setup_ui()
        self.aplicar_estilos()
        self.conectar_eventos()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre (obligatorio)")
        layout.addWidget(self.input_nombre)

        self.input_apellido1 = QLineEdit()
        self.input_apellido1.setPlaceholderText(
            "Primer apellido (obligatorio)")
        layout.addWidget(self.input_apellido1)

        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("DNI (obligatorio)")
        layout.addWidget(self.input_dni)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono (obligatorio)")
        layout.addWidget(self.input_telefono)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)
        botones_layout.setAlignment(Qt.AlignCenter)

        self.boton_crear = QPushButton("Crear")
        self.boton_crear.setEnabled(False)
        self.boton_crear.setIcon(
            QIcon(obtener_ruta_absoluta("img/crear.png")))
        self.boton_crear.setToolTip("Crear nuevo cliente")

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_cancelar.setToolTip("Volver sin crear")

        botones_layout.addWidget(self.boton_crear)
        botones_layout.addWidget(self.boton_cancelar)

        layout.addLayout(botones_layout)

    def aplicar_estilos(self):
        ruta_css = obtener_ruta_absoluta("css/crear_cliente_rapido.css")
        try:
            with open(ruta_css, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"No se encontró el CSS: {ruta_css}")

    def conectar_eventos(self):
        for campo in [
            self.input_nombre,
            self.input_apellido1,
            self.input_dni,
            self.input_telefono
        ]:
            campo.textChanged.connect(self.verificar_campos)

    def verificar_campos(self):
        campos = [
            self.input_nombre.text().strip(),
            self.input_apellido1.text().strip(),
            self.input_dni.text().strip(),
            self.input_telefono.text().strip()
        ]
        self.boton_crear.setEnabled(all(campos))
