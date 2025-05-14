from PySide6.QtWidgets import QLabel, QTextEdit, QTextBrowser
from pruebas.contrato_test import iniciar_ventana_contrato


def test_contrato_ventana_visible(qtbot):
    ventana = iniciar_ventana_contrato()
    qtbot.addWidget(ventana)
    ventana.show()

    assert ventana.isVisible()


def test_contrato_titulo_o_contenido_visible(qtbot):
    ventana = iniciar_ventana_contrato()
    qtbot.addWidget(ventana)
    ventana.show()

    visor = ventana.findChild(QTextBrowser)
    assert visor is not None
    assert "Contrato" in visor.toPlainText()
