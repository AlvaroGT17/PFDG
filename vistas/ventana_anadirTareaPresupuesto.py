"""
Módulo para el diálogo de creación de tareas en presupuestos dentro del sistema ReyBoxes.

Permite al usuario introducir el nombre de una tarea, su duración en horas y el precio por hora.
Realiza validaciones en tiempo real y muestra mensajes de error con retroalimentación visual.
Al aceptar, devuelve los valores introducidos, incluyendo el coste total de la tarea.
"""

from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel
from utilidades.rutas import obtener_ruta_absoluta


class DialogoTarea(QDialog):
    """
    Diálogo modal para introducir una tarea con duración y precio por hora.

    Incluye validación visual de los campos y animación en caso de errores.

    Métodos principales:
        - obtener_datos(): Devuelve los valores ingresados como tupla.
        - validar_y_aceptar(): Valida el contenido y acepta el diálogo si es correcto.
        - actualizar_estado_boton(): Habilita o deshabilita el botón aceptar según los datos.
    """

    def __init__(self):
        """
        Inicializa el diálogo, configurando estilos visuales, campos de entrada,
        validaciones y layout general del formulario.
        """
        super().__init__()

        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setWindowTitle("Nueva tarea")
        self.setObjectName("ventana_dialogo_tarea")

        self.setMinimumWidth(400)
        self.setSizeGripEnabled(False)

        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 15, 20, 15)
        self.layout_principal.setSpacing(10)

        self.cargar_estilos()
        self.init_ui()

        self.adjustSize()

    def cargar_estilos(self):
        """
        Carga la fuente personalizada y el archivo CSS para aplicar estilos visuales al diálogo.
        """
        QFontDatabase.addApplicationFont(
            "font/Montserrat-Italic-VariableFont_wght.ttf"
        )
        try:
            ruta_css = obtener_ruta_absoluta("css/anadirTareaPresupuesto.css")
            with open(ruta_css, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("❌ No se pudo cargar el CSS del diálogo:", e)

    def init_ui(self):
        """
        Construye el formulario principal del diálogo para introducir los datos de la tarea.

        Incluye:
            - Campo de texto para la descripción de la tarea.
            - Campos para duración (horas) y precio por hora.
            - Mensajes de error en tiempo real.
            - Botones de acción: Aceptar y Cancelar.
        """
        formulario = QFormLayout()

        self.campo_tarea = QLineEdit()
        self.campo_tarea.setPlaceholderText("Introduce la tarea")
        formulario.addRow("Tarea:", self.campo_tarea)

        self.campo_horas = QLineEdit()
        self.campo_horas.setPlaceholderText("Introduce el número de horas")
        formulario.addRow("Horas:", self.campo_horas)

        self.mensaje_error_horas = QLabel(
            "⚠️ Las horas deben ser un número decimal.")
        self.mensaje_error_horas.setObjectName("mensaje_error")
        self.mensaje_error_horas.setVisible(False)
        formulario.addRow("", self.mensaje_error_horas)

        self.campo_precio = QLineEdit()
        self.campo_precio.setPlaceholderText("Introduce el precio por hora")
        formulario.addRow("Precio/hora:", self.campo_precio)

        self.mensaje_error_precio = QLabel(
            "⚠️ El precio debe ser un número decimal.")
        self.mensaje_error_precio.setObjectName("mensaje_error")
        self.mensaje_error_precio.setVisible(False)
        formulario.addRow("", self.mensaje_error_precio)

        self.layout_principal.addLayout(formulario)

        botones = QHBoxLayout()
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setIcon(
            QIcon(obtener_ruta_absoluta("img/guardar.png")))
        self.boton_aceptar.setEnabled(False)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))

        botones.addWidget(self.boton_aceptar)
        botones.addWidget(self.boton_cancelar)
        self.layout_principal.addLayout(botones)

        self.boton_aceptar.clicked.connect(self.validar_y_aceptar)
        self.boton_cancelar.clicked.connect(self.reject)

        self.campo_tarea.textChanged.connect(self.actualizar_estado_boton)
        self.campo_horas.textChanged.connect(self.validar_horas_en_tiempo_real)
        self.campo_precio.textChanged.connect(
            self.validar_precio_en_tiempo_real)

    def validar_horas_en_tiempo_real(self):
        """
        Valida en tiempo real que el campo de horas contenga un valor decimal válido.
        Muestra un mensaje y animación si hay error.
        """
        texto = self.campo_horas.text().strip()
        try:
            if texto:
                float(texto)
            self._ocultar_error(self.mensaje_error_horas, self.campo_horas)
        except ValueError:
            self._mostrar_error(self.mensaje_error_horas, self.campo_horas)
        self.actualizar_estado_boton()

    def validar_precio_en_tiempo_real(self):
        """
        Valida en tiempo real que el campo de precio contenga un valor decimal válido.
        Muestra un mensaje y animación si hay error.
        """
        texto = self.campo_precio.text().strip()
        try:
            if texto:
                float(texto)
            self._ocultar_error(self.mensaje_error_precio, self.campo_precio)
        except ValueError:
            self._mostrar_error(self.mensaje_error_precio, self.campo_precio)
        self.actualizar_estado_boton()

    def actualizar_estado_boton(self):
        """
        Habilita el botón "Aceptar" solo si todos los campos son válidos y no están vacíos.
        """
        tarea_ok = self.campo_tarea.text().strip() != ""
        horas_ok = not self.mensaje_error_horas.isVisible(
        ) and self.campo_horas.text().strip() != ""
        precio_ok = not self.mensaje_error_precio.isVisible(
        ) and self.campo_precio.text().strip() != ""
        self.boton_aceptar.setEnabled(tarea_ok and horas_ok and precio_ok)

    def validar_y_aceptar(self):
        """
        Realiza una validación final de los campos y acepta el diálogo si todo es correcto.
        """
        self.validar_horas_en_tiempo_real()
        self.validar_precio_en_tiempo_real()
        if self.boton_aceptar.isEnabled():
            self.accept()

    def _mostrar_error(self, etiqueta, campo):
        """
        Muestra el mensaje de error asociado a un campo y aplica una animación.

        Args:
            etiqueta (QLabel): Etiqueta que muestra el error.
            campo (QLineEdit): Campo donde se produjo el error.
        """
        etiqueta.setVisible(True)
        campo.setProperty("error", True)
        campo.style().unpolish(campo)
        campo.style().polish(campo)
        self._animar_error(campo)
        self.adjustSize()

    def _ocultar_error(self, etiqueta, campo):
        """
        Oculta el mensaje de error asociado a un campo y restaura su estilo normal.

        Args:
            etiqueta (QLabel): Etiqueta de error a ocultar.
            campo (QLineEdit): Campo validado correctamente.
        """
        etiqueta.setVisible(False)
        campo.setProperty("error", False)
        campo.style().unpolish(campo)
        campo.style().polish(campo)
        self.adjustSize()

    def _animar_error(self, widget):
        """
        Aplica una animación de sacudida horizontal para destacar un campo con error.

        Args:
            widget (QWidget): Campo a animar.
        """
        anim = QPropertyAnimation(widget, b"geometry", self)
        rect = widget.geometry()
        anim.setDuration(150)
        anim.setKeyValueAt(0, rect)
        anim.setKeyValueAt(0.25, QRect(
            rect.x() - 5, rect.y(), rect.width(), rect.height()))
        anim.setKeyValueAt(0.5, rect)
        anim.setKeyValueAt(0.75, QRect(
            rect.x() + 5, rect.y(), rect.width(), rect.height()))
        anim.setKeyValueAt(1, rect)
        anim.start()

    def obtener_datos(self):
        """
        Devuelve los datos introducidos por el usuario y calcula el total.

        Returns:
            tuple: Una tupla con (tarea, horas, precio, total), o `None` si los valores no son válidos.
        """
        try:
            tarea = self.campo_tarea.text().strip()
            horas = float(self.campo_horas.text().strip())
            precio = float(self.campo_precio.text().strip())
            total = horas * precio
            return tarea, horas, precio, total
        except ValueError:
            return None
