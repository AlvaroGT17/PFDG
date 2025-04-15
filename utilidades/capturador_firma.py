from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent, QPixmap
from PySide6.QtCore import Qt, QPoint


class CapturadorFirma(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setMinimumSize(400, 100)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setAutoFillBackground(True)  # IMPORTANTE
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)

        self.puntos = []
        self.firmando = False
        self.activa = False

    def activar_firma(self, activa: bool):
        self.activa = activa
        self.setCursor(Qt.CrossCursor if activa else Qt.ArrowCursor)

    def limpiar(self):
        self.puntos.clear()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.activa and event.button() == Qt.LeftButton:
            self.firmando = True
            self.puntos.append([event.position().toPoint()])
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.activa and self.firmando:
            self.puntos[-1].append(event.position().toPoint())
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.firmando:
            self.firmando = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # FORZAR fondo blanco siempre

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for linea in self.puntos:
            if len(linea) >= 2:
                for i in range(len(linea) - 1):
                    painter.drawLine(linea[i], linea[i + 1])

        if not self.puntos:
            painter.setPen(QColor(180, 180, 180))
            painter.drawText(self.rect(), Qt.AlignCenter, "Espacio para firma")

    def obtener_firma(self):
        """Devuelve un QPixmap con la firma actual."""
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        self.render(painter, QPoint(0, 0))
        painter.end()
        return pixmap
