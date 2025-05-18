"""
Controlador principal de la pantalla de inicio tras el login del sistema.

Este módulo gestiona:
- Navegación a módulos según el rol del usuario.
- Conexión de eventos con las distintas ventanas (clientes, vehículos, fichaje, etc.).
- Acceso a módulos de impresión y reimpresión (presupuestos, compras, ventas, recepcionamientos).
- Control de cierre de sesión mediante señal.

Utiliza:
- Ventanas de `vistas.*` y controladores asociados para cada funcionalidad del taller.
- Funciones de carga dinámica y control de flujo de la aplicación.
"""
from PySide6.QtCore import QObject, Signal, QTimer, Qt
from vistas.ventana_inicio import VentanaInicio
from vistas.ventana_presupuesto import VentanaPresupuesto
from controladores.fichar_controlador import FicharControlador
from controladores.historial_controlador import HistorialControlador
from controladores.usuarios_controlador import UsuariosControlador
from controladores.clientes_controlador import ClientesControlador
from controladores.vehiculos_controlador import VehiculosControlador
from controladores.recepcionamiento_controlador import RecepcionamientoControlador
from vistas.ventana_recepcionamiento import VentanaRecepcionamiento
from vistas.ventana_carga_gif import VentanaCargaGif
from utilidades.abridor_con_carga import AbridorConCarga
from utilidades.hilos.hilo_carga_recepcionamiento import HiloCargaRecepcionamiento
from vistas.ventana_compraventa import VentanaCompraventa
from modelos.recepcionamiento_consultas import (
    obtener_motivos,
    obtener_urgencias,
    obtener_categorias_vehiculo,
    obtener_tipos_vehiculo,
    obtener_combustibles
)

from controladores.reimpresionPresupuestos_controlador import ReimpresionPresupuestosControlador
from controladores.reimpresionRecepcionamiento_controlador import ReimpresionRecepcionamientoControlador
from controladores.reimpresionCompras_controlador import ReimpresionComprasControlador
from controladores.reimpresionVentas_controlador import ReimpresionVentasControlador


