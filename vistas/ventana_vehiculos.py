"""
Módulo de interfaz gráfica para la gestión de vehículos en ReyBoxes.

Este formulario permite visualizar y gestionar información detallada de los vehículos
asociados a un cliente, incluyendo datos personales del propietario, detalles técnicos
del vehículo y opciones de gestión como registrar, modificar, limpiar, eliminar y volver.

La ventana está dividida en dos secciones scrollables: datos del cliente y del vehículo.
Se aplica un estilo visual personalizado cargado desde un archivo CSS externo.
"""

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QToolButton, QVBoxLayout, QHBoxLayout, QScrollArea, QComboBox, QTextEdit
from utilidades.rutas import obtener_ruta_absoluta


class VentanaVehiculos(QWidget):
    """
    Clase que representa la ventana principal para la gestión de vehículos.

    Incluye campos de visualización del cliente, datos del vehículo, combos para tipo
    y categoría, y botones para registrar, modificar, limpiar, eliminar y volver.
    """

    def __init__(self):
        """
        Inicializa la ventana de gestión de vehículos.

        - Define título, icono, tamaño y estilo.
        - Construye toda la interfaz gráfica.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Gestión de Vehículos")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(960, 720)
        self.setObjectName("ventana_vehiculos")
        self.forzar_cierre = False

        self.setup_ui()
        self.aplicar_estilos()

    def setup_ui(self):
        """
        Construye y organiza todos los elementos gráficos de la interfaz.

        Se divide en:
        - Área de búsqueda (por nombre, DNI, matrícula).
        - Información del cliente (lectura).
        - Información del vehículo (editable).
        - Botones de acción en la parte inferior.
        """
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)

        # Título principal
        titulo = QLabel(
            "<span style='color: white;'>Gestión de </span><span style='color: #d90429;'>Vehículos</span>")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_principal")
        layout_principal.addWidget(titulo)

        # 🔍 Búsqueda
        layout_seccion_busqueda = QHBoxLayout()
        layout_seccion_busqueda.setSpacing(10)

        layout_busqueda_izquierda = QHBoxLayout()
        self.input_buscar_nombre = QLineEdit()
        self.input_buscar_nombre.setPlaceholderText(
            "Buscar por nombre y apellidos")

        self.input_buscar_dni = QLineEdit()
        self.input_buscar_dni.setPlaceholderText("Buscar por DNI")
        self.input_buscar_dni.setFixedWidth(130)

        layout_busqueda_izquierda.addWidget(self.input_buscar_nombre)
        layout_busqueda_izquierda.addWidget(self.input_buscar_dni)

        self.input_buscar_matricula = QLineEdit()
        self.input_buscar_matricula.setPlaceholderText("Buscar por matrícula")
        self.input_buscar_matricula.setFixedWidth(200)

        layout_seccion_busqueda.addLayout(layout_busqueda_izquierda)
        layout_seccion_busqueda.addStretch()
        layout_seccion_busqueda.addWidget(self.input_buscar_matricula)
        layout_principal.addLayout(layout_seccion_busqueda)

        # Scrolls: cliente y vehículo
        layout_scrolls = QHBoxLayout()
        layout_scrolls.setSpacing(20)

        # Cliente
        scroll_cliente = QScrollArea()
        scroll_cliente.setWidgetResizable(True)
        contenedor_cliente = QWidget()
        contenedor_cliente.setObjectName("contenedor_scroll")
        layout_cliente = QVBoxLayout(contenedor_cliente)
        layout_cliente.setSpacing(10)

        # Campos cliente
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        self.input_apellido1 = QLineEdit()
        self.input_apellido1.setPlaceholderText("Primer apellido")
        self.input_apellido2 = QLineEdit()
        self.input_apellido2.setPlaceholderText("Segundo apellido")

        layout_dni_tel = QHBoxLayout()
        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("DNI")
        self.input_dni.setFixedWidth(180)
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")
        layout_dni_tel.addWidget(self.input_dni)
        layout_dni_tel.addWidget(self.input_telefono)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")

        layout_cp_localidad = QHBoxLayout()
        self.input_cp = QLineEdit()
        self.input_cp.setPlaceholderText("CP")
        self.input_cp.setFixedWidth(100)
        self.input_localidad = QLineEdit()
        self.input_localidad.setPlaceholderText("Localidad")
        layout_cp_localidad.addWidget(self.input_cp)
        layout_cp_localidad.addWidget(self.input_localidad)

        self.input_provincia = QLineEdit()
        self.input_provincia.setPlaceholderText("Provincia")

        # Campos de solo lectura
        self.input_nombre.setReadOnly(True)
        self.input_apellido1.setReadOnly(True)
        self.input_apellido2.setReadOnly(True)
        self.input_dni.setReadOnly(True)
        self.input_telefono.setReadOnly(True)
        self.input_email.setReadOnly(True)
        self.input_direccion.setReadOnly(True)
        self.input_cp.setReadOnly(True)
        self.input_localidad.setReadOnly(True)
        self.input_provincia.setReadOnly(True)

        layout_cliente.addWidget(self.input_nombre)
        layout_cliente.addWidget(self.input_apellido1)
        layout_cliente.addWidget(self.input_apellido2)
        layout_cliente.addLayout(layout_dni_tel)
        layout_cliente.addWidget(self.input_email)
        layout_cliente.addWidget(self.input_direccion)
        layout_cliente.addLayout(layout_cp_localidad)
        layout_cliente.addWidget(self.input_provincia)
        scroll_cliente.setWidget(contenedor_cliente)

        # Vehículo
        scroll_vehiculo = QScrollArea()
        scroll_vehiculo.setWidgetResizable(True)
        contenedor_vehiculo = QWidget()
        contenedor_vehiculo.setObjectName("contenedor_scroll")
        layout_vehiculo = QVBoxLayout(contenedor_vehiculo)
        layout_vehiculo.setSpacing(10)

        self.input_matricula = QLineEdit()
        self.input_matricula.setPlaceholderText("Matrícula")
        self.input_marca = QLineEdit()
        self.input_marca.setPlaceholderText("Marca")
        self.input_modelo = QLineEdit()
        self.input_modelo.setPlaceholderText("Modelo")
        self.input_color = QLineEdit()
        self.input_color.setPlaceholderText("Color")

        layout_anyo_combustible = QHBoxLayout()
        layout_anyo_combustible.setSpacing(10)

        self.input_anyo = QLineEdit()
        self.input_anyo.setPlaceholderText("Año")
        self.input_anyo.setFixedWidth(100)

        self.combo_combustible = QComboBox()
        self.combo_combustible.setObjectName("combo_combustible")
        self.combo_combustible.setMinimumWidth(200)

        layout_anyo_combustible.addWidget(self.input_anyo)
        layout_anyo_combustible.addWidget(self.combo_combustible)

        self.input_numero_bastidor = QLineEdit()
        self.input_numero_bastidor.setPlaceholderText("Número de bastidor")

        layout_categoria_tipo = QHBoxLayout()
        layout_categoria_tipo.setSpacing(10)

        self.combo_categoria = QComboBox()
        self.combo_categoria.setObjectName("combo_categoria")
        self.combo_categoria.addItem("Selecciona categoría")

        self.combo_tipo = QComboBox()
        self.combo_tipo.setObjectName("combo_tipo")
        self.combo_tipo.addItem("Selecciona tipo de vehículo")

        layout_categoria_tipo.addWidget(self.combo_categoria)
        layout_categoria_tipo.addWidget(self.combo_tipo)

        layout_vehiculo.addWidget(self.input_matricula)
        layout_vehiculo.addWidget(self.input_marca)
        layout_vehiculo.addWidget(self.input_modelo)
        layout_vehiculo.addWidget(self.input_color)
        layout_vehiculo.addLayout(layout_anyo_combustible)
        layout_vehiculo.addWidget(self.input_numero_bastidor)
        layout_vehiculo.addLayout(layout_categoria_tipo)

        self.input_observaciones = QTextEdit()
        self.input_observaciones.setPlaceholderText("Observaciones")
        self.input_observaciones.setFixedHeight(60)
        layout_vehiculo.addWidget(self.input_observaciones)

        scroll_vehiculo.setWidget(contenedor_vehiculo)
        layout_scrolls.addWidget(scroll_cliente)
        layout_scrolls.addWidget(scroll_vehiculo)
        layout_principal.addLayout(layout_scrolls)

        # Botones de acción
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

        layout_botones.addWidget(self.boton_guardar)
        layout_botones.addWidget(self.boton_modificar)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_eliminar)
        layout_botones.addWidget(self.boton_volver)

        layout_principal.addSpacing(10)
        layout_principal.addLayout(layout_botones)

    def aplicar_estilos(self):
        """
        Aplica el archivo de estilos CSS personalizado a la ventana.

        Si el archivo no se encuentra o da error, se imprime un mensaje.
        """
        ruta = obtener_ruta_absoluta("css/vehiculos.css")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error cargando estilos de vehículos: {e}")

    def closeEvent(self, event):
        """
        Sobrescribe el evento de cierre de ventana.

        Si `forzar_cierre` no está activado, se ignora el cierre manual.
        """
        if not getattr(self, "forzar_cierre", False):
            event.ignore()
