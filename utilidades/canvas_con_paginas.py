"""
Módulo para añadir numeración de páginas a documentos PDF generados con ReportLab.

Incluye una clase `NumeroPaginasCanvas` que extiende `reportlab.pdfgen.canvas.Canvas`
para permitir mostrar la numeración total de páginas y un pie de página personalizado
al estilo de la aplicación ReyBoxes.
"""

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class NumeroPaginasCanvas(canvas.Canvas):
    """
    Canvas personalizado que añade numeración de páginas y un pie de página con estilo ReyBoxes.

    Esta clase guarda el estado de cada página antes de finalizarla con `showPage()`,
    y en `save()` vuelve a procesar todas para añadir el número de página sobre el documento.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicializa el canvas extendido y prepara el almacenamiento de los estados de página.
        """
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        """
        Guarda el estado de la página actual antes de iniciar una nueva.

        Esto permite reescribir el contenido después con la numeración total.
        """
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """
        Finaliza el documento PDF, reescribiendo cada página para incluir la numeración total.

        Se invoca al final del proceso de escritura del PDF.
        """
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(total_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, total_pages):
        """
        Dibuja el número de página y una línea inferior con pie de página personalizado.

        Args:
            total_pages (int): Número total de páginas del documento.
        """
        self.saveState()
        self.setStrokeColor(colors.red)
        self.setLineWidth(1)
        self.line(30, 50, A4[0] - 30, 50)  # Línea horizontal al pie

        self.setFont("Helvetica", 9)
        self.drawString(30, 35, "ReyBoxes - Sistema de Gestión de Taller")
        self.drawRightString(
            A4[0] - 30, 35, f"Página {self._pageNumber} de {total_pages}")
        self.restoreState()
