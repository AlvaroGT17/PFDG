from pruebas.compraventa_test import iniciar_ventana_compraventa


def test_ventana_compraventa_carga_correcta(qtbot):
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)

    assert ventana.cliente_nombre.text() == "SERGIO CABRERA PEÑA"
    assert ventana.vehiculo_marca.text() == "SEAT"
    assert ventana.vehiculo_precio_compra.text() == "8500"
