"""
TESTS DE UTILIDAD: Validación de rutas absolutas

Este módulo prueba la función `obtener_ruta_absoluta` definida en
`utilidades/rutas.py`.

Objetivo:
---------
Comprobar que se puede localizar correctamente el archivo CSS
de la pantalla de verificación ('css/verificar_codigo.css').

Esto garantiza que:
- La función de rutas funciona correctamente en entornos reales.
- El archivo requerido para aplicar estilos está presente en el proyecto.
- Las rutas se resuelven de forma robusta incluso al ejecutarse desde carpetas distintas.

Relevancia:
-----------
Una ruta mal construida o un archivo faltante puede hacer que la interfaz gráfica
pierda estilos visuales, lo que afectaría directamente la experiencia del usuario.
"""

import os
from utilidades.rutas import obtener_ruta_absoluta


def test_ruta_css_verificar_codigo():
    """
    TEST: Resolución de ruta del CSS 'verificar_codigo.css'

    Usa la función `obtener_ruta_absoluta` para construir la ruta completa
    hacia el archivo de estilos de la ventana de verificación.

    Assertions:
    - La ruta resultante debe apuntar a un archivo que realmente exista
      en el sistema de archivos.
    """
    ruta = obtener_ruta_absoluta("css/verificar_codigo.css")
    assert os.path.exists(ruta), f"El archivo no se encuentra en: {ruta}"


if __name__ == "__main__":
    print("Ruta CSS verificada:", obtener_ruta_absoluta(
        "css/verificar_codigo.css"))
