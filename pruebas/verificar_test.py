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
    Devuelve una instancia de la ventana de verificación de código sin mostrarla.

    Returns:
        VentanaVerificar: Instancia de la ventana lista para pruebas.
    """
    return VentanaVerificar()


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, se lanza la ventana de forma manual
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = iniciar_ventana_verificar()
    ventana.show()
    sys.exit(app.exec())
