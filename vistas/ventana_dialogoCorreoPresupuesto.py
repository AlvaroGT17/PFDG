from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class VentanaDialogoCorreoPresupuesto(QDialog):
    def __init__(self, correo_defecto="", parent=None):
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
        return self.campo_correo.text().strip()
