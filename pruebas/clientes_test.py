"""
Módulo de prueba para lanzar la ventana de gestión de clientes (`VentanaClientes`).

Permite:
- Ejecutar y probar la ventana desde herramientas de testeo.
- Reutilizar la función `iniciar_ventana_clientes()` desde scripts o visores interactivos.

Forma parte del entorno de pruebas visuales y funcionales de ReyBoxes.
"""

from vistas.ventana_clientes import VentanaClientes


def iniciar_ventana_clientes():
    """
    Crea y devuelve una instancia de la ventana de clientes sin ventana padre.

    Esta función está pensada para ser usada en:
    - Test visual manual.
    - Visores de pruebas (`SelectorVentana`).
    - Scripts de validación.

    Returns:
        VentanaClientes: Instancia inicializada lista para mostrar.
    """
    return VentanaClientes(None)

# para ejecutar el modulo desde consola:
# python -m pruebas.clientes_test
