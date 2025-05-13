from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel
from utilidades.rutas import obtener_ruta_absoluta


class DialogoTarea(QDialog):
    """
    Diálogo modal para introducir una tarea con duración y precio por hora.

    Métodos:
        obtener_datos(): Devuelve los valores ingresados como una tupla.
        validar_y_aceptar(): Valida y acepta el diálogo si los datos son correctos.
        actualizar_estado_boton(): Habilita o deshabilita el botón aceptar según los datos ingresados.
    """

    def __init__(self):
        """Inicializa el diálogo, configurando el estilo y la interfaz."""
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
        """Carga la fuente personalizada y el estilo CSS del diálogo."""
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

        Este método define y organiza los siguientes elementos:
        - Un campo de texto para la descripción de la tarea.
        - Campos de texto para el número de horas y precio por hora.
        - Etiquetas para mostrar errores de validación en horas y precio.
        - Botones para aceptar o cancelar la operación.

        También conecta los campos a validaciones en tiempo real y actualiza dinámicamente
        el estado del botón "Aceptar" según la validez de los datos ingresados.
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
        """Valida que el campo de horas contenga un número decimal válido."""
        texto = self.campo_horas.text().strip()
        try:
            if texto:
                float(texto)
            self._ocultar_error(self.mensaje_error_horas, self.campo_horas)
        except ValueError:
            self._mostrar_error(self.mensaje_error_horas, self.campo_horas)

        self.actualizar_estado_boton()

    def validar_precio_en_tiempo_real(self):
        """Valida que el campo de precio contenga un número decimal válido."""
        texto = self.campo_precio.text().strip()
        try:
            if texto:
                float(texto)
            self._ocultar_error(self.mensaje_error_precio, self.campo_precio)
        except ValueError:
            self._mostrar_error(self.mensaje_error_precio, self.campo_precio)

        self.actualizar_estado_boton()

    def actualizar_estado_boton(self):
        """Habilita el botón de aceptar si todos los campos están correctamente validados."""
        tarea_ok = self.campo_tarea.text().strip() != ""
        horas_ok = not self.mensaje_error_horas.isVisible(
        ) and self.campo_horas.text().strip() != ""
        precio_ok = not self.mensaje_error_precio.isVisible(
        ) and self.campo_precio.text().strip() != ""
        self.boton_aceptar.setEnabled(tarea_ok and horas_ok and precio_ok)

    def validar_y_aceptar(self):
        """Realiza una última validación y cierra el diálogo si es válida."""
        self.validar_horas_en_tiempo_real()
        self.validar_precio_en_tiempo_real()
        if self.boton_aceptar.isEnabled():
            self.accept()

    def _mostrar_error(self, etiqueta, campo):
        """Muestra el mensaje de error y aplica animación visual al campo."""
        etiqueta.setVisible(True)
        campo.setProperty("error", True)
        campo.style().unpolish(campo)
        campo.style().polish(campo)
        self._animar_error(campo)
        self.adjustSize()

    def _ocultar_error(self, etiqueta, campo):
        """Oculta el mensaje de error y restaura el estilo normal del campo."""
        etiqueta.setVisible(False)
        campo.setProperty("error", False)
        campo.style().unpolish(campo)
        campo.style().polish(campo)
        self.adjustSize()

    def _animar_error(self, widget):
        """Aplica una animación de sacudida al campo en caso de error."""
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
        """Obtiene los datos ingresados y calcula el total.

        Returns:
            tuple: (tarea, horas, precio, total) o None si hay error.
        """
        try:
            tarea = self.campo_tarea.text().strip()
            horas = float(self.campo_horas.text().strip())
            precio = float(self.campo_precio.text().strip())
            total = horas * precio
            return tarea, horas, precio, total
        except ValueError:
            return None
