"""
Módulo de captura de firma digital con PySide6.

Proporciona un widget `CapturadorFirma` que permite al usuario dibujar una firma con el ratón,
obtenerla como imagen, como bytes PNG o codificada en base64 para incluir en HTML o almacenarla.
"""

import base64
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent, QPixmap


class CapturadorFirma(QWidget):
    """
    Widget interactivo para capturar la firma del usuario.

    Permite al usuario firmar sobre un área con el ratón, limpiar la firma,
    y exportarla en distintos formatos (QPixmap, bytes PNG, base64).
    """

    firma_finalizada = Signal()

    def __init__(self):
        """
        Inicializa el widget con fondo blanco y configuración predeterminada.
        """
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setMinimumSize(400, 100)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)

        # Lista de trazos (cada trazo es una lista de puntos)
        self.puntos = []
        self.firmando = False
        self.activa = False

    def activar_firma(self, activa: bool):
        """
        Activa o desactiva el modo de firma.

        Args:
            activa (bool): Si es True, se permite firmar; si es False, se desactiva.
        """
        self.activa = activa
        self.setCursor(Qt.CrossCursor if activa else Qt.ArrowCursor)

    def limpiar(self):
        """
        Limpia completamente el contenido de la firma.
        """
        self.puntos.clear()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        """
        Captura el inicio de un trazo si la firma está activa.
        """
        if self.activa and event.button() == Qt.LeftButton:
            self.firmando = True
            self.puntos.append([event.position().toPoint()])
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Añade puntos al trazo actual mientras se mantiene el clic izquierdo.
        """
        if self.activa and self.firmando:
            self.puntos[-1].append(event.position().toPoint())
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Finaliza el trazo actual.
        """
        if self.firmando:
            self.firmando = False

    def paintEvent(self, event):
        """
        Dibuja todos los trazos realizados sobre el widget.
        """
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # Forzar fondo blanco

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for linea in self.puntos:
            if len(linea) >= 2:
                for i in range(len(linea) - 1):
                    painter.drawLine(linea[i], linea[i + 1])

        if not self.puntos:
            # Texto indicativo si aún no hay firma
            painter.setPen(QColor(180, 180, 180))
            painter.drawText(self.rect(), Qt.AlignCenter, "Espacio para firma")

    def obtener_firma(self):
        """
        Obtiene la firma como un QPixmap.

        Returns:
            QPixmap: Imagen de la firma actual.
        """
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        self.render(painter, QPoint(0, 0))
        painter.end()
        return pixmap

    def obtener_firma_como_bytes(self):
        """
        Convierte la firma en bytes PNG.

        Returns:
            bytes or None: Imagen PNG de la firma en formato binario, o None si está vacía.
        """
        pixmap = self.obtener_firma()
        if pixmap.isNull():
            return None

        from io import BytesIO
        from PIL import ImageQt, Image

        image = Image.fromqpixmap(pixmap)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    def obtener_imagen_base64(self):
        """
        Devuelve la firma codificada en base64 como cadena, útil para incrustar en HTML.

        Returns:
            str: Firma en formato base64 (o cadena vacía si no hay firma).
        """
        firma_bytes = self.obtener_firma_como_bytes()
        if firma_bytes is None:
            return ""
        return base64.b64encode(firma_bytes).decode("utf-8")

    def keyPressEvent(self, event):
        """
        Captura la pulsación de teclas. Si se pulsa ENTER, se emite la señal firma_finalizada.
        """
        if self.activa and event.key() == Qt.Key_Return:
            self.firma_finalizada.emit()
        else:
            super().keyPressEvent(event)
