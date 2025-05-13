"""
Módulo de utilidades para la validación y generación de DNIs españoles.

Proporciona métodos estáticos para:
- Validar si un DNI es correcto.
- Generar DNIs válidos aleatorios (útiles para pruebas o datos simulados).
"""

import re
import random


class DNIUtils:
    """
    Clase de utilidades para el manejo de DNIs españoles.

    Contiene métodos estáticos para validar DNIs y generar DNIs válidos aleatorios.
    """

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    @staticmethod
    def validar_dni(dni: str) -> bool:
        """
        Valida si un DNI español es correcto.

        El DNI debe consistir en 8 números seguidos de una letra. 
        Se permiten entradas con espacios o puntos (que serán eliminados antes de la validación).

        Args:
            dni (str): El DNI a validar.

        Returns:
            bool: `True` si el DNI es válido, `False` si no lo es.
        """
        dni = dni.strip().upper().replace(" ", "").replace(".", "")
        if not re.fullmatch(r"\d{8}[A-Z]", dni):
            return False

        numero = int(dni[:-1])
        letra_correcta = DNIUtils.letras[numero % 23]
        return dni[-1] == letra_correcta

    @staticmethod
    def generar_dni() -> str:
        """
        Genera un DNI válido aleatorio.

        Crea un número de 8 cifras y calcula su letra correspondiente.

        Returns:
            str: Un DNI válido en formato string (por ejemplo, '12345678Z').
        """
        numero = random.randint(10000000, 99999999)
        letra = DNIUtils.letras[numero % 23]
        return f"{numero}{letra}"


# Bloque de ejecución directa para pruebas
if __name__ == "__main__":
    print("🧪 Generando 10 DNIs aleatorios válidos:\n")
    for _ in range(10):
        print(DNIUtils.generar_dni())
