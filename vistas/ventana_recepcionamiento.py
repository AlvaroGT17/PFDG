from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QTextEdit, QComboBox, QRadioButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QDateEdit, QButtonGroup,
    QWidget, QStackedLayout, QScrollArea, QToolButton, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QSize
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
                      self.input_anio, self.input_kilometros, self.input_combustible, self.input_vin,
                      self.input_compania, self.input_averias, self.input_valor_estimado,
                      self.input_estado_exterior, self.input_estado_interior, self.input_max_autorizado,
                      self.input_correo]:
            if isinstance(campo, (QLineEdit, QTextEdit)):
                campo.clear()

        self.combo_tipo.setCurrentIndex(-1)
        self.combo_urgencia.setCurrentIndex(0)

        self.radio_reparacion.setChecked(False)
        self.radio_tasacion.setChecked(False)
        self.radio_presupuesto.setChecked(False)
        self.radio_mantenimiento.setChecked(False)

        self.check_grua.setChecked(False)
        self.check_arranca.setChecked(False)
        self.check_seguro.setChecked(False)
        self.check_presupuesto_escrito.setChecked(False)
        self.checkbox_imprimir.setChecked(False)
        self.checkbox_enviar_correo.setChecked(False)

        self.stacked_motivo.setCurrentIndex(-1)

    def __init__(self):
        super().__init__()
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

        grupo_cliente = self.crear_seccion_plegable("Datos del Cliente")
        layout_cliente = QFormLayout()
        grupo_cliente['contenido'].setLayout(layout_cliente)
        self.input_nombre = QLineEdit()
        self.input_dni = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_email = QLineEdit()
        self.input_direccion = QLineEdit()
        layout_cliente.addRow("Nombre y apellidos:", self.input_nombre)
        layout_cliente.addRow("DNI:", self.input_dni)
        layout_cliente.addRow("Teléfono:", self.input_telefono)
        layout_cliente.addRow("Email:", self.input_email)
        layout_cliente.addRow("Dirección:", self.input_direccion)
        layout_scroll.addWidget(grupo_cliente['grupo'])

        grupo_vehiculo = self.crear_seccion_plegable("Datos del Vehículo")
        layout_vehiculo = QFormLayout()
        grupo_vehiculo['contenido'].setLayout(layout_vehiculo)
        self.input_matricula = QLineEdit()
        self.input_marca = QLineEdit()
        self.input_modelo = QLineEdit()
        self.input_color = QLineEdit()
        self.input_anio = QLineEdit()
        self.input_kilometros = QLineEdit()
        self.input_combustible = QLineEdit()
        self.input_vin = QLineEdit()
        self.combo_tipo = QComboBox()
        layout_vehiculo.addRow("Matrícula:", self.input_matricula)
        layout_vehiculo.addRow("Marca:", self.input_marca)
        layout_vehiculo.addRow("Modelo:", self.input_modelo)
        layout_vehiculo.addRow("Color:", self.input_color)
        layout_vehiculo.addRow("Año:", self.input_anio)
        layout_vehiculo.addRow("Kilómetros:", self.input_kilometros)
        layout_vehiculo.addRow("Combustible:", self.input_combustible)
        layout_vehiculo.addRow("Nº Bastidor (VIN):", self.input_vin)
        layout_vehiculo.addRow("Tipo de vehículo:", self.combo_tipo)
        layout_scroll.addWidget(grupo_vehiculo['grupo'])

        grupo_motivo = self.crear_seccion_plegable(
            "Motivo del Recepcionamiento")
        layout_motivo = QHBoxLayout()
        grupo_motivo['contenido'].setLayout(layout_motivo)
        self.radio_reparacion = QRadioButton("Reparación")
        self.radio_tasacion = QRadioButton("Tasación")
        self.radio_presupuesto = QRadioButton("Presupuesto")
        self.radio_mantenimiento = QRadioButton("Mantenimiento preventivo")

        self.grupo_motivo_radios = QButtonGroup()
        self.grupo_motivo_radios.addButton(self.radio_reparacion)
        self.grupo_motivo_radios.addButton(self.radio_tasacion)
        self.grupo_motivo_radios.addButton(self.radio_presupuesto)
        self.grupo_motivo_radios.addButton(self.radio_mantenimiento)

        layout_motivo.addWidget(self.radio_reparacion)
        layout_motivo.addWidget(self.radio_tasacion)
        layout_motivo.addWidget(self.radio_presupuesto)
        layout_motivo.addWidget(self.radio_mantenimiento)
        layout_scroll.addWidget(grupo_motivo['grupo'])

        grupo_entrega = self.crear_seccion_plegable("Entrega del documento")
        layout_entrega = QHBoxLayout()
        grupo_entrega['contenido'].setLayout(layout_entrega)
        self.checkbox_imprimir = QCheckBox("Imprimir")
        self.checkbox_enviar_correo = QCheckBox("Enviar por correo")
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo electrónico destino")
        self.input_correo.setEnabled(False)
        self.checkbox_enviar_correo.stateChanged.connect(
            lambda estado: self.input_correo.setEnabled(
                estado == Qt.CheckState.Checked)
        )
        layout_entrega.addWidget(self.checkbox_imprimir)
        layout_entrega.addWidget(self.checkbox_enviar_correo)
        layout_entrega.addWidget(self.input_correo)
        layout_scroll.addWidget(grupo_entrega['grupo'])

        layout_botones = QHBoxLayout()

        self.boton_confirmar = QToolButton()
        self.boton_confirmar.setText("Confirmar")
        self.boton_confirmar.setIcon(
            QIcon(obtener_ruta_absoluta("img/confirmar.png")))
        self.boton_confirmar.setIconSize(QSize(48, 48))
        self.boton_confirmar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_limpiar = QToolButton()
        self.boton_limpiar.setText("Limpiar")
        self.boton_limpiar.setIcon(
            QIcon(obtener_ruta_absoluta("img/escoba.png")))
        self.boton_limpiar.setIconSize(QSize(48, 48))
        self.boton_limpiar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.boton_limpiar.clicked.connect(self.confirmar_borrado)

        self.boton_cancelar = QToolButton()
        self.boton_cancelar.setText("Volver")
        self.boton_cancelar.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_cancelar.setIconSize(QSize(48, 48))
        self.boton_cancelar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones.addWidget(self.boton_confirmar)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_cancelar)
        layout_general.addLayout(layout_botones)

    def crear_seccion_plegable(self, titulo):
        grupo = QGroupBox()
        layout = QVBoxLayout(grupo)

        cabecera = QHBoxLayout()
        boton_toggle = QToolButton()
        icono_expandir = QIcon(obtener_ruta_absoluta("img/mas.png"))
        icono_colapsar = QIcon(obtener_ruta_absoluta("img/menos.png"))
        boton_toggle.setIcon(icono_colapsar)
        boton_toggle.setCheckable(True)
        boton_toggle.setChecked(True)
        boton_toggle.setIconSize(QSize(24, 24))
        etiqueta = QLabel(f"<b>{titulo}</b>")
        etiqueta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        etiqueta.setStyleSheet("color: white")

        cabecera.addWidget(etiqueta)
        cabecera.addWidget(boton_toggle)

        contenido = QWidget()
        contenido.setObjectName("contenido_plegable")

        def toggle():
            visible = boton_toggle.isChecked()
            contenido.setVisible(visible)
            boton_toggle.setIcon(icono_colapsar if visible else icono_expandir)

        boton_toggle.clicked.connect(toggle)

        layout.addLayout(cabecera)
        layout.addWidget(contenido)

        return {"grupo": grupo, "contenido": contenido}
