from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtGui import QIcon, QFont, QCursor
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaInicio(QWidget):
    def __init__(self, nombre_usuario, rol_usuario):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Inicio")
        self.setFixedSize(700, 600)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        ruta_css = obtener_ruta_absoluta("css/inicio.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario

        self.inicializar_ui()

    def inicializar_ui(self):
        layout = QVBoxLayout(self)

        # Bienvenida
        saludo = QLabel(
            f"<span>Bienvenido, </span><span style='color:#E30613;'>{self.nombre_usuario}</span>")
        saludo.setAlignment(Qt.AlignCenter)
        saludo.setObjectName("titulo_bienvenida")
        layout.addWidget(saludo)

        # Rol
        rol = QLabel(f"Rol: <b>{self.rol_usuario}</b>")
        rol.setAlignment(Qt.AlignCenter)
        rol.setObjectName("texto_rol")
        layout.addWidget(rol)

        # Rejilla de botones
        grid = QGridLayout()
        grid.setSpacing(20)

        self.botones = {}

        botones_info = [
            ("Fichar", "fichar.png"),
            ("Reparaciones", "reparacion.png"),
            ("Historial", "historial.png"),
            ("Clientes", "clientes.png"),
            ("Vehículos", "vehiculos.png"),
            ("Facturación", "facturacion.png"),
            ("Reportes", "reportes.png"),
            ("Usuarios", "usuarios.png"),
            ("Cerrar sesión", "salir.png")
        ]

        for i, (texto, icono) in enumerate(botones_info):
            btn = QPushButton(texto)
            btn.setIcon(QIcon(obtener_ruta_absoluta(f"img/{icono}")))
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setObjectName("boton_menu")
            self.botones[texto] = btn
            grid.addWidget(btn, i // 3, i % 3)

        layout.addLayout(grid)
