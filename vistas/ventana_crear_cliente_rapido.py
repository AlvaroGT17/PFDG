"""
Módulo para la creación rápida de clientes en el sistema ReyBoxes.

Esta ventana modal permite registrar un nuevo cliente introduciendo únicamente
los datos mínimos obligatorios: nombre, primer apellido, DNI y teléfono.

Está diseñada para flujos en los que se requiere rapidez, como procesos de venta directa,
evitando formularios largos. El botón "Crear" solo se habilita cuando todos los
campos requeridos están completados.
"""

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCrearClienteRapido(QWidget):
    """
    Ventana modal para crear un nuevo cliente de forma rápida.

    Esta interfaz solicita únicamente los datos básicos obligatorios:
    nombre, primer apellido, DNI y teléfono. Está diseñada para ser utilizada
    en flujos donde se requiere agilidad sin registrar todos los datos del cliente.

    El botón de creación solo se activa cuando todos los campos requeridos están completos.

    Atributos:
        input_nombre (QLineEdit): Campo para el nombre del cliente.
        input_apellido1 (QLineEdit): Campo para el primer apellido.
        input_dni (QLineEdit): Campo para el DNI.
        input_telefono (QLineEdit): Campo para el teléfono.
        boton_crear (QPushButton): Botón para crear el cliente.
        boton_cancelar (QPushButton): Botón para cancelar y cerrar la ventana.
    """

    def __init__(self):
        """
        Inicializa la ventana de creación rápida de cliente con estilos,
        estructura de campos y conexión de eventos.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Nuevo cliente rápido")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(420, 320)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.MSWindowsFixedSizeDialogHint)
        self.setObjectName("ventana_crear_cliente_rapido")

        self.setup_ui()
        self.aplicar_estilos()
        self.conectar_eventos()

    def setup_ui(self):
        """
        Crea y organiza los widgets de entrada y botones de la ventana.

        Incluye:
        - Campos de entrada para: nombre, primer apellido, DNI, y teléfono.
        - Botón "Crear" (deshabilitado por defecto).
        - Botón "Cancelar".
        """
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
        self.boton_crear.setIcon(QIcon(obtener_ruta_absoluta("img/crear.png")))
        self.boton_crear.setToolTip("Crear nuevo cliente")

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_cancelar.setToolTip("Volver sin crear")

        botones_layout.addWidget(self.boton_crear)
        botones_layout.addWidget(self.boton_cancelar)

        layout.addLayout(botones_layout)

    def aplicar_estilos(self):
        """
        Aplica los estilos CSS definidos en el archivo correspondiente.

        Si el archivo no se encuentra, muestra una advertencia por consola.
        """
        ruta_css = obtener_ruta_absoluta("css/crear_cliente_rapido.css")
        try:
            with open(ruta_css, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"No se encontró el CSS: {ruta_css}")

    def conectar_eventos(self):
        """
        Conecta los eventos de texto cambiado en los campos obligatorios.

        Habilita el botón "Crear" únicamente cuando todos los campos están rellenos.
        """
        for campo in [
            self.input_nombre,
            self.input_apellido1,
            self.input_dni,
            self.input_telefono
        ]:
            campo.textChanged.connect(self.verificar_campos)

    def verificar_campos(self):
        """
        Verifica si todos los campos obligatorios están completos.

        Si todos los campos tienen contenido, se habilita el botón "Crear";
        de lo contrario, permanece deshabilitado.
        """
        campos = [
            self.input_nombre.text().strip(),
            self.input_apellido1.text().strip(),
            self.input_dni.text().strip(),
            self.input_telefono.text().strip()
        ]
        self.boton_crear.setEnabled(all(campos))
