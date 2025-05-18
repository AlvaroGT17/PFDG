"""
Módulo de interfaz para registrar y gestionar clientes en el sistema ReyBoxes.

La ventana permite buscar, visualizar, registrar, modificar y eliminar datos
de clientes del taller. Incluye campos detallados para la información personal
y un conjunto de botones de acción. Está diseñada para una experiencia fluida
mediante scroll y estilos visuales personalizados.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QToolButton, QVBoxLayout, QHBoxLayout, QScrollArea
from utilidades.rutas import obtener_ruta_absoluta


class VentanaClientes(QWidget):
    """
    Ventana principal para registrar y gestionar los datos de los clientes en el sistema ReyBoxes.

    Permite:
    - Buscar clientes por nombre, DNI o teléfono.
    - Visualizar y editar información detallada del cliente.
    - Registrar nuevos clientes, modificar registros existentes, limpiar el formulario o eliminar datos.
    - Utiliza un diseño limpio y scrollable para mejorar la experiencia de usuario.

    Atributos:
        input_buscar_nombre (QLineEdit): Campo de búsqueda por nombre y apellidos.
        input_buscar_dni (QLineEdit): Campo de búsqueda por DNI.
        input_buscar_telefono (QLineEdit): Campo de búsqueda por teléfono.
        titulo (QLabel): Título dinámico de la ventana.
        input_nombre, input_apellido1, ... (QLineEdit/QTextEdit): Campos de entrada para los datos del cliente.
        boton_guardar, boton_modificar, ... (QToolButton): Botones de acción de la ventana.
    """

    def __init__(self):
        """
        Inicializa la ventana de gestión de clientes.

        Configura el título, icono, tamaño fijo, widgets de entrada, scroll, botones de acción
        y aplica estilos visuales personalizados desde un archivo CSS.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Registrar cliente")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(860, 720)
        self.setObjectName("ventana_clientes")

        self.setup_ui()
        self.aplicar_estilos()

    def setup_ui(self):
        """
        Inicializa y organiza todos los elementos gráficos de la interfaz:

        - Campos de búsqueda (nombre, DNI, teléfono).
        - Campos de entrada para los datos del cliente.
        - Botones de acción (registrar, modificar, limpiar, eliminar, volver).
        - Scroll para facilitar la navegación en pantallas pequeñas.
        - Conexión para actualizar dinámicamente el título con el nombre del cliente.
        """
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # Campos de búsqueda
        layout_busqueda = QHBoxLayout()
        layout_busqueda.setSpacing(10)

        label_nombre = QLabel("Nombre:")
        self.input_buscar_nombre = QLineEdit()
        self.input_buscar_nombre.setPlaceholderText("Nombre y apellidos")

        label_dni = QLabel("DNI:")
        self.input_buscar_dni = QLineEdit()
        self.input_buscar_dni.setPlaceholderText("DNI")
        self.input_buscar_dni.setFixedWidth(130)

        label_tel = QLabel("Teléfono:")
        self.input_buscar_telefono = QLineEdit()
        self.input_buscar_telefono.setPlaceholderText("Teléfono")
        self.input_buscar_telefono.setFixedWidth(130)

        layout_busqueda.addWidget(label_nombre)
        layout_busqueda.addWidget(self.input_buscar_nombre, stretch=1)
        layout_busqueda.addWidget(label_dni)
        layout_busqueda.addWidget(self.input_buscar_dni)
        layout_busqueda.addWidget(label_tel)
        layout_busqueda.addWidget(self.input_buscar_telefono)

        layout_principal.addLayout(layout_busqueda)

        # Título dinámico
        self.titulo = QLabel()
        self.titulo.setObjectName("titulo_cliente")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.actualizar_titulo("")
        layout_principal.addWidget(self.titulo)

        # Scroll con campos de entrada
        contenedor = QWidget()
        contenedor.setObjectName("contenedor")
        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setSpacing(12)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_apellido1 = QLineEdit()
        self.input_apellido1.setPlaceholderText("Primer apellido")

        self.input_apellido2 = QLineEdit()
        self.input_apellido2.setPlaceholderText("Segundo apellido")

        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("DNI")

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")

        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")

        self.input_cp = QLineEdit()
        self.input_cp.setPlaceholderText("Código postal")

        self.input_localidad = QLineEdit()
        self.input_localidad.setPlaceholderText("Localidad")

        self.input_provincia = QLineEdit()
        self.input_provincia.setPlaceholderText("Provincia")

        self.input_observaciones = QTextEdit()
        self.input_observaciones.setPlaceholderText("Observaciones (opcional)")
        self.input_observaciones.setFixedHeight(80)

        for widget in [
            self.input_nombre, self.input_apellido1, self.input_apellido2, self.input_dni,
            self.input_telefono, self.input_email, self.input_direccion,
            self.input_cp, self.input_localidad, self.input_provincia,
            self.input_observaciones
        ]:
            layout_contenedor.addWidget(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scroll_area")
        scroll.setWidget(contenedor)
        layout_principal.addWidget(scroll)

        # Botones
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(30)
        layout_botones.setAlignment(Qt.AlignCenter)

        self.boton_guardar = QToolButton()
        self.boton_guardar.setText("Registrar")
        self.boton_guardar.setIconSize(QSize(48, 48))
        self.boton_guardar.setIcon(
            QIcon(obtener_ruta_absoluta("img/guardar.png")))
        self.boton_guardar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_modificar = QToolButton()
        self.boton_modificar.setText("Modificar")
        self.boton_modificar.setIconSize(QSize(48, 48))
        self.boton_modificar.setIcon(
            QIcon(obtener_ruta_absoluta("img/modificar_registro.png")))
        self.boton_modificar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_limpiar = QToolButton()
        self.boton_limpiar.setText("Limpiar")
        self.boton_limpiar.setIconSize(QSize(48, 48))
        self.boton_limpiar.setIcon(
            QIcon(obtener_ruta_absoluta("img/escoba.png")))
        self.boton_limpiar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_eliminar = QToolButton()
        self.boton_eliminar.setText("Eliminar")
        self.boton_eliminar.setIconSize(QSize(48, 48))
        self.boton_eliminar.setIcon(
            QIcon(obtener_ruta_absoluta("img/borrar_registro.png")))
        self.boton_eliminar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_volver = QToolButton()
        self.boton_volver.setText("Volver")
        self.boton_volver.setIconSize(QSize(48, 48))
        self.boton_volver.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        for btn in [
            self.boton_guardar, self.boton_modificar, self.boton_limpiar,
            self.boton_eliminar, self.boton_volver
        ]:
            layout_botones.addWidget(btn)

        layout_principal.addLayout(layout_botones)

        # Actualización dinámica del título con el nombre
        self.input_nombre.textChanged.connect(self.actualizar_titulo)

    def aplicar_estilos(self):
        """
        Aplica los estilos personalizados definidos en el archivo CSS correspondiente a la ventana de clientes.
        """
        ruta_css = obtener_ruta_absoluta("css/clientes.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def actualizar_titulo(self, texto):
        """
        Actualiza dinámicamente el título principal de la ventana con el nombre ingresado en el campo.

        Args:
            texto (str): Texto actual del campo de nombre.
        """
        nombre = texto.strip().upper()
        if nombre:
            self.titulo.setText(
                f"<span style='color: #FFFFFF;'>Registrar cliente </span>"
                f"<span style='color: #D90429;'>{nombre}</span>"
            )
        else:
            self.titulo.setText(
                "<span style='color: #FFFFFF;'>Registrar cliente</span>")

    def closeEvent(self, event):
        """
        Anula el evento de cierre de la ventana para evitar el cierre accidental.

        Args:
            event (QCloseEvent): Evento de cierre capturado por Qt.
        """
        event.ignore()
