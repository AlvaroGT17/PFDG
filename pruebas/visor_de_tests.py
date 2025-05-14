"""
Visor interactivo para abrir manualmente cualquier ventana del sistema ReyBoxes.
Solo para uso en entorno de desarrollo.
"""

import sys
from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox
from pruebas.verificar_test import iniciar_ventana_verificar
from pruebas.vehiculos_test import iniciar_ventana_vehiculos  # 👈 Añadido

ventanas_disponibles = {
    "Ventana Verificar": iniciar_ventana_verificar,
    "Ventana Vehículos": iniciar_ventana_vehiculos,  # 👈 Añadido
    # Agrega más a medida que los refactorices
}


class SelectorVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Visor de pruebas ReyBoxes")
        self.setMinimumSize(300, 400)

        self.lista = QListWidget()
        self.lista.addItems(ventanas_disponibles.keys())

        self.boton_abrir = QPushButton("Abrir ventana seleccionada")
        self.boton_abrir.clicked.connect(self.abrir_ventana)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lista)
        layout.addWidget(self.boton_abrir)

    def abrir_ventana(self):
        nombre = self.lista.currentItem().text()
        if nombre and nombre in ventanas_disponibles:
            ventana = ventanas_disponibles[nombre]()
            ventana.show()
        else:
            QMessageBox.warning(
                self, "Aviso", "Selecciona una ventana válida.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = SelectorVentana()
    selector.show()
    sys.exit(app.exec())
