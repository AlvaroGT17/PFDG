import os
import sys


def obtener_ruta_absoluta(ruta_relativa: str) -> str:
    """
    Devuelve la ruta absoluta del recurso a partir de su ruta relativa
    respecto al directorio base de ejecución. Lanza un error si no existe.
    """
    if getattr(sys, 'frozen', False):
        # Si la aplicación está empaquetada (ej: PyInstaller)
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Normalizamos la ruta relativa (por si tiene \ en Windows)
    ruta_relativa = ruta_relativa.replace('\\', '/')
    ruta_absoluta = os.path.abspath(
        os.path.join(base_path, '..', ruta_relativa))

    if not os.path.exists(ruta_absoluta):
        raise FileNotFoundError(f"El recurso no existe: {ruta_absoluta}")

    return ruta_absoluta


if __name__ == '__main__':
    # Si se pasa argumento por consola, lo usamos. Si no, usamos una por defecto
    ruta_rel = sys.argv[1] if len(sys.argv) > 1 else 'img/logo.jpg'

    try:
        ruta = obtener_ruta_absoluta(ruta_rel)
        print(f"✅ Ruta absoluta:\n{ruta}")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
