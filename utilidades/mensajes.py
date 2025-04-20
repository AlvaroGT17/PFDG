from PySide6.QtWidgets import QMessageBox


def mostrar_mensaje_personalizado(vista, titulo, texto, icono=QMessageBox.Question,
                                  botones=QMessageBox.Yes | QMessageBox.No) -> int:
    """
    Muestra un QMessageBox con estilo personalizado.

    Args:
        vista: ventana padre.
        titulo: título del cuadro de diálogo.
        texto: cuerpo del mensaje.
        icono: tipo de icono (Question, Warning, Information, etc.).
        botones: botones a mostrar (Yes/No, Ok/Cancel, etc.).

    Returns:
        int: botón pulsado (por ejemplo QMessageBox.Yes).
    """
    box = QMessageBox(vista)
    box.setWindowTitle(titulo)
    box.setText(texto)
    box.setIcon(icono)
    box.setStandardButtons(botones)

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
