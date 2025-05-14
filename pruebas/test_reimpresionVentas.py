from PySide6.QtWidgets import QPushButton, QTableWidget
from pruebas.reimpresionVentas_test import iniciar_ventana_reimpresion_ventas


def test_reimpresion_ventas_componentes(qtbot):
    ventana = iniciar_ventana_reimpresion_ventas()
    qtbot.addWidget(ventana)
    ventana.show()

    # Verificar existencia de tabla y columnas
    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    # Verificar existencia de botones con texto esperado
    botones = ventana.findChildren(QPushButton)
    textos_botones = [b.text().lower() for b in botones]

    assert any("volver" in texto for texto in textos_botones)
    assert any("enviar" in texto for texto in textos_botones)
    assert any("imprimir" in texto for texto in textos_botones)
