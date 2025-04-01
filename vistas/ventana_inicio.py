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

        grid = QGridLayout()
        grid.setSpacing(15)

        botones = [
            ("Fichar", "fichar.png"),
            ("Reparaciones", "reparacion.png"),
            ("Historial", "historial.png"),
            ("Clientes", "clientes.png"),
            ("Vehículos", "vehiculos.png"),
            ("Facturación", "facturacion.png"),
            ("Reportes", "reportes.png"),
            ("Usuarios", "usuarios.png"),
            ("Cerrar sesión", "salir.png"),
        ]

        for i, (texto, icono) in enumerate(botones):
            boton = BotonAnimado(texto, icono)
            boton.setObjectName("boton_menu")
            grid.addWidget(boton, i // 3, i % 3)
            self.botones[texto.lower()] = boton

        layout_contenedor.addLayout(grid)
        layout_principal.addWidget(contenedor, alignment=Qt.AlignCenter)
