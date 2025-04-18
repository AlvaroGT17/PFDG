from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QScrollArea, QToolButton, QSizePolicy, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCompraventa(QWidget):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Compraventa")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(1000, 720)
        self.setObjectName("ventana_compraventa")
        self.ventana_anterior = ventana_anterior

        ruta_css = obtener_ruta_absoluta("css/compraventa.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        layout_general = QVBoxLayout(self)

        titulo = QLabel(
            "<h1><span style='color:#738496;'>Rey</span><span style='color:#E30613;'>Boxes</span> - Compraventa</h1>")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_compraventa")
        layout_general.addWidget(titulo)

        # Selector de tipo operación
        fila_selector = QHBoxLayout()
        fila_selector.setContentsMargins(30, 10, 30, 10)
        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems(["Compra", "Venta"])
        self.combo_operacion.currentTextChanged.connect(
            self.actualizar_secciones)
        fila_selector.addWidget(QLabel("Tipo de operación:"))
        fila_selector.addWidget(self.combo_operacion)
        fila_selector.addStretch()
        layout_general.addLayout(fila_selector)

        # Scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout_general.addWidget(scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_area.setWidget(self.scroll_widget)

        # Secciones
        self.seccion_cliente = self.crear_seccion_datos_cliente()
        self.seccion_vehiculo = self.crear_seccion_datos_vehiculo()
        self.seccion_operacion = self.crear_seccion_datos_operacion()

        self.scroll_layout.addWidget(self.seccion_cliente['grupo'])
        self.scroll_layout.addWidget(self.seccion_vehiculo['grupo'])
        self.scroll_layout.addWidget(self.seccion_operacion['grupo'])

        # Botones
        botones = QHBoxLayout()
        self.boton_confirmar = QPushButton("Confirmar")
        self.boton_borrar = QPushButton("Borrar todo")
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.volver)

        botones.addStretch()
        botones.addWidget(self.boton_confirmar)
        botones.addWidget(self.boton_borrar)
        botones.addWidget(self.boton_cancelar)
        layout_general.addLayout(botones)

        self.actualizar_secciones("Compra")

    def crear_seccion_plegable(self, titulo):
        grupo = QGroupBox()
        layout = QVBoxLayout(grupo)

        cabecera = QHBoxLayout()
        boton_toggle = QToolButton()
        icono_expandir = QIcon(obtener_ruta_absoluta("img/mas.png"))
        icono_colapsar = QIcon(obtener_ruta_absoluta("img/menos.png"))
        boton_toggle.setIcon(icono_expandir)
        boton_toggle.setCheckable(True)
        boton_toggle.setChecked(False)
        boton_toggle.setIconSize(QSize(24, 24))
        etiqueta = QLabel(f"<b>{titulo}</b>")
        etiqueta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        etiqueta.setStyleSheet("color: white")

        cabecera.addWidget(etiqueta)
        cabecera.addWidget(boton_toggle)

        contenido = QWidget()
        contenido.setObjectName("contenido_plegable")
        contenido.setVisible(False)

        def toggle():
            visible = boton_toggle.isChecked()
            contenido.setVisible(visible)
            boton_toggle.setIcon(icono_colapsar if visible else icono_expandir)

        boton_toggle.clicked.connect(toggle)

        layout.addLayout(cabecera)
        layout.addWidget(contenido)

        return {"grupo": grupo, "contenido": contenido, "toggle": boton_toggle}

    def crear_seccion_datos_cliente(self):
        grupo = self.crear_seccion_plegable("Datos del Cliente")
        layout = QFormLayout()
        grupo['contenido'].setLayout(layout)

        self.cliente_nombre = QLineEdit()
        self.cliente_dni = QLineEdit()
        self.cliente_telefono = QLineEdit()
        self.cliente_email = QLineEdit()
        self.cliente_direccion = QLineEdit()
        self.cliente_localidad = QLineEdit()
        self.cliente_provincia = QLineEdit()
        self.cliente_observaciones = QTextEdit()
        self.cliente_observaciones.setFixedHeight(60)

        layout.addRow("Nombre y apellidos:", self.cliente_nombre)
        layout.addRow("DNI:", self.cliente_dni)
        layout.addRow("Teléfono:", self.cliente_telefono)
        layout.addRow("Email:", self.cliente_email)
        layout.addRow("Dirección:", self.cliente_direccion)
        layout.addRow("Localidad:", self.cliente_localidad)
        layout.addRow("Provincia:", self.cliente_provincia)
        layout.addRow("Observaciones:", self.cliente_observaciones)

        return grupo

    def crear_seccion_datos_vehiculo(self):
        grupo = self.crear_seccion_plegable("Datos del Vehículo")
        layout = QGridLayout()
        grupo['contenido'].setLayout(layout)

        self.vehiculo_matricula = QLineEdit()
        self.vehiculo_bastidor = QLineEdit()
        self.vehiculo_marca = QLineEdit()
        self.vehiculo_modelo = QLineEdit()
        self.vehiculo_color = QLineEdit()
        self.vehiculo_anio = QLineEdit()
        self.vehiculo_km = QLineEdit()
        self.vehiculo_combustible = QLineEdit()
        self.vehiculo_observaciones = QTextEdit()
        self.vehiculo_observaciones.setFixedHeight(60)

        layout.addWidget(QLabel("Matrícula:"), 0, 0)
        layout.addWidget(self.vehiculo_matricula, 0, 1)
        layout.addWidget(QLabel("Nº Bastidor:"), 0, 2)
        layout.addWidget(self.vehiculo_bastidor, 0, 3)

        layout.addWidget(QLabel("Marca:"), 1, 0)
        layout.addWidget(self.vehiculo_marca, 1, 1)
        layout.addWidget(QLabel("Modelo:"), 1, 2)
        layout.addWidget(self.vehiculo_modelo, 1, 3)

        layout.addWidget(QLabel("Color:"), 2, 0)
        layout.addWidget(self.vehiculo_color, 2, 1)
        layout.addWidget(QLabel("Año:"), 2, 2)
        layout.addWidget(self.vehiculo_anio, 2, 3)

        layout.addWidget(QLabel("Kilómetros:"), 3, 0)
        layout.addWidget(self.vehiculo_km, 3, 1)
        layout.addWidget(QLabel("Combustible:"), 3, 2)
        layout.addWidget(self.vehiculo_combustible, 3, 3)

        layout.addWidget(QLabel("Observaciones:"), 4, 0, 1, 4)
        layout.addWidget(self.vehiculo_observaciones, 5, 0, 1, 4)

        return grupo

    def crear_seccion_datos_operacion(self):
        grupo = self.crear_seccion_plegable("Detalles de la Venta")
        layout = QFormLayout()
        grupo['contenido'].setLayout(layout)

        self.operacion_precio = QLineEdit()
        self.operacion_descuento = QLineEdit()
        self.operacion_estado = QComboBox()
        self.operacion_estado.addItems(["RESERVADO", "VENDIDO"])
        self.operacion_observaciones = QTextEdit()
        self.operacion_observaciones.setFixedHeight(60)

        layout.addRow("Precio de venta:", self.operacion_precio)
        layout.addRow("Descuento aplicado (%):", self.operacion_descuento)
        layout.addRow("Estado:", self.operacion_estado)
        layout.addRow("Observaciones:", self.operacion_observaciones)

        return grupo

    def actualizar_secciones(self, tipo):
        self.seccion_operacion['grupo'].setVisible(tipo.upper() == "VENTA")

    def volver(self):
        if self.ventana_anterior:
            self.ventana_anterior.show()
        self.close()