class InicioControlador(QObject):
    """
    Controlador que gestiona la pantalla de inicio y la navegación por módulos del sistema.

    Señales:
        senal_cerrar_sesion: se emite cuando el usuario cierra sesión voluntariamente.
    """
    senal_cerrar_sesion = Signal()

    def __init__(self, nombre, rol):
        """
        Inicializa el controlador principal tras el login.

        Args:
            nombre (str): Nombre de usuario.
            rol (str): Rol asignado al usuario (ADMINISTRADOR, MECANICO, etc.).
        """
        super().__init__()
        self.nombre = nombre
        self.rol = rol

        self.usuario_id = self.obtener_id_usuario()  # Se busca por nombre
        self.ventana = VentanaInicio(nombre, rol)

        if "cerrar sesión" in self.ventana.botones:
            self.ventana.botones["cerrar sesión"].clicked.connect(self.cerrar)

        if "fichar" in self.ventana.botones:
            self.ventana.botones["fichar"].clicked.connect(self.abrir_fichaje)

        if "historial\nfichaje" in self.ventana.botones:
            self.ventana.botones["historial\nfichaje"].clicked.connect(
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

        if self.rol.upper() in ["ADMINISTRADOR", "ADMINISTRATIVO", "MECANICO"]:
            if "presupuestos" in self.ventana.botones:
                self.ventana.botones["presupuestos"].clicked.connect(
                    self.abrir_presupuestos)

        if self.rol.upper() in ["ADMINISTRADOR", "COMPRA/VENTA"]:
            if "compraventa" in self.ventana.botones:
                self.ventana.botones["compraventa"].clicked.connect(
                    self.abrir_compraventa)

        if self.rol.upper() in ["ADMINISTRADOR", "ADMINISTRATIVO"]:
            mapping_reimp = {
                "reimpresion\nrecepcionamientos": self.abrir_reimpresion_recepcionamientos,
                "reimpresion\npresupuestos":      self.abrir_reimpresion_presupuestos,
                "reimpresion\ncompras":           self.abrir_reimpresion_compras,
                "reimpresion\nventas":            self.abrir_reimpresion_ventas,
            }
            for clave, slot in mapping_reimp.items():
                if clave in self.ventana.botones:
                    self.ventana.botones[clave].clicked.connect(slot)

    def mostrar(self):
        """Muestra la ventana de inicio."""
        self.ventana.show()

    def cerrar(self):
        """
        Cierra la sesión actual y emite la señal correspondiente.
        """
        self.ventana.forzar_cierre = True
        self.ventana.close()
        self.senal_cerrar_sesion.emit()

    def abrir_fichaje(self):
        """Abre la ventana de fichaje de entrada o salida."""
        self.fichaje = FicharControlador({
            "id": self.usuario_id,
            "nombre": self.nombre,
            "rol": self.rol
        })
        self.fichaje.mostrar()

    def obtener_id_usuario(self):
        """
        Obtiene el ID del usuario a partir de su nombre.

        Returns:
            int | None: ID si existe el usuario, None si no se encuentra.
        """
        from modelos.login_consultas import obtener_usuario_por_nombre
        usuario = obtener_usuario_por_nombre(self.nombre)
        return usuario["id"] if usuario else None

    def abrir_historial(self):
        """Abre la ventana del historial de fichajes del usuario o de todos (si es administrador)."""
        self.controlador_historial = HistorialControlador(
            usuario_id=self.usuario_id,
            es_admin=(self.rol.upper() == "ADMINISTRADOR")
        )
        self.controlador_historial.mostrar()

    def abrir_gestion_usuarios(self):
        """Abre la gestión de usuarios si el rol lo permite."""
        self.ventana.hide()
        self.usuarios_controlador = UsuariosControlador(self.ventana)

    def abrir_clientes(self):
        """Abre la ventana de gestión de clientes."""
        self.ventana.hide()
        self.clientes_controlador = ClientesControlador(self.ventana)

    def abrir_vehiculos(self):
        """Abre la ventana de gestión de vehículos."""
        self.ventana.hide()
        self.vehiculos_controlador = VehiculosControlador(self.ventana)

    def abrir_recepcionamiento(self):
        """Abre el módulo de recepción de vehículos mediante carga previa."""
        def cargar_datos():
            return {
                "motivos": obtener_motivos(),
                "urgencias": obtener_urgencias(),
                "categorias": obtener_categorias_vehiculo(),
                "tipos": obtener_tipos_vehiculo(),
                "combustibles": obtener_combustibles(),
                "usuario_id": self.usuario_id
            }

        self.abridor_recepcionamiento = AbridorConCarga(
            ventana_padre=self.ventana,
            clase_ventana=VentanaRecepcionamiento,
            clase_controlador=RecepcionamientoControlador,
            funcion_carga=cargar_datos
        )

    def mostrar_recepcionamiento(self):
        """Muestra la ventana de recepcionamiento directamente, usada internamente."""
        self.recepcionamiento = VentanaRecepcionamiento()
        self.controlador_recepcionamiento = RecepcionamientoControlador(
            self.recepcionamiento)
        self.ventana_carga.cerrar()
        self.recepcionamiento.exec()

    def abrir_compraventa(self):
        """Abre la ventana de gestión de compraventa de vehículos."""
        self.ventana.hide()
        self.controlador_compraventa = VentanaCompraventa(self.ventana)
        self.controlador_compraventa.show()

    def abrir_presupuestos(self):
        """Abre el módulo de presupuestos en modo diálogo y vuelve a inicio al cerrarse."""
        self.ventana.hide()  # Oculta la ventana de inicio

        self.dialogo_presupuesto = VentanaPresupuesto(self.ventana)

        from controladores.presupuesto_controlador import PresupuestoControlador
        PresupuestoControlador(self.dialogo_presupuesto)

        self.dialogo_presupuesto.exec()  # Espera a que se cierre
        self.ventana.show()  # <- Recupera la ventana de inicio al cerrarse

    def _abrir_ventana_reimpresion(self, clase_ventana, lista_documentos=None):
        """
        Abre una ventana de reimpresión de documentos, conectando las señales necesarias.

        Args:
            clase_ventana: Clase de la ventana a abrir.
            lista_documentos: Lista opcional de documentos precargados.
        """
        self.ventana.hide()
        dlg = clase_ventana(lista_documentos, parent=self.ventana)
        dlg.senal_reimprimir.connect(self.reimprimir_documento)
        dlg.senal_reenviar.connect(self.reenviar_documento)
        dlg.exec()
        self.ventana.show()

    def abrir_reimpresion_recepcionamientos(self):
        """Abre el controlador de reimpresión de recepcionamientos."""
        self.ventana.hide()
        self.reimpresion_controlador = ReimpresionRecepcionamientoControlador(
            main_app=self,
            nombre_usuario=self.nombre,
            rol_usuario=self.rol
        )

    def abrir_reimpresion_presupuestos(self):
        """Abre el controlador de reimpresión de presupuestos."""
        self.ventana.hide()
        self.reimpresion_presupuestos = ReimpresionPresupuestosControlador(
            main_app=self,
            nombre_usuario=self.nombre,
            rol_usuario=self.rol
        )

    def abrir_reimpresion_compras(self):
        """Abre el controlador de reimpresión de documentos de compras."""
        self.ventana.hide()
        self.reimpresion_compras = ReimpresionComprasControlador(
            main_app=self,
            nombre_usuario=self.nombre,
            rol_usuario=self.rol
        )

    def abrir_reimpresion_ventas(self):
        """Abre el controlador de reimpresión de documentos de ventas."""
        self.ventana.hide()
        self.reimpresion_ventas = ReimpresionVentasControlador(
            main_app=self,
            nombre_usuario=self.nombre,
            rol_usuario=self.rol
        )

    # Señales que ejecutarás con tu lógica real
    def reimprimir_documento(self, doc_id: str):
        """
        Lógica pendiente para procesar la reimpresión de un documento.

        Args:
            doc_id (str): Identificador único del documento a imprimir.
        """
        # TODO: lógica de impresión (PDF, impresora, etc.)
        print(f"[DEBUG] Solicitud de reimpresión del documento {doc_id}")

    def reenviar_documento(self, doc_id: str):
        """
        Lógica pendiente para reenviar un documento por correo u otros medios.

        Args:
            doc_id (str): Identificador único del documento a reenviar.
        """
        # TODO: lógica de envío por correo / WhatsApp / API
        print(f"[DEBUG] Solicitud de reenvío del documento {doc_id}")

    def mostrar_ventana_inicio(self, nombre, rol):
        """Muestra nuevamente la ventana principal del sistema."""
        self.ventana.show()
