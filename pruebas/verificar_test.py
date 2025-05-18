"""
Módulo de prueba para lanzar y testear la ventana de verificación de código (`VentanaVerificar`).

Este módulo permite:
- Ejecutar manualmente la ventana desde consola (`python -m pruebas.verificar_test`)
- Reutilizar la función `iniciar_ventana_verificar()` en pruebas automáticas con `pytest`

Forma parte del sistema ReyBoxes y está diseñado para facilitar validaciones sin bloquear la interfaz gráfica.
"""

from vistas.ventana_verificar import VentanaVerificar


def iniciar_ventana_verificar():
    """
    Crea y devuelve una instancia de la ventana de verificación de código.

    Esta función es útil para ser invocada desde otros módulos de test o desde un visor
    de ventanas como `SelectorVentana`.

    Returns:
        VentanaVerificar: Instancia de la ventana lista para ser mostrada o testeada.
    """
    return VentanaVerificar()


if __name__ == "__main__":
    """
    Punto de entrada para ejecutar manualmente la ventana de verificación.

    Lanza una aplicación Qt y muestra la ventana `VentanaVerificar`.
    Este modo está pensado para pruebas visuales individuales.
    """
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = iniciar_ventana_verificar()
    ventana.show()
    sys.exit(app.exec())

# para ejecutar el modulo desde consola:
# python -m pruebas.verificar_test
