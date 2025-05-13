"""
Módulo de utilidad para impresión de archivos PDF.

Este módulo intenta imprimir archivos PDF utilizando dos métodos:
1. SumatraPDF si está instalado (modo silencioso).
2. El visor predeterminado del sistema mediante el comando `/p`.

En caso de fallo, se muestra un mensaje de advertencia al usuario.
"""

import os
import shutil
import subprocess
from PySide6.QtWidgets import QMessageBox


def imprimir_pdf(ruta_pdf, parent=None):
    """
    Intenta imprimir un archivo PDF utilizando el software disponible en el sistema.

    La función sigue un orden de preferencia:
    1. Imprimir con SumatraPDF (si está instalado), usando la opción silenciosa `-print-to-default`.
    2. Imprimir usando el visor predeterminado del sistema mediante el comando `/p` de Windows.

    En caso de que ambas opciones fallen, se muestra un mensaje de advertencia con la causa del error.

    Args:
        ruta_pdf (str): Ruta absoluta al archivo PDF que se desea imprimir.
        parent (QWidget, opcional): Ventana padre para mostrar el mensaje de advertencia en caso de error.

    Returns:
        None
    """
    try:
        # Verificar si el archivo existe
        if not os.path.isfile(ruta_pdf):
            raise FileNotFoundError("Archivo PDF no encontrado")

        # Opción 1: SumatraPDF (más seguro y silencioso)
        sumatra_path = shutil.which("SumatraPDF.exe")
        if sumatra_path:
            subprocess.run([
                sumatra_path,
                "-print-to-default",
                ruta_pdf
            ])
            return

        # Opción 2: visor predeterminado con /p
        subprocess.run(
            ['cmd', '/c', f'start "" /min "{ruta_pdf}" /p'], shell=True)

    except Exception as e:
        print(f"❌ Error al imprimir: {e}")
        QMessageBox.warning(
            parent,
            "Error al imprimir",
            f"No se pudo enviar el contrato a la impresora:\n{str(e)}\n\n"
            "Verifica que tienes instalado un visor PDF como Adobe, Foxit o SumatraPDF."
        )
