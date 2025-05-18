"""
Módulo para la ventana de fichaje del personal en el sistema ReyBoxes.

Permite a los usuarios registrar su entrada o salida del trabajo mediante una interfaz gráfica,
que incluye un reloj en tiempo real, selección de tipo de fichaje y botones de acción.

La ventana se comporta como modal, deshabilitando el cierre con el botón (❌) para forzar
el uso del botón "Volver".
"""

from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QTime, Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QHBoxLayout, QMessageBox, QButtonGroup, QToolButton
from utilidades.rutas import obtener_ruta_absoluta


class VentanaFichar(QWidget):
    """
    Ventana modal para registrar el fichaje de entrada o salida del personal.

    Esta interfaz muestra un reloj en tiempo real, permite seleccionar el tipo de fichaje
    (Entrada o Salida), y dispone de botones para confirmar la acción o volver al menú principal.
    El botón de cierre (❌) está deshabilitado para obligar al usuario a usar "Volver".

    Atributos:
        reloj_label (QLabel): Etiqueta que muestra la hora actual.
        radio_entrada (QRadioButton): Botón para fichaje de entrada.
        radio_salida (QRadioButton): Botón para fichaje de salida.
        btn_confirmar (QToolButton): Botón para confirmar el fichaje.
        btn_volver (QToolButton): Botón para volver al menú principal.
    """

    def __init__(self):
        """
        Inicializa la ventana de fichaje, cargando estilos, configurando el diseño
        y activando el reloj en vivo.
        """
        super().__init__()
        self.setWindowTitle("Fichaje de personal")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowModality(Qt.ApplicationModal)

        ruta_css = obtener_ruta_absoluta("css/fichar.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.inicializar_ui()
        self.iniciar_reloj()

    def inicializar_ui(self):
        """
        Configura la interfaz gráfica de la ventana:
        - Muestra la hora actual en tiempo real.
        - Ofrece botones de selección para fichaje de Entrada o Salida.
        - Añade botones "Confirmar" y "Volver" con sus respectivos iconos.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Línea de texto y hora
        fila_hora = QHBoxLayout()
        label_texto = QLabel("Hora actual:")
        label_texto.setObjectName("texto_hora")

        self.reloj_label = QLabel("00:00:00")
        self.reloj_label.setObjectName("reloj")

        fila_hora.addStretch()
        fila_hora.addWidget(label_texto)
        fila_hora.addWidget(self.reloj_label)
        fila_hora.addStretch()
        layout.addLayout(fila_hora)

        # Opciones Entrada/Salida centradas
        self.radio_entrada = QRadioButton("Entrada")
        self.radio_salida = QRadioButton("Salida")

        grupo = QButtonGroup(self)
        grupo.addButton(self.radio_entrada)
        grupo.addButton(self.radio_salida)

        layout_radios = QVBoxLayout()
        layout_radios.addWidget(self.radio_entrada, alignment=Qt.AlignCenter)
        layout_radios.addWidget(self.radio_salida, alignment=Qt.AlignCenter)
        layout.addLayout(layout_radios)

        # Botones inferiores tipo menú
        botones_layout = QHBoxLayout()

        self.btn_confirmar = QToolButton()
        self.btn_confirmar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_confirmar.setIcon(
            QIcon(obtener_ruta_absoluta("img/check.png")))
        self.btn_confirmar.setIconSize(QSize(48, 48))
        self.btn_confirmar.setText("Confirmar")
        self.btn_confirmar.setObjectName("boton_menu")
        self.btn_confirmar.setToolTip(
            "Registrar fichaje con la opción seleccionada")
        self.btn_confirmar.setFixedSize(120, 100)

        self.btn_volver = QToolButton()
        self.btn_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_volver.setIcon(QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.btn_volver.setIconSize(QSize(48, 48))
        self.btn_volver.setText("Volver")
        self.btn_volver.setObjectName("boton_menu")
        self.btn_volver.setToolTip("Volver al menú principal")
        self.btn_volver.setFixedSize(120, 100)
        self.btn_volver.clicked.connect(self.close)

        botones_layout.addWidget(self.btn_confirmar)
        botones_layout.addWidget(self.btn_volver)
        layout.addLayout(botones_layout)

    def iniciar_reloj(self):
        """
        Inicia un temporizador que actualiza la hora cada segundo.
        La hora se muestra en formato HH:mm:ss.
        """
        timer = QTimer(self)
        timer.timeout.connect(self.actualizar_reloj)
        timer.start(1000)
        self.actualizar_reloj()

    def actualizar_reloj(self):
        """
        Actualiza el texto del reloj con la hora actual del sistema.
        """
        hora_actual = QTime.currentTime().toString("HH:mm:ss")
        self.reloj_label.setText(hora_actual)

    def obtener_tipo_fichaje(self):
        """
        Devuelve el tipo de fichaje seleccionado por el usuario.

        Returns:
            str | None: "ENTRADA", "SALIDA" o None si no se ha seleccionado ninguna opción.
        """
        if self.radio_entrada.isChecked():
            return "ENTRADA"
        elif self.radio_salida.isChecked():
            return "SALIDA"
        return None

    def mostrar_error(self, mensaje):
        """
        Muestra un cuadro de advertencia con el mensaje proporcionado.

        Args:
            mensaje (str): Mensaje a mostrar en el cuadro de diálogo.
        """
        QMessageBox.warning(self, "Fichaje inválido", mensaje)

    def mostrar_confirmacion(self, mensaje):
        """
        Muestra un cuadro de información indicando que el fichaje fue registrado correctamente.

        Args:
            mensaje (str): Mensaje a mostrar en el cuadro de diálogo.
        """
        QMessageBox.information(self, "Fichaje registrado", mensaje)
