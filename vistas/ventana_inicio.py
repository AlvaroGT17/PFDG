"""
Módulo para la ventana principal del sistema ReyBoxes (Dashboard).

La ventana sirve como punto de inicio tras el login, mostrando un saludo personalizado
y una cuadrícula de botones animados para acceder a distintas funcionalidades,
según el rol del usuario (Administrador, Mecánico, etc.).

Incluye soporte para scroll si hay demasiados accesos visibles.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from utilidades.boton_animado import BotonAnimado
from utilidades.rutas import obtener_ruta_absoluta


class VentanaInicio(QWidget):
    """
    Ventana principal del sistema ReyBoxes que funciona como panel de navegación.

    Muestra una cuadrícula de botones animados que otorgan acceso a las diferentes
    funcionalidades del sistema dependiendo del rol del usuario (administrador, mecánico, etc).

    Incluye un saludo personalizado y un panel con scroll si hay demasiadas opciones.

    Atributos:
        nombre (str): Nombre del usuario conectado (en mayúsculas).
        rol (str): Rol del usuario (ADMINISTRADOR, MECANICO, etc.).
        botones (dict): Diccionario que almacena los botones visibles por texto en minúscula.
    """

    def __init__(self, nombre, rol):
        """
        Inicializa la ventana de inicio, cargando estilos, nombre del usuario y su rol.

        Args:
            nombre (str): Nombre del usuario conectado.
            rol (str): Rol asignado al usuario (determina los botones visibles).
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Panel Principal")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(900, 720)
        self.setObjectName("ventana_inicio")

        ruta_css = obtener_ruta_absoluta("css/inicio.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.nombre = nombre.upper()
        self.rol = rol
        self.botones = {}

        self.inicializar_ui()

    def inicializar_ui(self):
        """
        Crea la estructura visual de la ventana:
        - Muestra un saludo con el nombre del usuario.
        - Indica el rol actual del usuario.
        - Carga botones permitidos según el rol y los organiza en una cuadrícula.
        - Añade scroll vertical si hay más de 3 filas de botones.
        """
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)

        contenedor = QWidget()
        contenedor.setObjectName("contenedor")
        contenedor.setFixedWidth(840)
        layout_contenedor = QVBoxLayout(contenedor)

        saludo = QLabel(
            f"<b><i>Bienvenido, <span style='color:#d90429;'>{self.nombre}</span></i></b>")
        saludo.setObjectName("titulo_bienvenida")
        saludo.setAlignment(Qt.AlignCenter)

        rol_label = QLabel(f"Rol: <b>{self.rol}</b>")
        rol_label.setObjectName("texto_rol")
        rol_label.setAlignment(Qt.AlignCenter)

        layout_contenedor.addWidget(saludo)
        layout_contenedor.addWidget(rol_label)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)

        # Lista de botones definidos con texto e icono
        botones_definidos = [
            ("Fichar", "fichar.png"),
            ("Historial\nfichaje", "historial.png"),
            ("Crear usuarios", "crear.png"),
            ("Clientes", "clientes.png"),
            ("Vehículos", "vehiculos.png"),
            ("Recepcionamiento", "recepcionamiento.png"),
            ("Compraventa", "compraventa.png"),
            ("Presupuestos", "presupuesto.png"),
            ("Reimpresion\nrecepcionamientos", "reimprimir_recepcionamiento.png"),
            ("Reimpresion\npresupuestos", "reimprimir_presupuestos.png"),
            ("Reimpresion\ncompras", "reimprimir_compra.png"),
            ("Reimpresion\nventas", "reimprimir_venta.png"),
            ("Cerrar sesión", "salir.png"),
        ]

        # Accesos permitidos por rol (debes completar estos arrays según tu lógica)
        accesos_por_rol = {
            "ADMINISTRADOR": [...],
            "MECANICO": [...],
            "COMPRA/VENTA": [...],
            "ADMINISTRATIVO": [...],
        }

        rol_normalizado = self.rol.upper().strip()
        botones_visibles = accesos_por_rol.get(rol_normalizado, [])

        fila = columna = 0
        for texto, icono in botones_definidos:
            if texto.lower() in [b.lower() for b in botones_visibles]:
                boton = BotonAnimado(texto, icono)
                boton.setObjectName("boton_menu")
                self.grid_layout.addWidget(boton, fila, columna)
                self.botones[texto.lower()] = boton

                columna += 1
                if columna == 3:
                    columna = 0
                    fila += 1

        contenedor_grid = QWidget()
        contenedor_grid.setObjectName("grid_fondo")
        contenedor_grid.setLayout(self.grid_layout)
        contenedor_grid.setFixedWidth(780)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(contenedor_grid)
        scroll.setObjectName("scroll_botones")
        scroll.setFixedHeight(400)

        layout_contenedor.addWidget(scroll)
        layout_principal.addWidget(contenedor, alignment=Qt.AlignCenter)

    def closeEvent(self, event):
        """
        Controla el cierre de la ventana. Solo se permite cerrar si la variable "forzar_cierre" está activada.

        Si no está activada, el intento de cierre se ignora.

        Args:
            event (QCloseEvent): Evento de cierre de la ventana.
        """
        if not getattr(self, "forzar_cierre", False):
            event.ignore()
        else:
            event.accept()
