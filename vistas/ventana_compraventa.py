from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QScrollArea, QToolButton, QSizePolicy, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from utilidades.rutas import obtener_ruta_absoluta, obtener_ruta_predeterminada_compras, obtener_ruta_predeterminada_ventas
from utilidades.capturador_firma import CapturadorFirma
from modelos.compraventa_consulta import obtener_vehiculos_disponibles
from controladores.compraventa_controlador import CompraventaControlador


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

        # Cargar estilo CSS
        ruta_css = obtener_ruta_absoluta("css/compraventa.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        layout_general = QVBoxLayout(self)

        # Título
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
        self.combo_operacion.addItems([
            "Compra por parte del concesionario",
            "Venta por parte del concesionario"
        ])
        fila_selector.addWidget(QLabel("Tipo de operación:"))
        fila_selector.addWidget(self.combo_operacion)
        fila_selector.addStretch()
        layout_general.addLayout(fila_selector)

        # Scroll central
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll_area_compraventa")
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0, 0, 0, 0)
        layout_general.addWidget(scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scroll_widget")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(self.scroll_widget)

        # ✅ Crear primero las secciones que no dependen del controlador
        self.seccion_cliente = self.crear_seccion_datos_cliente()
        self.seccion_vehiculo = self.crear_seccion_datos_vehiculo()

        # ✅ Crear el controlador (ya puede usar atributos como cliente_nombre, etc.)
        self.controlador = CompraventaControlador(self)

        # ✅ Crear ahora la sección que SÍ depende del controlador
        self.seccion_operacion = self.crear_seccion_datos_operacion()

        # Añadir secciones al layout
        self.scroll_layout.addWidget(self.seccion_cliente['grupo'])
        self.scroll_layout.addWidget(self.seccion_vehiculo['grupo'])
        self.scroll_layout.addWidget(self.seccion_operacion['grupo'])

        # Botones inferiores
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

        # Conectar combo de operación
        self.combo_operacion.currentTextChanged.connect(
            self.actualizar_secciones)
        self.actualizar_secciones(self.combo_operacion.currentText())

        # Conectar botones de rutas
        self.boton_buscar_ruta_compra.clicked.connect(
            self.controlador.seleccionar_ruta_guardado_compra)
        self.boton_buscar_ruta_venta.clicked.connect(
            self.controlador.seleccionar_ruta_guardado_venta)

        # Inicializar rutas predeterminadas
        self.controlador.toggle_ruta_guardado(
            self.checkbox_ruta_predeterminada_compra.isChecked(),
            self.input_ruta_guardado_compra,
            self.boton_buscar_ruta_compra,
            "compra"
        )
        self.controlador.toggle_ruta_guardado(
            self.checkbox_ruta_predeterminada_venta.isChecked(),
            self.input_ruta_guardado_venta,
            self.boton_buscar_ruta_venta,
            "venta"
        )

        # Inicializar tabla de vehículos al arrancar
        self.controlador.inicializar_datos_vehiculos()

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

        return {
            "grupo": grupo,
            "contenido": contenido,
            "toggle": boton_toggle
        }

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
        self.vehiculo_matricula = QLineEdit()
        self.vehiculo_matricula.setToolTip(
            "Matrícula del vehículo. Ejemplo: 1234-ABC")

        self.vehiculo_marca = QLineEdit()
        self.vehiculo_marca.setToolTip(
            "Marca del fabricante del vehículo. Ejemplo: Renault, Toyota...")

        self.vehiculo_modelo = QLineEdit()
        self.vehiculo_modelo.setToolTip(
            "Modelo comercial del vehículo. Ejemplo: Clio, Yaris...")

        layout.addWidget(QLabel("Matrícula:"), 0, 0)
        layout.addWidget(self.vehiculo_matricula, 0, 1)
        layout.addWidget(QLabel("Marca:"), 0, 2)
        layout.addWidget(self.vehiculo_marca, 0, 3)
        layout.addWidget(QLabel("Modelo:"), 0, 4)
        layout.addWidget(self.vehiculo_modelo, 0, 5)

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

        # Línea 6: Checkboxes de impresión y correo
        self.checkbox_imprimir_compra = QCheckBox("Imprimir documento")
        self.checkbox_correo_compra = QCheckBox("Enviar por correo")
        layout.addWidget(self.checkbox_imprimir_compra, 5, 0)
        layout.addWidget(self.checkbox_correo_compra, 5, 1)

        # Firma
        firma_label = QLabel("Firma del cliente:")
        self.capturador_firma = CapturadorFirma()
        self.capturador_firma.setToolTip(
            "Captura la firma del cliente en este espacio.")
        self.capturador_firma.activar_firma(False)
        layout.addWidget(firma_label, 6, 0)
        layout.addWidget(self.capturador_firma, 6, 1, 1, 5)

        # Botones
        self.boton_activar_firma = QToolButton()
        self.boton_activar_firma.setObjectName("boton_compraventa")
        self.boton_activar_firma.setText("Activar\nfirma")
        self.boton_activar_firma.setIcon(
            QIcon(obtener_ruta_absoluta("img/firma.png")))
        self.boton_activar_firma.setIconSize(QSize(48, 48))
        self.boton_activar_firma.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_activar_firma.setFixedSize(110, 110)
        self.boton_activar_firma.clicked.connect(
            lambda: self.toggle_firma(self.capturador_firma, self.boton_activar_firma))

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

        cuadricula_botones = QGridLayout()
        cuadricula_botones.addWidget(self.boton_activar_firma, 0, 0)
        cuadricula_botones.addWidget(self.boton_limpiar_firma, 0, 1)
        cuadricula_botones.addWidget(self.boton_simular_contrato, 1, 0)
        cuadricula_botones.addWidget(self.boton_aceptar_contrato, 1, 1)
        layout.addLayout(cuadricula_botones, 6, 6, 1, 2)

        # 📁 Ruta de guardado
        self.checkbox_ruta_predeterminada_compra = QCheckBox(
            "Guardar en la ruta predeterminada")
        self.checkbox_ruta_predeterminada_compra.setChecked(True)

        self.input_ruta_guardado_compra = QLineEdit()
        self.input_ruta_guardado_compra.setDisabled(True)

        self.boton_buscar_ruta_compra = QPushButton("Seleccionar carpeta")
        self.boton_buscar_ruta_compra.setDisabled(True)

        layout.addWidget(self.checkbox_ruta_predeterminada_compra, 7, 0, 1, 3)
        layout.addWidget(self.input_ruta_guardado_compra, 8, 0, 1, 4)
        layout.addWidget(self.boton_buscar_ruta_compra, 8, 4, 1, 2)

        # ✅ Conexión para activar/desactivar y cargar ruta según check
        self.checkbox_ruta_predeterminada_compra.toggled.connect(
            lambda estado: self.controlador.toggle_ruta_guardado(
                estado,
                self.input_ruta_guardado_compra,
                self.boton_buscar_ruta_compra,
                "compra"
            )
        )

        # 🔗 Conectar botones de COMPRA
        self.boton_simular_contrato.clicked.connect(
            lambda: self.controlador.simular_contrato("compra")
        )
        self.boton_aceptar_contrato.clicked.connect(
            lambda: self.controlador.aceptar_contrato("compra")
        )

        return grupo

    def crear_seccion_datos_operacion(self):
        grupo = self.crear_seccion_plegable("Datos para la Venta del Vehículo")
        layout = QVBoxLayout()
        grupo['contenido'].setLayout(layout)

        # 🔴 1. Crear tabla (antes que los filtros)
        self.tabla_vehiculos = QTableWidget()
        self.tabla_vehiculos.setColumnCount(18)
        self.tabla_vehiculos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_vehiculos.setHorizontalHeaderLabels([
            "ID", "Matrícula", "Marca", "Modelo", "Versión", "Año", "Bastidor", "Color", "Combustible",
            "Kilómetros", "Potencia", "Cambio", "Puertas", "Plazas", "P. Compra", "P. Venta", "Descuento", "Estado"
        ])
        self.tabla_vehiculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_vehiculos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_vehiculos.setMinimumHeight(
            self.tabla_vehiculos.verticalHeader().defaultSectionSize() * 6 +
            self.tabla_vehiculos.horizontalHeader().height()
        )
        layout.addWidget(self.tabla_vehiculos)

        # 🔴 2. Crear filtros (interfaz)
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
            combo.currentTextChanged.connect(
                self.controlador.actualizar_tabla_vehiculos)

        layout.addLayout(filtros_layout)

        # 🔴 3. Firma y acciones
        contenedor_firma = QGroupBox("Firma del cliente")
        layout_firma = QVBoxLayout(contenedor_firma)

        checkboxes_envio_layout = QHBoxLayout()
        self.checkbox_imprimir_venta = QCheckBox("Imprimir documento")
        self.checkbox_correo_venta = QCheckBox("Enviar por correo")
        checkboxes_envio_layout.addWidget(self.checkbox_imprimir_venta)
        checkboxes_envio_layout.addWidget(self.checkbox_correo_venta)
        checkboxes_envio_layout.addStretch()
        layout_firma.addLayout(checkboxes_envio_layout)

        firma_botones_layout = QHBoxLayout()

        self.capturador_firma_venta = CapturadorFirma()
        self.capturador_firma_venta.setToolTip(
            "Firma del cliente que realiza la compra.")
        self.capturador_firma_venta.setFixedSize(400, 120)
        self.capturador_firma_venta.activar_firma(False)

        botones_firma = QHBoxLayout()
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
        self.boton_activar_firma_venta.clicked.connect(
            lambda: self.toggle_firma(self.capturador_firma_venta, self.boton_activar_firma_venta))

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
        self.boton_recargar_vehiculos.clicked.connect(
            self.controlador.recargar_vehiculos)

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

        firma_botones_layout.addWidget(self.capturador_firma_venta)
        firma_botones_layout.addLayout(botones_firma)
        layout_firma.addLayout(firma_botones_layout)

        # 📁 Ruta de guardado debajo de la firma
        self.checkbox_ruta_predeterminada_venta = QCheckBox(
            "Guardar en la ruta predeterminada")
        self.checkbox_ruta_predeterminada_venta.setChecked(True)

        self.input_ruta_guardado_venta = QLineEdit()
        self.input_ruta_guardado_venta.setDisabled(True)

        self.boton_buscar_ruta_venta = QPushButton("Seleccionar carpeta")
        self.boton_buscar_ruta_venta.setDisabled(True)

        self.checkbox_ruta_predeterminada_venta.toggled.connect(
            lambda estado: self.controlador.toggle_ruta_guardado(
                self.checkbox_ruta_predeterminada_venta.isChecked(),
                self.input_ruta_guardado_venta,
                self.boton_buscar_ruta_venta,
                "venta"
            )
        )

        self.controlador.toggle_ruta_guardado(
            self.checkbox_ruta_predeterminada_venta.isChecked(),
            self.input_ruta_guardado_venta,
            self.boton_buscar_ruta_venta,
            "venta"
        )

        layout_firma.addWidget(self.checkbox_ruta_predeterminada_venta)
        ruta_guardado_layout = QHBoxLayout()
        ruta_guardado_layout.addWidget(self.input_ruta_guardado_venta)
        ruta_guardado_layout.addWidget(self.boton_buscar_ruta_venta)
        layout_firma.addLayout(ruta_guardado_layout)

        layout.addWidget(contenedor_firma)

        # 🔗 Conectar botones de VENTA
        self.boton_simular_contrato_venta.clicked.connect(
            lambda: self.controlador.simular_contrato("venta")
        )
        self.boton_aceptar_contrato_venta.clicked.connect(
            lambda: self.controlador.aceptar_contrato("venta")
        )

        return grupo

    def volver(self):
        if self.ventana_anterior:
            self.ventana_anterior.show()
        self.close()

    def toggle_firma(self, capturador, boton):
        if capturador.activa:
            capturador.activar_firma(False)
            boton.setText("Activar\nfirma")
        else:
            capturador.activar_firma(True)
            boton.setText("Desactivar\nfirma")
