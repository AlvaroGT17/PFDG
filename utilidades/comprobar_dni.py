# utilidades/dni_utils.py

import random
import re


class DNIUtils:
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    @staticmethod
    def validar_dni(dni: str) -> bool:
        """
        Valida un DNI español (8 números + letra)
        Admite formatos con o sin espacios/puntos.
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
        Genera un DNI español válido aleatorio.
        """
        numero = random.randint(10000000, 99999999)
        letra = DNIUtils.letras[numero % 23]
        return f"{numero}{letra}"


# Si se ejecuta directamente, genera DNIs aleatorios
if __name__ == "__main__":
    print("🧪 Generando 10 DNIs aleatorios válidos:\n")
    for _ in range(10):
        print(DNIUtils.generar_dni())
