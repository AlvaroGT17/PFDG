from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


class NumeroPaginasCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(total_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, total_pages):
        self.saveState()
        self.setStrokeColor(colors.red)
        self.setLineWidth(1)
        self.line(30, 50, A4[0] - 30, 50)
        self.setFont("Helvetica", 9)
        self.drawString(30, 35, "ReyBoxes - Sistema de Gestión de Taller")
        self.drawRightString(
            A4[0] - 30, 35, f"Página {self._pageNumber} de {total_pages}")
        self.restoreState()
