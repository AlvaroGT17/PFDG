"""
Módulo de utilidad para iniciar manualmente la ventana de carga animada (`VentanaCargaGif`).

Este módulo encapsula la creación de la ventana de carga con GIF animado, permitiendo
su reutilización en pruebas unitarias, test visuales o llamadas internas desde otros módulos.

Forma parte del entorno gráfico del sistema ReyBoxes.
"""

from vistas.ventana_carga_gif import VentanaCargaGif


def iniciar_ventana_carga_gif():
    """
    Crea y devuelve una instancia de la ventana de carga con animación GIF.

    Esta función es útil para:
    - Pruebas visuales.
    - Mostrar carga en procesos bloqueantes de interfaz.
    - Usarla como componente reutilizable.

    Returns:
        VentanaCargaGif: Instancia lista para ser mostrada.
    """
    return VentanaCargaGif()

# para ejecutar el modulo desde consola:
# python -m pruebas.carga_gif_test
