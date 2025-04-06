from PySide6.QtCore import QObject, Signal
from vistas.ventana_inicio import VentanaInicio
from controladores.fichar_controlador import FicharControlador
from controladores.historial_controlador import HistorialControlador
from controladores.usuarios_controlador import UsuariosControlador
from controladores.clientes_controlador import ClientesControlador
from controladores.vehiculos_controlador import VehiculosControlador
from controladores.recepcionamiento_controlador import RecepcionamientoControlador
from vistas.ventana_recepcionamiento import VentanaRecepcionamiento


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

        if "historial" in self.ventana.botones:
            self.ventana.botones["historial"].clicked.connect(
                self.abrir_historial)

        if self.rol.upper() == "ADMINISTRADOR":
            self.ventana.botones["crear usuarios"].clicked.connect(
                self.abrir_gestion_usuarios)

        if self.rol.upper() in ["ADMINISTRADOR", "ADMINISTRATIVO"]:
            if "clientes" in self.ventana.botones:
                self.ventana.botones["clientes"].clicked.connect(
                    self.abrir_clientes)

        if self.rol.upper() in ["ADMINISTRADOR", "ADMINISTRATIVO", "COMPRA/VENTA", "MECANICO"]:
            if "vehículos" in self.ventana.botones:
                self.ventana.botones["vehículos"].clicked.connect(
                    self.abrir_vehiculos)

        if "recepcionamiento" in self.ventana.botones:
            self.ventana.botones["recepcionamiento"].clicked.connect(
                self.abrir_recepcionamiento)

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.forzar_cierre = True  # <-- permite cierre
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

    def abrir_historial(self):
        self.controlador_historial = HistorialControlador(
            usuario_id=self.usuario_id,
            es_admin=(self.rol.upper() == "ADMINISTRADOR")
        )
        self.controlador_historial.mostrar()

    def abrir_gestion_usuarios(self):
        self.ventana.hide()
        self.usuarios_controlador = UsuariosControlador(self.ventana)

    def abrir_clientes(self):
        self.ventana.hide()
        self.clientes_controlador = ClientesControlador(self.ventana)

    def abrir_vehiculos(self):
        self.ventana.hide()
        self.vehiculos_controlador = VehiculosControlador(self.ventana)

    def abrir_recepcionamiento(self):
        self.recepcionamiento = VentanaRecepcionamiento()
        self.controlador_recepcionamiento = RecepcionamientoControlador(
            self.recepcionamiento)
        self.recepcionamiento.exec()
