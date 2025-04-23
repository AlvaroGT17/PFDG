from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QFormLayout, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase


class VentanaPresupuesto(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Presupuestos")
        self.setFixedSize(600, 500)

        self.cargar_estilos()
        self.init_ui()

    def cargar_estilos(self):
        # Fuente personalizada (opcional)
        QFontDatabase.addApplicationFont(
            "font/Montserrat-Italic-VariableFont_wght.ttf")

        # Aplicar estilos CSS
        try:
            with open("css/presupuesto.css", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("No se pudo cargar el CSS:", e)

    def init_ui(self):
        layout_principal = QVBoxLayout(self)

        # Título
        titulo = QLabel("Gestión de Presupuestos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #e30613;")
        layout_principal.addWidget(titulo)

        # Buscador
        layout_busqueda = QHBoxLayout()
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText(
            "Buscar por nº recepción o matrícula")
        self.boton_buscar = QPushButton("Buscar")
        layout_busqueda.addWidget(self.campo_busqueda)
        layout_busqueda.addWidget(self.boton_buscar)
        layout_principal.addLayout(layout_busqueda)

        # Formulario de datos
        formulario = QFormLayout()
        self.campo_cliente = QLineEdit()
        self.campo_cliente.setReadOnly(True)
        self.campo_vehiculo = QLineEdit()
        self.campo_vehiculo.setReadOnly(True)
        self.campo_fecha = QLineEdit()
        self.campo_fecha.setReadOnly(True)
        self.campo_limite = QLineEdit()
        self.campo_limite.setReadOnly(True)

        formulario.addRow("Cliente:", self.campo_cliente)
        formulario.addRow("Vehículo:", self.campo_vehiculo)
        formulario.addRow("Fecha recepción:", self.campo_fecha)
        formulario.addRow("Precio máx autorizado:", self.campo_limite)
        layout_principal.addLayout(formulario)

        # Observaciones
        self.texto_observaciones = QTextEdit()
        self.texto_observaciones.setPlaceholderText(
            "Observaciones del diagnóstico...")
        layout_principal.addWidget(self.texto_observaciones)

        # Coste estimado
        layout_coste = QHBoxLayout()
        etiqueta_coste = QLabel("Coste estimado:")
        self.campo_coste = QDoubleSpinBox()
        self.campo_coste.setMaximum(100000)
        self.campo_coste.setSuffix(" €")
        self.campo_coste.setDecimals(2)
        layout_coste.addWidget(etiqueta_coste)
        layout_coste.addWidget(self.campo_coste)
        layout_principal.addLayout(layout_coste)

        # Autorización directa
        self.etiqueta_autorizado = QLabel("✓ Autorizado automáticamente")
        self.etiqueta_autorizado.setObjectName("etiqueta_autorizado")
        self.etiqueta_autorizado.setVisible(False)
        layout_principal.addWidget(self.etiqueta_autorizado)

        # Respuesta cliente
        layout_principal.addWidget(
            QLabel("Respuesta del cliente (si aplica):"))
        self.combo_respuesta = QComboBox()
        self.combo_respuesta.addItems(
            ["", "Aceptado", "Rechazado", "En espera"])
        layout_principal.addWidget(self.combo_respuesta)

        # Botones
        layout_botones = QHBoxLayout()
        self.boton_guardar = QPushButton("💾 Guardar presupuesto")
        self.boton_volver = QPushButton("🔙 Volver")
        layout_botones.addWidget(self.boton_guardar)
        layout_botones.addWidget(self.boton_volver)
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)
