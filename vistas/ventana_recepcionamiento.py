from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QTextEdit, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QDateEdit, QButtonGroup,
    QWidget, QStackedLayout, QScrollArea, QToolButton, QSizePolicy, QMessageBox, QGridLayout, QScrollArea, QPushButton, QRadioButton, QFileDialog
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon
from utilidades.rutas import obtener_ruta_absoluta


class VentanaRecepcionamiento(QDialog):

    def confirmar_borrado(self):
        msgbox = QMessageBox(self)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setWindowTitle("Confirmar borrado")
        msgbox.setText(
            "<b>¿Estás seguro de que quieres borrar todos los datos del formulario?</b>")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        respuesta = msgbox.exec()
        if respuesta == QMessageBox.Yes:
            self.borrar_todo()

    def borrar_todo(self):
        for campo in [self.input_nombre, self.input_dni, self.input_telefono, self.input_email, self.input_direccion,
                      self.input_matricula, self.input_marca, self.input_modelo, self.input_color,
                      self.input_anio, self.input_kilometros, self.combo_combustible, self.input_vin,
                      self.input_compania, self.input_averias, self.input_valor_estimado,
                      self.input_estado_exterior, self.input_estado_interior, self.input_max_autorizado,
                      self.input_correo, self.input_observaciones]:
            if isinstance(campo, (QLineEdit, QTextEdit)):
                campo.clear()

        self.combo_tipo.setCurrentIndex(-1)
        self.combo_categoria.setCurrentIndex(-1)
        self.combo_urgencia.setCurrentIndex(0)

        self.check_grua.setChecked(False)
        self.check_arranca.setChecked(False)
        self.check_seguro.setChecked(False)
        self.check_presupuesto_escrito.setChecked(False)
        self.check_itv.setChecked(False)
        self.checkbox_imprimir.setChecked(False)
        self.checkbox_enviar_correo.setChecked(False)

        self.stacked_motivo.setCurrentIndex(-1)

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setWindowTitle("ReyBoxes - Recepcionamiento de Vehículos")
        self.setFixedSize(900, 720)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setObjectName("ventana_recepcionamiento")

        ruta_css = obtener_ruta_absoluta("css/recepcionamiento.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        layout_general = QVBoxLayout(self)

        titulo = QLabel(
            "<h1><span style='color:#738496;'>Rey</span><span style='color:#E30613;'>Boxes</span> - Recepcionamiento</h1>")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_recepcionamiento")
        layout_general.addWidget(titulo)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scroll_area_recepcionamiento")
        layout_general.addWidget(scroll_area)

        widget_contenido = QWidget()
        widget_contenido.setObjectName("widget_contenido")
        scroll_area.setWidget(widget_contenido)

        layout_scroll = QVBoxLayout()
        widget_contenido.setLayout(layout_scroll)

        layout_scroll.addWidget(self.crear_seccion_datos_cliente())
        layout_scroll.addWidget(self.crear_seccion_datos_vehiculo())
        layout_scroll.addWidget(self.crear_seccion_motivo_recepcionamiento())
        layout_scroll.addWidget(self.crear_seccion_entrega_documento())

        layout_botones = QHBoxLayout()

        self.boton_confirmar = QToolButton()
        self.boton_confirmar.setText("Confirmar")
        self.boton_confirmar.setIcon(
            QIcon(obtener_ruta_absoluta("img/confirmar.png")))
        self.boton_confirmar.setIconSize(QSize(48, 48))
        self.boton_confirmar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_limpiar = QToolButton()
        self.boton_limpiar.setText("Borrar todo")
        self.boton_limpiar.setIcon(
            QIcon(obtener_ruta_absoluta("img/escoba.png")))
        self.boton_limpiar.setIconSize(QSize(48, 48))
        self.boton_limpiar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_limpiar.clicked.connect(self.confirmar_borrado)

        self.boton_cancelar = QToolButton()
        self.boton_cancelar.setText("Cancelar")
        self.boton_cancelar.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_cancelar.setIconSize(QSize(48, 48))
        self.boton_cancelar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones.addWidget(self.boton_confirmar)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_cancelar)
        layout_general.addLayout(layout_botones)

        for boton in [self.boton_confirmar, self.boton_limpiar, self.boton_cancelar]:
            boton.setFixedSize(110, 90)  # O ajusta a tu gusto

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

        self.input_nombre = QLineEdit()
        self.input_dni = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_email = QLineEdit()
        self.input_direccion = QLineEdit()

        layout.addRow("Nombre y apellidos:", self.input_nombre)
        layout.addRow("DNI:", self.input_dni)
        layout.addRow("Teléfono:", self.input_telefono)
        layout.addRow("Email:", self.input_email)
        layout.addRow("Dirección:", self.input_direccion)

        return grupo['grupo']

    def crear_seccion_datos_vehiculo(self):
        grupo = self.crear_seccion_plegable("Datos del Vehículo")
        layout = QGridLayout()
        grupo['contenido'].setLayout(layout)

        self.input_matricula = QLineEdit()
        self.input_marca = QLineEdit()
        self.input_modelo = QLineEdit()
        self.input_color = QLineEdit()
        self.input_anio = QLineEdit()
        self.input_kilometros = QLineEdit()
        self.combo_combustible = QComboBox()
        self.input_vin = QLineEdit()
        self.combo_categoria = QComboBox()
        self.combo_tipo = QComboBox()

        layout.addWidget(QLabel("Matrícula:"), 0, 0)
        layout.addWidget(self.input_matricula, 0, 1)
        layout.addWidget(QLabel("Nº Bastidor (VIN):"), 0, 2)
        layout.addWidget(self.input_vin, 0, 3)

        layout.addWidget(QLabel("Marca:"), 1, 0)
        layout.addWidget(self.input_marca, 1, 1)
        layout.addWidget(QLabel("Modelo:"), 1, 2)
        layout.addWidget(self.input_modelo, 1, 3)

        layout.addWidget(QLabel("Color:"), 2, 0)
        layout.addWidget(self.input_color, 2, 1)
        layout.addWidget(QLabel("Año:"), 2, 2)
        layout.addWidget(self.input_anio, 2, 3)

        layout.addWidget(QLabel("Kilómetros:"), 3, 0)
        layout.addWidget(self.input_kilometros, 3, 1)
        layout.addWidget(QLabel("Combustible:"), 3, 2)
        layout.addWidget(self.combo_combustible, 3, 3)

        layout.addWidget(QLabel("Categoría:"), 4, 0)
        layout.addWidget(self.combo_categoria, 4, 1)
        layout.addWidget(QLabel("Tipo de vehículo:"), 4, 2)
        layout.addWidget(self.combo_tipo, 4, 3)

        return grupo['grupo']

    def crear_seccion_motivo_recepcionamiento(self):
        grupo = self.crear_seccion_plegable("Motivo del Recepcionamiento")
        layout = QVBoxLayout()
        grupo['contenido'].setLayout(layout)

        # Fila 1: Motivo, urgencia y fecha
        fila1 = QHBoxLayout()
        label_motivo = QLabel("Motivo:")
        self.combo_motivo = QComboBox()
        self.combo_motivo.setPlaceholderText("Seleccione un motivo")
        fila1.addWidget(label_motivo)
        fila1.addWidget(self.combo_motivo)

        label_urgencia = QLabel("Urgencia:")
        self.combo_urgencia = QComboBox()
        self.combo_urgencia.setPlaceholderText(
            "Seleccione un grado de urgencia")
        fila1.addWidget(label_urgencia)
        fila1.addWidget(self.combo_urgencia)

        label_fecha = QLabel("Fecha Recepción:")
        self.fecha_recepcion = QDateEdit()
        self.fecha_recepcion.setDisplayFormat("dd-MM-yyyy")
        self.fecha_recepcion.setDate(QDate.currentDate())
        self.fecha_recepcion.setFixedWidth(110)
        fila1.addWidget(label_fecha)
        fila1.addWidget(self.fecha_recepcion)
        layout.addLayout(fila1)

        # Fila 2: Checkboxes
        fila2 = QHBoxLayout()
        self.check_arranca = QCheckBox("Arranca")
        self.check_grua = QCheckBox("Viene con grúa")
        self.check_itv = QCheckBox("ITV en vigor")
        self.check_presupuesto_escrito = QCheckBox("Presupuesto escrito")
        fila2.addWidget(self.check_arranca)
        fila2.addWidget(self.check_grua)
        fila2.addWidget(self.check_itv)
        fila2.addWidget(self.check_presupuesto_escrito)
        layout.addLayout(fila2)

        # Fila 3: Tiene seguro y compañía
        fila3 = QHBoxLayout()
        self.check_seguro = QCheckBox("Tiene seguro")
        label_compania = QLabel("Compañía Seguro:")
        self.input_compania = QLineEdit()
        self.input_compania.setPlaceholderText(
            "Nombre del seguro y Nº de póliza")
        fila3.addWidget(self.check_seguro)
        fila3.addWidget(label_compania)
        fila3.addWidget(self.input_compania)
        layout.addLayout(fila3)

        # Fila 4: Última revisión, reparación hasta y valor estimado
        fila4 = QHBoxLayout()
        label_revision = QLabel("Última revisión:")
        self.input_ultima_revision = QLineEdit()
        fila4.addWidget(label_revision)
        fila4.addWidget(self.input_ultima_revision)

        label_reparacion = QLabel("Reparación hasta:")
        self.input_max_autorizado = QLineEdit()
        self.input_max_autorizado.setMaxLength(4)
        self.input_max_autorizado.setFixedWidth(80)
        euro1 = QLabel("€")
        fila4.addWidget(label_reparacion)
        fila4.addWidget(self.input_max_autorizado)
        fila4.addWidget(euro1)

        label_valor = QLabel("Valor estimado:")
        self.input_valor_estimado = QLineEdit()
        self.input_valor_estimado.setMaxLength(4)
        self.input_valor_estimado.setFixedWidth(80)
        euro2 = QLabel("€")
        fila4.addWidget(label_valor)
        fila4.addWidget(self.input_valor_estimado)
        fila4.addWidget(euro2)
        layout.addLayout(fila4)

        # Fila 5-7: TextAreas
        layout.addWidget(QLabel("Estado exterior:"))
        self.input_estado_exterior = QTextEdit()
        layout.addWidget(self.input_estado_exterior)

        layout.addWidget(QLabel("Estado interior:"))
        self.input_estado_interior = QTextEdit()
        layout.addWidget(self.input_estado_interior)

        layout.addWidget(QLabel("Observaciones generales:"))
        self.input_observaciones = QTextEdit()
        layout.addWidget(self.input_observaciones)

        return grupo['grupo']

    def crear_seccion_entrega_documento(self):
        grupo = self.crear_seccion_plegable("Entrega del documento")
        layout = QVBoxLayout()
        grupo['contenido'].setLayout(layout)

        # Fila 1: Nº Recepcionamiento y checkboxes
        fila1 = QHBoxLayout()
        label_numero_recepcion = QLabel("Nº Recepcionamiento:")
        label_numero_recepcion.setAlignment(Qt.AlignVCenter)
        self.input_numero_recepcion = QLineEdit()
        self.input_numero_recepcion.setMaxLength(9)
        self.input_numero_recepcion.setFixedWidth(120)
        self.checkbox_imprimir = QCheckBox("Imprimir")
        self.checkbox_enviar_correo = QCheckBox("Enviar por correo")

        fila1.addWidget(label_numero_recepcion)
        fila1.addWidget(self.input_numero_recepcion)
        fila1.addSpacing(20)
        fila1.addWidget(self.checkbox_imprimir)
        fila1.addSpacing(10)
        fila1.addWidget(self.checkbox_enviar_correo)
        fila1.addStretch()
        fila1.setAlignment(Qt.AlignLeft)
        layout.addLayout(fila1)

        # Fila 2: Campo correo alineado a la izquierda
        fila2 = QHBoxLayout()
        label_correo = QLabel("Correo destino:")
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo electrónico destino")
        self.input_correo.setEnabled(False)
        self.checkbox_enviar_correo.stateChanged.connect(
            lambda estado: self.input_correo.setEnabled(
                estado == Qt.CheckState.Checked)
        )
        fila2.addWidget(label_correo)
        fila2.addWidget(self.input_correo)
        fila2.addStretch()
        layout.addLayout(fila2)

        # Fila 3: Firma
        fila3 = QVBoxLayout()
        label_firma = QLabel("Firma del cliente:")
        self.zona_firma = QLabel("[ Aquí se capturará la firma ⬇️ ]")
        self.zona_firma.setStyleSheet(
            "background-color: white; border: 1px solid #ccc; min-height: 100px; max-width: 400px;")
        fila3.addWidget(label_firma)
        fila3.addWidget(self.zona_firma)
        fila1.setAlignment(Qt.AlignLeft)
        layout.addLayout(fila3)

        # Fila 4: Ruta de guardado
        fila4 = QHBoxLayout()
        self.checkbox_ruta_predeterminada = QCheckBox(
            "Guardar en la ruta por defecto")
        layout.addWidget(self.checkbox_ruta_predeterminada)

        fila5 = QHBoxLayout()
        self.input_ruta_guardado = QLineEdit()
        self.boton_buscar_ruta = QPushButton("Seleccionar carpeta")
        self.boton_buscar_ruta.clicked.connect(self.seleccionar_ruta_guardado)
        fila5.addWidget(self.input_ruta_guardado)
        fila5.addWidget(self.boton_buscar_ruta)
        layout.addLayout(fila5)

        return grupo['grupo']

    def seleccionar_ruta_guardado(self):
        ruta = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta de guardado")
        if ruta:
            self.input_ruta_guardado.setText(ruta)
