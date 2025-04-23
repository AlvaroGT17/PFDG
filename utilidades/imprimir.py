import os
import subprocess
import shutil
from PySide6.QtWidgets import QMessageBox


def imprimir_pdf(ruta_pdf, parent=None):
    """
    Intenta imprimir un archivo PDF usando:
    1. SumatraPDF (si está disponible)
    2. El visor predeterminado del sistema (/p)
    Si todo falla, muestra un mensaje de advertencia.
    """
    try:
        # Verificar si el archivo existe
        if not os.path.isfile(ruta_pdf):
            raise FileNotFoundError("Archivo PDF no encontrado")

        # 🟡 Opción 1: SumatraPDF (más seguro y silencioso)
        sumatra_path = shutil.which("SumatraPDF.exe")
        if sumatra_path:
            subprocess.run([
                sumatra_path,
                "-print-to-default",
                ruta_pdf
            ])
            return

        # 🟡 Opción 2: visor predeterminado con /p
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
