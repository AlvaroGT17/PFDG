from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta
from utilidades.boton_animado import BotonAnimado


class VentanaInicio(QWidget):
    def __init__(self, nombre, rol):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Panel Principal")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(700, 500)

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
            ("Reparaciones", "reparacion.png"),
            ("Clientes", "clientes.png"),
            ("Vehículos", "vehiculos.png"),
            ("Facturación", "facturacion.png"),
            ("Reportes", "reportes.png"),
            ("Usuarios", "usuarios.png"),
            ("Cerrar sesión", "salir.png"),
        ]

        accesos_por_rol = {
            "ADMINISTRADOR": ["fichar", "historial", "reparaciones", "clientes", "vehículos", "facturación", "reportes", "usuarios", "cerrar sesión"],
            "MECANICO": ["fichar", "historial", "reparaciones", "vehículos", "cerrar sesión"],
            "COMPRA/VENTA": ["fichar", "historial", "reportes", "cerrar sesión"],
            "ADMINISTRATIVO": ["fichar", "historial", "clientes", "facturación", "cerrar sesión"]
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

        layout_contenedor.addLayout(self.grid_layout)
        layout_principal.addWidget(contenedor, alignment=Qt.AlignCenter)
