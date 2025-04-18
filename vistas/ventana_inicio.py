from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta
from utilidades.boton_animado import BotonAnimado
from vistas.ventana_recepcionamiento import VentanaRecepcionamiento
from controladores.recepcionamiento_controlador import RecepcionamientoControlador


class VentanaInicio(QWidget):
    def __init__(self, nombre, rol):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Panel Principal")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(900, 720)  # ⬅️ Ventana más ancha para margen lateral

        self.setObjectName("ventana_inicio")
        ruta_css = obtener_ruta_absoluta("css/inicio.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.nombre = nombre.upper()
        self.rol = rol
        self.botones = {}

        self.inicializar_ui()

    def inicializar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)

        contenedor = QWidget()
        contenedor.setObjectName("contenedor")
        # ⬅️ Más ancho para que haya margen blanco a la derecha
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

        botones_definidos = [
            ("Fichar", "fichar.png"),
            ("Historial", "historial.png"),
            ("Crear usuarios", "crear.png"),
            ("Clientes", "clientes.png"),
            ("Vehículos", "vehiculos.png"),
            ("Recepcionamiento", "recepcionamiento.png"),
            ("Compraventa", "compraventa.png"),
            ("Reparaciones", "reparacion.png"),
            ("Facturación", "facturacion.png"),
            ("Reportes", "reportes.png"),
            ("Usuarios", "usuarios.png"),
            ("Cerrar sesión", "salir.png"),
        ]

        accesos_por_rol = {
            "ADMINISTRADOR": ["fichar", "historial", "crear usuarios", "clientes", "vehículos", "recepcionamiento", "compraventa", "reparaciones", "facturación", "reportes", "usuarios", "cerrar sesión"],
            "MECANICO": ["fichar", "historial", "vehículos", "recepcionamiento", "reparaciones", "cerrar sesión"],
            "COMPRA/VENTA": ["fichar", "historial", "vehículos", "recepcionamiento", "compraventa", "reportes", "cerrar sesión"],
            "ADMINISTRATIVO": ["fichar", "historial", "clientes", "vehículos", "recepcionamiento", "facturación", "cerrar sesión"]
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
        # ⬅️ Perfecto para 3 columnas sin scroll horizontal
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
        # Solo ignorar si NO es cierre programático (por código)
        if not getattr(self, "forzar_cierre", False):
            event.ignore()
        else:
            event.accept()
