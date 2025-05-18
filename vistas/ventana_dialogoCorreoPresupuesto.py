"""
Módulo para el diálogo de envío de presupuestos por correo electrónico en ReyBoxes.

Esta ventana modal solicita al usuario que introduzca un correo electrónico
para enviar el presupuesto correspondiente. Se puede establecer un valor por defecto
y se utilizan botones estándar para confirmar o cancelar la operación.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class VentanaDialogoCorreoPresupuesto(QDialog):
    """
    Diálogo modal para introducir un correo electrónico al que se enviará un presupuesto.

    Esta ventana solicita al usuario un correo, mostrando por defecto un valor si se proporciona,
    y permite confirmar o cancelar la acción mediante botones estándar (Aceptar / Cancelar).

    Atributos:
        campo_correo (QLineEdit): Campo de entrada donde el usuario escribe el correo.
    """

    def __init__(self, correo_defecto="", parent=None):
        """
        Inicializa el diálogo con un campo para ingresar el correo y botones de acción.

        Args:
            correo_defecto (str): Correo que se mostrará inicialmente en el campo de entrada.
            parent (QWidget, optional): Widget padre del diálogo, si lo hay.
        """
        super().__init__(parent)
        self.setWindowTitle("Enviar presupuesto por correo")

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Introduce el correo al que deseas enviar el presupuesto:"))

        self.campo_correo = QLineEdit()
        self.campo_correo.setText(correo_defecto)
        layout.addWidget(self.campo_correo)

        botones = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        self.setLayout(layout)

    def obtener_correo(self):
        """
        Devuelve el correo electrónico introducido en el campo de texto, sin espacios.

        Returns:
            str: Correo electrónico ingresado por el usuario.
        """
        return self.campo_correo.text().strip()
