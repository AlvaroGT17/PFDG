"""
Módulo de utilidades para mostrar cuadros de diálogo personalizados con PySide6.

Contiene funciones reutilizables para mostrar mensajes de confirmación y errores
con estilos visuales adaptados a la estética de la aplicación.
"""

from PySide6.QtWidgets import QMessageBox


def mostrar_mensaje_personalizado(vista, titulo, texto, icono=QMessageBox.Question,
                                  botones=QMessageBox.Yes | QMessageBox.No) -> int:
    """
    Muestra un cuadro de diálogo (QMessageBox) personalizado con opciones configurables.

    Se utiliza para confirmar acciones o mostrar mensajes interactivos, con un estilo visual adaptado.

    Args:
        vista: Ventana padre que invoca el cuadro de diálogo.
        titulo (str): Título de la ventana emergente.
        texto (str): Mensaje a mostrar al usuario.
        icono (QMessageBox.Icon, opcional): Icono del mensaje (por defecto: Question).
        botones (QMessageBox.StandardButtons, opcional): Botones a mostrar (por defecto: Yes y No).

    Returns:
        int: Código del botón pulsado por el usuario (por ejemplo: QMessageBox.Yes).
    """
    box = QMessageBox(vista)
    box.setWindowTitle(titulo)
    box.setText(texto)
    box.setIcon(icono)
    box.setStandardButtons(botones)

    # Aplicar estilos visuales personalizados
    box.setStyleSheet("""
        QMessageBox {
            background-color: #f3f3f3;
            color: #222;
            font-size: 14px;
            border: 1px solid #bbb;
        }
        QLabel {
            color: #222;
        }
        QPushButton {
            background-color: #E30613;
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #b10410;
        }
    """)
    return box.exec()


def mostrar_error(vista, titulo, mensaje):
    """
    Muestra un cuadro de diálogo de error con diseño personalizado.

    Esta función se utiliza para notificar errores críticos al usuario con un mensaje claro y visualmente destacado.

    Args:
        vista: Ventana padre que invoca el cuadro de error.
        titulo (str): Título de la ventana de error.
        mensaje (str): Mensaje de error que se mostrará al usuario.
    """
    msg = QMessageBox(vista)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(titulo)
    msg.setText(f"<p style='color: black;'>{mensaje}</p>")
    msg.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QLabel {
            color: black;
            font-size: 14px;
        }
        QPushButton {
            min-width: 80px;
            padding: 6px;
            background-color: #E30613;
            color: white;
            font-weight: bold;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #ff2f2f;
        }
    """)
    msg.exec()
