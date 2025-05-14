from PySide6.QtWidgets import QToolButton, QTableWidget
from pruebas.reimpresionCompras_test import iniciar_ventana_reimpresion_compras


def test_reimpresion_compras_componentes_basicos(qtbot):
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)
    ventana.show()

    # Verifica que se ha cargado una tabla
    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    # Verifica que existen los botones principales
    botones = ventana.findChildren(QToolButton)
    textos = [b.text().lower() for b in botones]

    assert any("volver" in t for t in textos)
    assert any("enviar" in t for t in textos)
    assert any("imprimir" in t for t in textos)
