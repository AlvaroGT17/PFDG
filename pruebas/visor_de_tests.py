"""
Visor interactivo para abrir manualmente cualquier ventana del sistema ReyBoxes.
Solo para uso en entorno de desarrollo.

Permite al desarrollador seleccionar una ventana específica desde una lista
y lanzarla para pruebas visuales o funcionales individuales.
"""

import sys
from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox
from pruebas.verificar_test import iniciar_ventana_verificar
from pruebas.vehiculos_test import iniciar_ventana_vehiculos

# Diccionario que relaciona el nombre de la ventana con su función de apertura
ventanas_disponibles = {
    "Ventana Verificar": iniciar_ventana_verificar,
    "Ventana Vehículos": iniciar_ventana_vehiculos,
}


class SelectorVentana(QWidget):
    """
    Ventana de selección para pruebas de desarrollo.

    Muestra una lista con las ventanas disponibles para testeo y un botón
    para abrir la ventana seleccionada. Pensado exclusivamente para uso
    en entorno de desarrollo, no debe formar parte del sistema en producción.
    """

    def __init__(self):
        """
        Inicializa la interfaz con una lista de ventanas disponibles y un botón de acción.
        """
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
        """
        Llama a la función correspondiente a la ventana seleccionada en la lista.

        Si no hay selección válida, se muestra una advertencia.
        """
        nombre = self.lista.currentItem().text()
        if nombre and nombre in ventanas_disponibles:
            ventana = ventanas_disponibles[nombre]()
            ventana.show()
        else:
            QMessageBox.warning(
                self, "Aviso", "Selecciona una ventana válida."
            )


if __name__ == "__main__":
    """
    Punto de entrada para lanzar el visor desde consola o entorno de pruebas.

    Crea la aplicación y muestra la ventana de selección de pruebas.
    """
    app = QApplication(sys.argv)
    selector = SelectorVentana()
    selector.show()
    sys.exit(app.exec())

# para ejecutar el modulo desde consola:
# python -m pruebas.visor_de_tests
