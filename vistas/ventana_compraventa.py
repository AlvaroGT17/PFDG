from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QScrollArea, QToolButton, QSizePolicy, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from utilidades.rutas import obtener_ruta_absoluta
from utilidades.capturador_firma import CapturadorFirma
from modelos.compraventa_consulta import obtener_vehiculos_disponibles


class VentanaCompraventa(QWidget):
    def actualizar_secciones(self, tipo):
        tipo = tipo.upper()

        # Ocultar todo de inicio
        for seccion in [self.seccion_cliente, self.seccion_vehiculo, self.seccion_operacion]:
            seccion['grupo'].setEnabled(False)
            seccion['contenido'].setEnabled(False)
            seccion['contenido'].setVisible(False)
            seccion['toggle'].setChecked(False)
            seccion['toggle'].setEnabled(False)

        if tipo == "SELECCIONE LA OPERACIÓN DESEADA":
            return

        # 🔓 Activar sección Cliente (común a ambas)
        self.seccion_cliente['grupo'].setEnabled(True)
        self.seccion_cliente['contenido'].setEnabled(True)
        self.seccion_cliente['toggle'].setEnabled(True)
        self.seccion_cliente['contenido'].setVisible(True)
        self.seccion_cliente['toggle'].setChecked(True)

        if tipo == "COMPRA POR PARTE DEL CONCESIONARIO":
            self.seccion_vehiculo['grupo'].setEnabled(True)
            self.seccion_vehiculo['contenido'].setEnabled(True)
            self.seccion_vehiculo['toggle'].setEnabled(True)
            self.seccion_vehiculo['contenido'].setVisible(True)
            self.seccion_vehiculo['toggle'].setChecked(True)

        elif tipo == "VENTA POR PARTE DEL CONCESIONARIO":
            self.seccion_operacion['grupo'].setEnabled(True)
            self.seccion_operacion['contenido'].setEnabled(True)
            self.seccion_operacion['toggle'].setEnabled(True)
            self.seccion_operacion['contenido'].setVisible(True)
            self.seccion_operacion['toggle'].setChecked(True)

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
        self.combo_operacion.addItem("Seleccione la operación deseada")
        self.combo_operacion.addItems(
            ["Compra por parte del concesionario", "Venta por parte del concesionario"])
        fila_selector.addWidget(QLabel("Tipo de operación:"))
        fila_selector.addWidget(self.combo_operacion)
        fila_selector.addStretch()
        layout_general.addLayout(fila_selector)

        self.combo_operacion.currentTextChanged.connect(
            self.actualizar_secciones)

        # Scroll
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll_area_compraventa")
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0, 0, 0, 0)  # ✅ Márgenes a 0
        layout_general.addWidget(scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName(
            "scroll_widget")  # ✅ Nombre importante
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(
            0, 0, 0, 0)  # ✅ Márgenes internos a 0
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

        self.actualizar_secciones(self.combo_operacion.currentText())

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
        self.cliente_nombre.setToolTip(
            "Introduce el nombre o apellidos del cliente para buscarlo.")

        self.cliente_dni = QLineEdit()
        self.cliente_dni.setToolTip(
            "Introduce el DNI del cliente para buscarlo. Ejemplo: 12345678A")

        self.cliente_telefono = QLineEdit()
        self.cliente_telefono.setReadOnly(True)

        self.cliente_email = QLineEdit()
        self.cliente_email.setReadOnly(True)

        self.cliente_direccion = QLineEdit()
        self.cliente_direccion.setReadOnly(True)

        self.cliente_localidad = QLineEdit()
        self.cliente_localidad.setReadOnly(True)

        self.cliente_provincia = QLineEdit()
        self.cliente_provincia.setReadOnly(True)

        self.cliente_observaciones = QTextEdit()
        self.cliente_observaciones.setFixedHeight(60)
        self.cliente_observaciones.setReadOnly(True)

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
        grupo = self.crear_seccion_plegable("Datos del Vehículo a comprar")
        layout = QGridLayout()
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)
        grupo['contenido'].setLayout(layout)

        # Línea 1
        self.vehiculo_id = QLineEdit()
        self.vehiculo_id.setReadOnly(True)
        self.vehiculo_id.setObjectName("vehiculo_id")
        self.vehiculo_id.setToolTip(
            "Identificador único asignado automáticamente por el sistema")

        self.vehiculo_matricula = QLineEdit()
        self.vehiculo_matricula.setToolTip(
            "Matrícula del vehículo. Ejemplo: 1234-ABC")

        self.vehiculo_marca = QLineEdit()
        self.vehiculo_marca.setToolTip(
            "Marca del fabricante del vehículo. Ejemplo: Renault, Toyota...")

        self.vehiculo_modelo = QLineEdit()
        self.vehiculo_modelo.setToolTip(
            "Modelo comercial del vehículo. Ejemplo: Clio, Yaris...")

        layout.addWidget(QLabel("ID:"), 0, 0)
        layout.addWidget(self.vehiculo_id, 0, 1)
        layout.addWidget(QLabel("Matrícula:"), 0, 2)
        layout.addWidget(self.vehiculo_matricula, 0, 3)
        layout.addWidget(QLabel("Marca:"), 0, 4)
        layout.addWidget(self.vehiculo_marca, 0, 5)
        layout.addWidget(QLabel("Modelo:"), 0, 6)
        layout.addWidget(self.vehiculo_modelo, 0, 7)

        # Línea 2
        self.vehiculo_version = QLineEdit()
        self.vehiculo_version.setToolTip(
            "Versión o acabado del vehículo. Ejemplo: GT Line, Sport, Hybrid...")

        self.vehiculo_anio = QLineEdit()
        self.vehiculo_anio.setToolTip(
            "Año de matriculación del vehículo. Ejemplo: 2020")

        self.vehiculo_bastidor = QLineEdit()
        self.vehiculo_bastidor.setToolTip(
            "Número de bastidor (VIN). Debe ser único y tener 17 caracteres")

        self.vehiculo_color = QLineEdit()
        self.vehiculo_color.setToolTip(
            "Color principal del vehículo. Ejemplo: Gris metalizado")

        layout.addWidget(QLabel("Versión:"), 1, 0)
        layout.addWidget(self.vehiculo_version, 1, 1)
        layout.addWidget(QLabel("Año:"), 1, 2)
        layout.addWidget(self.vehiculo_anio, 1, 3)
        layout.addWidget(QLabel("Nº Bastidor:"), 1, 4)
        layout.addWidget(self.vehiculo_bastidor, 1, 5)
        layout.addWidget(QLabel("Color:"), 1, 6)
        layout.addWidget(self.vehiculo_color, 1, 7)

        # Línea 3
        self.vehiculo_cv = QLineEdit()
        self.vehiculo_cv.setToolTip(
            "Potencia del vehículo expresada en caballos (CV)")

        self.vehiculo_combustible = QLineEdit()
        self.vehiculo_combustible.setToolTip(
            "Tipo de combustible: gasolina, diésel, híbrido, eléctrico...")

        self.vehiculo_km = QLineEdit()
        self.vehiculo_km.setToolTip("Kilómetros recorridos por el vehículo")

        layout.addWidget(QLabel("CV:"), 2, 0)
        layout.addWidget(self.vehiculo_cv, 2, 1)
        layout.addWidget(QLabel("Combustible:"), 2, 2)
        layout.addWidget(self.vehiculo_combustible, 2, 3)
        layout.addWidget(QLabel("Kilómetros:"), 2, 4)
        layout.addWidget(self.vehiculo_km, 2, 5)

        # Línea 4
        self.vehiculo_cambio = QLineEdit()
        self.vehiculo_cambio.setToolTip(
            "Tipo de transmisión: manual, automática, etc.")

        self.vehiculo_puertas = QLineEdit()
        self.vehiculo_puertas.setToolTip("Número de puertas del vehículo")

        self.vehiculo_plazas = QLineEdit()
        self.vehiculo_plazas.setToolTip(
            "Número total de plazas disponibles en el vehículo")

        layout.addWidget(QLabel("Cambio:"), 3, 0)
        layout.addWidget(self.vehiculo_cambio, 3, 1)
        layout.addWidget(QLabel("Puertas:"), 3, 2)
        layout.addWidget(self.vehiculo_puertas, 3, 3)
        layout.addWidget(QLabel("Plazas:"), 3, 4)
        layout.addWidget(self.vehiculo_plazas, 3, 5)

        # Línea 5
        self.vehiculo_precio_compra = QLineEdit()
        self.vehiculo_precio_compra.setToolTip(
            "Precio al que el taller ha comprado el vehículo")

        self.vehiculo_precio_venta = QLineEdit()
        self.vehiculo_precio_venta.setToolTip(
            "Precio final de venta al cliente")

        self.vehiculo_descuento = QLineEdit()
        self.vehiculo_descuento.setToolTip(
            "Descuento máximo aplicable al precio de venta (porcentaje)")

        layout.addWidget(QLabel("Precio compra:"), 4, 0)
        layout.addWidget(self.vehiculo_precio_compra, 4, 1)
        layout.addWidget(QLabel("Precio venta:"), 4, 2)
        layout.addWidget(self.vehiculo_precio_venta, 4, 3)
        layout.addWidget(QLabel("Descuento máx. (%):"), 4, 4)
        layout.addWidget(self.vehiculo_descuento, 4, 5)

        # Línea 6: Firma del cliente
        firma_label = QLabel("Firma del cliente:")
        self.capturador_firma = CapturadorFirma()
        self.capturador_firma.setToolTip(
            "Captura la firma del cliente en este espacio.")
        self.capturador_firma.activar_firma(False)
        layout.addWidget(firma_label, 5, 0)
        layout.addWidget(self.capturador_firma, 5, 1, 1, 5)

        # 🔧 Primero crear los botones
        self.boton_activar_firma = QToolButton()
        self.boton_activar_firma.setObjectName("boton_compraventa")
        self.boton_activar_firma.setText("Activar\nfirma")
        self.boton_activar_firma.setIcon(
            QIcon(obtener_ruta_absoluta("img/firma.png")))
        self.boton_activar_firma.setIconSize(QSize(48, 48))
        self.boton_activar_firma.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_activar_firma.setFixedSize(110, 110)
        self.boton_activar_firma.clicked.connect(self.activar_modo_firma)

        self.boton_limpiar_firma = QToolButton()
        self.boton_limpiar_firma.setObjectName("boton_compraventa")
        self.boton_limpiar_firma.setText("Limpiar\nfirma")
        self.boton_limpiar_firma.setIcon(
            QIcon(obtener_ruta_absoluta("img/limpiar_firma.png")))
        self.boton_limpiar_firma.setIconSize(QSize(48, 48))
        self.boton_limpiar_firma.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_limpiar_firma.setFixedSize(110, 110)
        self.boton_limpiar_firma.clicked.connect(self.capturador_firma.limpiar)

        self.boton_simular_contrato = QToolButton()
        self.boton_simular_contrato.setObjectName("boton_compraventa")
        self.boton_simular_contrato.setText("Simular\ncontrato")
        self.boton_simular_contrato.setIcon(
            QIcon(obtener_ruta_absoluta("img/simular.png")))
        self.boton_simular_contrato.setIconSize(QSize(48, 48))
        self.boton_simular_contrato.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_simular_contrato.setFixedSize(110, 110)

        self.boton_aceptar_contrato = QToolButton()
        self.boton_aceptar_contrato.setObjectName("boton_compraventa")
        self.boton_aceptar_contrato.setText("Aceptar\ncontrato")
        self.boton_aceptar_contrato.setIcon(
            QIcon(obtener_ruta_absoluta("img/aceptar.png")))
        self.boton_aceptar_contrato.setIconSize(QSize(48, 48))
        self.boton_aceptar_contrato.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_aceptar_contrato.setFixedSize(110, 110)

        self.boton_activar_firma.setToolTip(
            "Activar o desactivar la captura de firma")
        self.boton_limpiar_firma.setToolTip("Borrar la firma actual")
        self.boton_simular_contrato.setToolTip(
            "Generar una vista previa del contrato")
        self.boton_aceptar_contrato.setToolTip(
            "Aceptar y registrar el contrato final")

        # ✅ Luego añádelos a la cuadrícula
        cuadricula_botones = QGridLayout()
        cuadricula_botones.addWidget(self.boton_activar_firma, 0, 0)
        cuadricula_botones.addWidget(self.boton_limpiar_firma, 0, 1)
        cuadricula_botones.addWidget(self.boton_simular_contrato, 1, 0)
        cuadricula_botones.addWidget(self.boton_aceptar_contrato, 1, 1)

        layout.addLayout(cuadricula_botones, 5, 6, 1, 2)

        return grupo

    def crear_seccion_datos_operacion(self):
        grupo = self.crear_seccion_plegable("Datos para la Venta del Vehículo")
        layout = QVBoxLayout()
        grupo['contenido'].setLayout(layout)

        # 🔴 1. Obtener todos los vehículos
        self.vehiculos_disponibles = obtener_vehiculos_disponibles()
        self.vehiculos_filtrados = self.vehiculos_disponibles.copy()

        # 🔴 2. Crear tabla (antes que los filtros)
        self.tabla_vehiculos = QTableWidget()
        self.tabla_vehiculos.setColumnCount(18)
        self.tabla_vehiculos.setHorizontalHeaderLabels([
            "ID", "Matrícula", "Marca", "Modelo", "Versión", "Año", "Bastidor", "Color", "Combustible",
            "Kilómetros", "Potencia", "Cambio", "Puertas", "Plazas", "P. Compra", "P. Venta", "Descuento", "Estado"
        ])
        self.tabla_vehiculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_vehiculos.setSelectionBehavior(QTableWidget.SelectRows)

        # 🔧 Mínimo 6 filas visibles
        self.tabla_vehiculos.setMinimumHeight(
            self.tabla_vehiculos.verticalHeader().defaultSectionSize() * 6 +
            self.tabla_vehiculos.horizontalHeader().height()
        )

        layout.addWidget(self.tabla_vehiculos)

        # 🔴 3. Crear los filtros (en 4 columnas)
        filtros_layout = QGridLayout()
        filtros_layout.setHorizontalSpacing(10)
        filtros_layout.setVerticalSpacing(6)

        self.filtro_marca = QComboBox()
        self.filtro_anio = QComboBox()
        self.filtro_color = QComboBox()
        self.filtro_combustible = QComboBox()
        self.filtro_km = QComboBox()
        self.filtro_potencia = QComboBox()
        self.filtro_cambio = QComboBox()
        self.filtro_puertas = QComboBox()
        self.filtro_plazas = QComboBox()
        self.filtro_precio = QComboBox()

        # ✅ Diccionario de filtros
        self.filtros = {
            "marca": self.filtro_marca,
            "anio": self.filtro_anio,
            "color": self.filtro_color,
            "combustible": self.filtro_combustible,
            "kilometros": self.filtro_km,
            "potencia_cv": self.filtro_potencia,
            "cambio": self.filtro_cambio,
            "puertas": self.filtro_puertas,
            "plazas": self.filtro_plazas,
            "precio_venta": self.filtro_precio,
        }

        filtros = [
            ("Marca", self.filtro_marca),
            ("Año", self.filtro_anio),
            ("Color", self.filtro_color),
            ("Combustible", self.filtro_combustible),
            ("Kilómetros", self.filtro_km),
            ("Potencia (CV)", self.filtro_potencia),
            ("Cambio", self.filtro_cambio),
            ("Puertas", self.filtro_puertas),
            ("Plazas", self.filtro_plazas),
            ("Precio", self.filtro_precio),
        ]

        for i, (label, combo) in enumerate(filtros):
            fila, columna = divmod(i, 4)
            filtros_layout.addWidget(QLabel(label), fila * 2, columna)
            filtros_layout.addWidget(combo, fila * 2 + 1, columna)
            combo.currentTextChanged.connect(self.actualizar_tabla_vehiculos)

        layout.addLayout(filtros_layout)

        # 🔴 4. Llenar combos y tabla
        self.llenar_valores_filtros()
        self.actualizar_tabla_vehiculos()

        # 🔴 5. Sección de firma y acciones
        contenedor_firma = QGroupBox("Firma del cliente")
        layout_firma = QHBoxLayout(contenedor_firma)

        self.capturador_firma_venta = CapturadorFirma()
        self.capturador_firma_venta.setToolTip(
            "Firma del cliente que realiza la compra.")
        self.capturador_firma_venta.setFixedSize(400, 120)
        self.capturador_firma_venta.activar_firma(False)

        botones_firma = QHBoxLayout()

        # Tamaño común
        tam_boton = QSize(90, 90)
        tam_icono = QSize(40, 40)

        self.boton_activar_firma_venta = QToolButton()
        self.boton_activar_firma_venta.setObjectName("boton_compraventa_venta")
        self.boton_activar_firma_venta.setText("Activar\nfirma")
        self.boton_activar_firma_venta.setIcon(
            QIcon(obtener_ruta_absoluta("img/firma.png")))
        self.boton_activar_firma_venta.setIconSize(tam_icono)
        self.boton_activar_firma_venta.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_activar_firma_venta.setFixedSize(tam_boton)
        self.boton_activar_firma_venta.clicked.connect(self.toggle_firma_venta)

        self.boton_limpiar_firma_venta = QToolButton()
        self.boton_limpiar_firma_venta.setObjectName("boton_compraventa_venta")
        self.boton_limpiar_firma_venta.setText("Limpiar\nfirma")
        self.boton_limpiar_firma_venta.setIcon(
            QIcon(obtener_ruta_absoluta("img/limpiar_firma.png")))
        self.boton_limpiar_firma_venta.setIconSize(tam_icono)
        self.boton_limpiar_firma_venta.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_limpiar_firma_venta.setFixedSize(tam_boton)
        self.boton_limpiar_firma_venta.clicked.connect(
            self.capturador_firma_venta.limpiar)

        self.boton_recargar_vehiculos = QToolButton()
        self.boton_recargar_vehiculos.setObjectName("boton_compraventa_venta")
        self.boton_recargar_vehiculos.setText("Recargar\nvehículos")
        self.boton_recargar_vehiculos.setIcon(
            QIcon(obtener_ruta_absoluta("img/recargar.png")))
        self.boton_recargar_vehiculos.setIconSize(tam_icono)
        self.boton_recargar_vehiculos.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_recargar_vehiculos.setFixedSize(tam_boton)
        self.boton_recargar_vehiculos.clicked.connect(self.recargar_vehiculos)

        self.boton_simular_contrato_venta = QToolButton()
        self.boton_simular_contrato_venta.setObjectName(
            "boton_compraventa_venta")
        self.boton_simular_contrato_venta.setText("Simular\ncontrato")
        self.boton_simular_contrato_venta.setIcon(
            QIcon(obtener_ruta_absoluta("img/simular.png")))
        self.boton_simular_contrato_venta.setIconSize(tam_icono)
        self.boton_simular_contrato_venta.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_simular_contrato_venta.setFixedSize(tam_boton)

        self.boton_aceptar_contrato_venta = QToolButton()
        self.boton_aceptar_contrato_venta.setObjectName(
            "boton_compraventa_venta")
        self.boton_aceptar_contrato_venta.setText("Aceptar\ncontrato")
        self.boton_aceptar_contrato_venta.setIcon(
            QIcon(obtener_ruta_absoluta("img/aceptar.png")))
        self.boton_aceptar_contrato_venta.setIconSize(tam_icono)
        self.boton_aceptar_contrato_venta.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_aceptar_contrato_venta.setFixedSize(tam_boton)

        for boton in [
            self.boton_activar_firma_venta,
            self.boton_limpiar_firma_venta,
            self.boton_recargar_vehiculos,
            self.boton_simular_contrato_venta,
            self.boton_aceptar_contrato_venta,
        ]:
            botones_firma.addWidget(boton)

        layout_firma.addWidget(self.capturador_firma_venta)
        layout_firma.addLayout(botones_firma)

        layout.addWidget(contenedor_firma)

        return grupo

    def volver(self):
        if self.ventana_anterior:
            self.ventana_anterior.show()
        self.close()

    def activar_modo_firma(self):
        """Activa o desactiva el modo firma en el capturador."""
        if self.capturador_firma.activa:
            self.capturador_firma.activar_firma(False)
            self.boton_activar_firma.setText("Activar\nfirma")
        else:
            self.capturador_firma.activar_firma(True)
            self.boton_activar_firma.setText("Desactivar\nfirma")

    def cargar_tabla_filtrada(self):
        self.tabla_vehiculos.setRowCount(len(self.vehiculos_filtrados))

        for fila, vehiculo in enumerate(self.vehiculos_filtrados):
            for columna, clave in enumerate(vehiculo):
                item = QTableWidgetItem(str(vehiculo[clave]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)  # 🔧 Centrado opcional
                self.tabla_vehiculos.setItem(fila, columna, item)

        # 🔧 Mejoras visuales:
        self.tabla_vehiculos.verticalHeader().setVisible(
            False)           # Ocultar número de fila
        # Evita que se parta el texto
        self.tabla_vehiculos.setWordWrap(False)
        # Ajusta alto de fila
        self.tabla_vehiculos.resizeRowsToContents()
        # Ajusta ancho al contenido
        self.tabla_vehiculos.resizeColumnsToContents()
        self.tabla_vehiculos.setAlternatingRowColors(
            True)                # Colores alternos en filas

    def llenar_valores_filtros(self):
        # Recopilar valores únicos
        valores = {campo: set() for campo in self.filtros}
        for veh in self.vehiculos_disponibles:
            for campo in valores:
                valores[campo].add(str(veh.get(campo, "")))

        # Campos con rangos personalizados
        rangos = {
            "kilometros": ["0-25k", "25k-50k", "50k-100k", "100k-150k", "150k+"],
            "potencia_cv": ["0-75", "75-100", "100-150", "150-200", "200+"],
            "precio_venta": ["0-5k", "5k-10k", "10k-15k", "15k-20k", "20k+"],
        }

        for campo, combo in self.filtros.items():
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("Cualquiera")

            if campo in rangos:
                for rango in rangos[campo]:
                    combo.addItem(rango)
            else:
                for val in sorted(valores[campo]):
                    combo.addItem(val)

            combo.blockSignals(False)

    def aplicar_filtros(self):
        def coincide_rango(valor, texto_rango):
            try:
                val = float(valor)
                if texto_rango.endswith("+"):
                    return val >= float(texto_rango[:-1].replace("k", "000"))
                minimo, maximo = texto_rango.replace("k", "000").split("-")
                return float(minimo) <= val < float(maximo)
            except:
                return False

        self.vehiculos_filtrados = []

        for veh in self.vehiculos_disponibles:
            if veh.get("estado") not in ("DISPONIBLE", "RESERVADO"):
                continue

            incluir = True
            for campo, combo in self.filtros.items():
                filtro = combo.currentText()
                if filtro == "Cualquiera":
                    continue
                valor = str(veh.get(campo, ""))

                if campo in ("kilometros", "potencia_cv", "precio_venta"):
                    if not coincide_rango(valor, filtro):
                        incluir = False
                        break
                else:
                    if filtro != valor:
                        incluir = False
                        break

            if incluir:
                self.vehiculos_filtrados.append(veh)

        self.cargar_tabla_filtrada()

    def actualizar_tabla_vehiculos(self):
        self.aplicar_filtros()

    def toggle_firma_venta(self):
        if self.capturador_firma_venta.activa:
            self.capturador_firma_venta.activar_firma(False)
            self.boton_activar_firma_venta.setText("Activar\nfirma")
        else:
            self.capturador_firma_venta.activar_firma(True)
            self.boton_activar_firma_venta.setText("Desactivar\nfirma")

    def recargar_vehiculos(self):
        self.vehiculos_disponibles = obtener_vehiculos_disponibles()
        self.vehiculos_filtrados = self.vehiculos_disponibles.copy()
        self.llenar_valores_filtros()
        self.actualizar_tabla_vehiculos()
