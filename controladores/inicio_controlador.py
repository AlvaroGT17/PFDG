from PySide6.QtCore import QObject, Signal
from vistas.ventana_inicio import VentanaInicio
from controladores.fichar_controlador import FicharControlador


class InicioControlador(QObject):
    senal_cerrar_sesion = Signal()

    def __init__(self, nombre, rol):
        super().__init__()
        self.nombre = nombre
        self.rol = rol

        self.usuario_id = self.obtener_id_usuario()  # Se busca por nombre

        self.ventana = VentanaInicio(nombre, rol)

        if "cerrar sesión" in self.ventana.botones:
            self.ventana.botones["cerrar sesión"].clicked.connect(self.cerrar)

        if "fichar" in self.ventana.botones:
            self.ventana.botones["fichar"].clicked.connect(self.abrir_fichaje)

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()
        self.senal_cerrar_sesion.emit()

    def abrir_fichaje(self):
        self.fichaje = FicharControlador({
            "id": self.usuario_id,
            "nombre": self.nombre,
            "rol": self.rol
        })
        self.fichaje.mostrar()

    def obtener_id_usuario(self):
        from modelos.login_consultas import obtener_usuario_por_nombre
        usuario = obtener_usuario_por_nombre(self.nombre)
        return usuario["id"] if usuario else None
