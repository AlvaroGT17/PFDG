from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QScrollArea, QToolButton, QSizePolicy, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem,  QHeaderView, QCheckBox, QSizePolicy
from utilidades.rutas import obtener_ruta_absoluta, obtener_ruta_predeterminada_compras, obtener_ruta_predeterminada_ventas
from utilidades.capturador_firma import CapturadorFirma
from modelos.compraventa_consulta import obtener_vehiculos_disponibles
from controladores.compraventa_controlador import CompraventaControlador


class VentanaCompraventa(QWidget):
    """
    Ventana principal para gestionar el módulo de compraventa de vehículos.

    Esta ventana permite:
    - Realizar compras de vehículos (con registro manual de datos y firma).
    - Realizar ventas de vehículos existentes en stock (con filtros, tabla, firma y contrato).
    - Imprimir o enviar por correo los contratos generados.

    Se adapta dinámicamente al tipo de operación seleccionada.
    """

    def actualizar_secciones(self, tipo):
        """
        Activa y muestra únicamente las secciones correspondientes al tipo de operación
        seleccionado por el usuario: "compra" o "venta".

        Si el valor recibido es el texto por defecto, se ocultan todas las secciones.
        Este método gestiona la visibilidad, habilitación y expansión de las secciones:
        - Cliente (común a ambas operaciones)
        - Vehículo (solo para compras)
        - Operación (solo para ventas)

        Parámetros:
            tipo (str): Tipo de operación seleccionado desde el combo. Se espera
                        "Compra por parte del concesionario" o "Venta por parte del concesionario".
        """
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

        # Activar sección Cliente (común a ambas)
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
        """
        Constructor de la clase VentanaCompraventa.

        Inicializa y configura toda la interfaz de la ventana de compraventa. Esta ventana
        permite gestionar tanto operaciones de compra como de venta de vehículos, y se adapta
        dinámicamente en función del tipo de operación seleccionada.

        Incluye:
        - Carga del estilo visual desde archivo CSS.
        - Configuración de secciones plegables: cliente, vehículo y operación.
        - Conexión de botones, acciones y combo de selección.
        - Preparación de rutas de guardado, firma y tabla de vehículos.
        - Asociación del controlador correspondiente.

        Parámetros:
            ventana_anterior (QWidget): Referencia a la ventana desde la que se accede a esta.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Compraventa")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(1000, 720)
        self.setObjectName("ventana_compraventa")
        self.ventana_anterior = ventana_anterior
        self.firma_activa_compra = False
        self.firma_activa_venta = False

    def crear_seccion_plegable(self, titulo):
        """
        Crea una sección visual plegable (expandible/colapsable) con un título especificado.

        Esta sección consiste en un `QGroupBox` que contiene un botón de tipo `QToolButton` 
        que alterna entre expandir y contraer el contenido. Se utiliza para organizar
        visualmente partes de la interfaz como los datos del cliente, del vehículo, etc.

        Parámetros:
            titulo (str): Título que se mostrará en la cabecera de la sección.

        Retorna:
            dict: Un diccionario con claves:
                - 'grupo': el QGroupBox principal de la sección.
                - 'contenido': el QWidget que contiene los campos plegables.
                - 'toggle': el botón para expandir/colapsar la sección.
        """
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

        # El toggle controla visibilidad del contenido
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
        """
        Crea la sección visual correspondiente a los datos del cliente.

        Esta sección incluye campos de solo lectura donde se muestran los datos del cliente
        recuperados desde la base de datos, como nombre, DNI, teléfono, email, dirección, 
        localidad, provincia y observaciones.

        Los campos de búsqueda (`nombre/apellidos` y `DNI`) están habilitados para permitir
        localizar al cliente. El resto de campos se completan automáticamente cuando se
        encuentra un cliente registrado.

        Retorna:
            dict: Un diccionario con las claves:
                - 'grupo': el contenedor QGroupBox completo.
                - 'contenido': el widget interno que contiene los campos.
                - 'toggle': el botón para plegar/expandir la sección.
        """
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
        """
        Crea la sección visual que permite introducir y visualizar los datos de un vehículo a comprar.

        Esta sección está compuesta por varios campos distribuidos en un `QGridLayout`, incluyendo:
        matrícula, marca, modelo, versión, año, bastidor, color, potencia, combustible, kilómetros,
        cambio, número de puertas, plazas, precios y descuento. También permite configurar si se desea
        imprimir o enviar por correo el contrato generado.

        Además, contiene una sub-sección para la firma del cliente, donde se puede activar o limpiar
        la firma, simular el contrato o aceptar la operación.

        Incluye controles para establecer la ruta de guardado del documento generado, ya sea en una
        ubicación predeterminada o personalizada.

        Retorna:
            dict: Un diccionario con las claves:
                - 'grupo': el `QGroupBox` que contiene toda la sección.
                - 'contenido': el `QWidget` interno con el contenido editable.
                - 'toggle': el botón que permite expandir o contraer la sección.
        """
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

        # Contenedor firma y botones
        contenedor_firma_compra = QGroupBox("Firma del cliente")
        layout_firma = QVBoxLayout(contenedor_firma_compra)

        self.capturador_firma = CapturadorFirma()
        self.capturador_firma.setToolTip("Captura la firma del cliente.")
        self.capturador_firma.setFixedSize(400, 120)
        self.capturador_firma.activar_firma(False)

        self.mensaje_firma_compra = QLabel(
            "🖊️ Firma activada – pulse ENTER para finalizar")
        self.mensaje_firma_compra.setStyleSheet(
            "color: yellow; font-weight: bold;")
        self.mensaje_firma_compra.setAlignment(Qt.AlignCenter)
        self.mensaje_firma_compra.setVisible(False)

        botones_firma = QHBoxLayout()
        tam_boton = QSize(90, 90)
        tam_icono = QSize(40, 40)

        self.boton_activar_firma = QToolButton()
        self.boton_activar_firma.setObjectName("boton_compraventa")
        self.boton_activar_firma.setText("Activar\nfirma")
        self.boton_activar_firma.setIcon(
            QIcon(obtener_ruta_absoluta("img/firma.png")))
        self.boton_activar_firma.setIconSize(tam_icono)
        self.boton_activar_firma.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_activar_firma.setFixedSize(tam_boton)
        self.boton_activar_firma.clicked.connect(
            lambda: self.toggle_firma(self.capturador_firma, self.boton_activar_firma))

        self.boton_limpiar_firma = QToolButton()
        self.boton_limpiar_firma.setObjectName("boton_compraventa")
        self.boton_limpiar_firma.setText("Limpiar\nfirma")
        self.boton_limpiar_firma.setIcon(
            QIcon(obtener_ruta_absoluta("img/limpiar_firma.png")))
        self.boton_limpiar_firma.setIconSize(tam_icono)
        self.boton_limpiar_firma.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_limpiar_firma.setFixedSize(tam_boton)
        self.boton_limpiar_firma.clicked.connect(self.capturador_firma.limpiar)

        self.boton_simular_contrato = QToolButton()
        self.boton_simular_contrato.setObjectName("boton_compraventa")
        self.boton_simular_contrato.setText("Simular\ncontrato")
        self.boton_simular_contrato.setIcon(
            QIcon(obtener_ruta_absoluta("img/simular.png")))
        self.boton_simular_contrato.setIconSize(tam_icono)
        self.boton_simular_contrato.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_simular_contrato.setFixedSize(tam_boton)

        self.boton_aceptar_contrato = QToolButton()
        self.boton_aceptar_contrato.setObjectName("boton_compraventa")
        self.boton_aceptar_contrato.setText("Aceptar\ncontrato")
        self.boton_aceptar_contrato.setIcon(
            QIcon(obtener_ruta_absoluta("img/aceptar.png")))
        self.boton_aceptar_contrato.setIconSize(tam_icono)
        self.boton_aceptar_contrato.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.boton_aceptar_contrato.setFixedSize(tam_boton)

        for boton in [self.boton_activar_firma, self.boton_limpiar_firma,
                      self.boton_simular_contrato, self.boton_aceptar_contrato]:
            botones_firma.addWidget(boton)

        # Ruta de guardado
        self.checkbox_ruta_predeterminada_compra = QCheckBox(
            "Guardar en la ruta predeterminada")
        self.checkbox_ruta_predeterminada_compra.setChecked(True)

        self.input_ruta_guardado_compra = QLineEdit()
        self.input_ruta_guardado_compra.setDisabled(True)

        self.boton_buscar_ruta_compra = QPushButton("Seleccionar carpeta")
        self.boton_buscar_ruta_compra.setDisabled(True)

        self.checkbox_ruta_predeterminada_compra.toggled.connect(
            lambda estado: self.controlador.toggle_ruta_guardado(
                estado,
                self.input_ruta_guardado_compra,
                self.boton_buscar_ruta_compra,
                "compra"
            )
        )

        ruta_guardado_layout = QHBoxLayout()
        ruta_guardado_layout.addWidget(self.input_ruta_guardado_compra)
        ruta_guardado_layout.addWidget(self.boton_buscar_ruta_compra)

        # Layout horizontal con firma + botones
        firma_y_botones_vertical = QVBoxLayout()
        firma_y_botones_vertical.addWidget(self.capturador_firma)
        firma_y_botones_vertical.addWidget(self.mensaje_firma_compra)

        firma_y_botones = QHBoxLayout()
        firma_y_botones.addLayout(firma_y_botones_vertical)
        firma_y_botones.addLayout(botones_firma)

        layout_firma.addLayout(firma_y_botones)

        layout_firma.addWidget(self.checkbox_ruta_predeterminada_compra)
        layout_firma.addLayout(ruta_guardado_layout)

        layout.addWidget(contenedor_firma_compra, 6, 0, 1, 8)

        # Conectar botones de COMPRA
        self.boton_simular_contrato.clicked.connect(
            lambda: self.controlador.simular_contrato("compra"))
        self.boton_aceptar_contrato.clicked.connect(
            self.controlador.aceptar_contrato_compra)

        return grupo

    def crear_seccion_datos_operacion(self):
        """
        Crea y devuelve la sección visual correspondiente a la venta de vehículos desde el concesionario.

        Esta sección incluye:
        - Una tabla (`QTableWidget`) con los vehículos disponibles para la venta, cargados desde la base de datos.
        - Un conjunto de filtros (`QComboBox`) que permiten refinar los resultados visibles en la tabla según
        criterios como marca, año, color, combustible, precio, etc.
        - Un área de firma digital donde el cliente puede firmar electrónicamente el contrato de compraventa.
        - Botones para activar y limpiar la firma, simular el contrato generado, aceptar la operación y
        recargar los vehículos.
        - Opciones para imprimir o enviar el contrato por correo.
        - Selección de ruta de guardado, ya sea predeterminada o personalizada.

        La sección queda plegada por defecto y se expande cuando el usuario selecciona "Venta por parte del concesionario"
        en el combo principal.

        Retorna:
            dict: Un diccionario con las claves:
                - 'grupo': el `QGroupBox` contenedor de la sección.
                - 'contenido': el widget interno que contiene el contenido.
                - 'toggle': botón para expandir o contraer la sección.
        """
        grupo = self.crear_seccion_plegable("Datos para la Venta del Vehículo")
        layout = QVBoxLayout()
        grupo['contenido'].setLayout(layout)

        # 1. Crear tabla (antes que los filtros)
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

        # 2. Crear filtros (interfaz)
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

        # 3. Firma y acciones
        contenedor_firma = QGroupBox("Firma del cliente")
        layout_firma = QVBoxLayout(contenedor_firma)

        # Mensaje informativo sobre la firma (VENTA)
        self.mensaje_firma_venta = QLabel(
            "🖊️ Firma activada – pulse ENTER para finalizar")
        self.mensaje_firma_venta.setStyleSheet(
            "color: yellow; font-weight: bold;")
        self.mensaje_firma_venta.setAlignment(Qt.AlignCenter)
        self.mensaje_firma_venta.setVisible(False)

        # Capturador de firma
        self.capturador_firma_venta = CapturadorFirma()
        self.capturador_firma_venta.setToolTip(
            "Firma del cliente que realiza la compra.")
        self.capturador_firma_venta.setFixedSize(400, 120)
        self.capturador_firma_venta.activar_firma(False)

        # Layout vertical para mensaje + firma
        contenedor_firma_venta = QVBoxLayout()
        contenedor_firma_venta.addWidget(self.mensaje_firma_venta)
        contenedor_firma_venta.addWidget(self.capturador_firma_venta)

        # Botones
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
            lambda: self.toggle_firma(
                self.capturador_firma_venta, self.boton_activar_firma_venta)
        )

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

        # Añadir botones al layout
        for boton in [
            self.boton_activar_firma_venta,
            self.boton_limpiar_firma_venta,
            self.boton_recargar_vehiculos,
            self.boton_simular_contrato_venta,
            self.boton_aceptar_contrato_venta,
        ]:
            botones_firma.addWidget(boton)

        # Añadir todo al layout principal de la sección
        firma_y_botones = QHBoxLayout()
        firma_y_botones.addLayout(contenedor_firma_venta)
        firma_y_botones.addLayout(botones_firma)
        layout_firma.addLayout(firma_y_botones)

        # Checkboxes para imprimir y enviar por correo (VENTA)
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.setSpacing(15)  # reduce el espacio entre ellos

        self.checkbox_imprimir_venta = QCheckBox("Imprimir documento")
        self.checkbox_correo_venta = QCheckBox("Enviar por correo")

        checkboxes_layout.addWidget(self.checkbox_imprimir_venta)
        checkboxes_layout.addWidget(self.checkbox_correo_venta)
        checkboxes_layout.addStretch()  # empuja a la izquierda

        layout_firma.addLayout(checkboxes_layout)

        # Ruta de guardado debajo de la firma
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

        # Agregar al layout principal
        layout.addWidget(contenedor_firma)

        # Conectar botones de VENTA
        self.boton_simular_contrato_venta.clicked.connect(
            lambda: self.controlador.simular_contrato("venta")
        )
        self.boton_aceptar_contrato_venta.clicked.connect(
            self.controlador.aceptar_contrato_venta)

        return grupo

    def volver(self):
        """
        Cierra la ventana actual de compraventa y vuelve a mostrar la ventana anterior.

        Este método se invoca al pulsar el botón "Volver". Si la ventana anterior fue pasada
        al crear esta ventana (normalmente el menú principal o dashboard), se vuelve a mostrar.

        No realiza comprobaciones adicionales ni solicita confirmación al usuario.
        """
        if self.ventana_anterior:
            self.ventana_anterior.show()
        self.close()

    def toggle_firma(self, capturador, boton):
        if capturador == self.capturador_firma:  # COMPRA
            if not self.firma_activa_compra:
                self.firma_activa_compra = True
                capturador.activar_firma(True)
                boton.setText("Firmando...")
                self.mensaje_firma_compra.setVisible(True)
                capturador.setFocus()
            else:
                self.firma_activa_compra = False
                capturador.activar_firma(False)
                boton.setText("Activar\nfirma")
                self.mensaje_firma_compra.setVisible(False)

        elif capturador == self.capturador_firma_venta:  # VENTA
            if not self.firma_activa_venta:
                self.firma_activa_venta = True
                capturador.activar_firma(True)
                boton.setText("Firmando...")
                self.mensaje_firma_venta.setVisible(True)
                capturador.setFocus()
            else:
                self.firma_activa_venta = False
                capturador.activar_firma(False)
                boton.setText("Activar\nfirma")
                self.mensaje_firma_venta.setVisible(False)

    def eventFilter(self, source, event):
        """
        Activa o desactiva el modo de firma en el capturador correspondiente (compra o venta).

        Este método se utiliza para permitir que el cliente firme en el cuadro de firma, ya sea
        para la operación de compra o de venta. Cambia el estado visual, activa o desactiva la
        funcionalidad del capturador, muestra u oculta el mensaje de firma y modifica el texto
        del botón que controla la acción.

        Parámetros:
            capturador (CapturadorFirma): Widget de firma a activar o desactivar.
            boton (QToolButton): Botón que ha activado el proceso y cuyo texto se modifica según el estado.
        """
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.firma_activa_compra:
                self.toggle_firma(self.capturador_firma,
                                  self.boton_activar_firma)
                return True
            elif self.firma_activa_venta:
                self.toggle_firma(self.capturador_firma_venta,
                                  self.boton_activar_firma_venta)
                return True
        return super().eventFilter(source, event)

    def borrar_todo(self):
        """
        Restablece todos los campos del formulario de compraventa a su estado inicial.

        Esta función se encarga de:
        - Limpiar todos los campos de texto relacionados con los datos del cliente y del vehículo.
        - Limpiar ambas firmas (compra y venta).
        - Vaciar los campos de rutas de guardado.
        - Desmarcar las casillas de imprimir y enviar por correo.
        - Restaurar el uso de rutas predeterminadas para guardar contratos.
        - Reiniciar la selección del tipo de operación.
        - Ocultar los mensajes de activación de firma.
        - Resetear los estados internos de firma activa y los textos de los botones.

        Esta función es llamada cuando el usuario pulsa el botón "Borrar todo".
        Deja el formulario completamente limpio y listo para iniciar una nueva operación.
        """
        # Limpiar campos del cliente
        self.cliente_nombre.clear()
        self.cliente_dni.clear()
        self.cliente_direccion.clear()
        self.cliente_localidad.clear()
        self.cliente_provincia.clear()
        self.cliente_telefono.clear()
        self.cliente_email.clear()
        self.cliente_observaciones.clear()

        # Limpiar campos del vehículo
        self.vehiculo_marca.clear()
        self.vehiculo_modelo.clear()
        self.vehiculo_version.clear()
        self.vehiculo_anio.clear()
        self.vehiculo_matricula.clear()
        self.vehiculo_bastidor.clear()
        self.vehiculo_color.clear()
        self.vehiculo_combustible.clear()
        self.vehiculo_km.clear()
        self.vehiculo_cv.clear()
        self.vehiculo_cambio.clear()
        self.vehiculo_puertas.clear()
        self.vehiculo_plazas.clear()
        self.vehiculo_precio_compra.clear()
        self.vehiculo_precio_venta.clear()
        self.vehiculo_descuento.clear()

        # Limpiar firmas
        self.capturador_firma.limpiar()
        self.capturador_firma_venta.limpiar()

        # Limpiar rutas
        self.input_ruta_guardado_compra.clear()
        self.input_ruta_guardado_venta.clear()

        # Desmarcar checkbox
        self.checkbox_correo_compra.setChecked(False)
        self.checkbox_imprimir_compra.setChecked(False)
        self.checkbox_correo_venta.setChecked(False)
        self.checkbox_imprimir_venta.setChecked(False)

        # Volver a ruta predeterminada en compra y venta
        self.checkbox_ruta_predeterminada_compra.setChecked(True)
        self.checkbox_ruta_predeterminada_venta.setChecked(True)

        # Resetear selección de operación
        self.combo_operacion.setCurrentIndex(0)

        # Ocultar mensajes de firma
        self.mensaje_firma_compra.setVisible(False)
        self.mensaje_firma_venta.setVisible(False)

        # Resetear estado de firma
        self.firma_activa_compra = False
        self.firma_activa_venta = False

        # Resetear botones de firma
        self.boton_activar_firma.setText("Activar\nfirma")
        self.boton_activar_firma_venta.setText("Activar\nfirma")
