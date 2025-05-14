from PySide6.QtWidgets import QToolButton, QTableWidget
from pruebas.reimpresionPresupuestos_test import iniciar_ventana_reimpresion_presupuestos


def test_reimpresion_presupuestos_componentes(qtbot):
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)
    ventana.show()

    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    botones = ventana.findChildren(QToolButton)
    textos = [btn.text().lower() for btn in botones]

    assert any("volver" in t for t in textos)
    assert any("enviar" in t for t in textos)
    assert any("imprimir" in t for t in textos)
