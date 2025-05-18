"""
Controlador del módulo de fichaje de empleados.

Este módulo permite al usuario registrar un fichaje de entrada o salida,
a través de una interfaz visual simple.

Incluye validaciones básicas para asegurar que se seleccione un tipo de fichaje.

Utiliza:
- `VentanaFichar`: interfaz de usuario con selección de tipo y botones.
- `registrar_fichaje`: función del modelo que guarda el registro en la base de datos.
"""

from PySide6.QtCore import QObject
from vistas.ventana_fichar import VentanaFichar
from modelos.fichajes_consultas import registrar_fichaje


class FicharControlador(QObject):
    """
    Controlador responsable de gestionar la lógica de la ventana de fichaje.

    Permite al usuario registrar un fichaje (Entrada o Salida) y notifica al finalizar.
    """

    def __init__(self, usuario):
        """
        Inicializa el controlador con los datos del usuario activo.

        Args:
            usuario (dict): Diccionario con la información del usuario (incluye al menos 'id').
        """
        super().__init__()
        self.usuario = usuario
        self.ventana = VentanaFichar()

        self.ventana.btn_confirmar.clicked.connect(self.fichar)

    def mostrar(self):
        """
        Muestra la ventana de fichaje.
        """
        self.ventana.show()

    def fichar(self):
        """
        Ejecuta el fichaje tras validar el tipo seleccionado (Entrada o Salida).

        - Muestra error si no se ha seleccionado ninguna opción.
        - Registra el fichaje en la base de datos.
        - Muestra confirmación y cierra la ventana.
        """
        tipo = self.ventana.obtener_tipo_fichaje()
        if not tipo:
            self.ventana.mostrar_error(
                "Debes seleccionar 'Entrada' o 'Salida'")
            return

        registrar_fichaje(self.usuario["id"], tipo)
        self.ventana.mostrar_confirmacion(
            f"Fichaje de {tipo} registrado correctamente.")
        self.ventana.close()
