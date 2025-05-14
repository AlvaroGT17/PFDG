from PySide6.QtWidgets import QLineEdit
from pruebas.crear_cliente_rapido_test import iniciar_ventana_crear_cliente_rapido


def test_campos_crear_cliente_rapido(qtbot):
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    # Buscar campos de entrada
    campos = ventana.findChildren(QLineEdit)
    textos = [c.placeholderText().lower() for c in campos]

    assert any("nombre" in t for t in textos)
    assert any("dni" in t for t in textos)
    assert any("teléfono" in t or "telefono" in t for t in textos)


def test_crear_cliente_rapido_interaccion(qtbot):
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    # Rellenar campos
    campos = ventana.findChildren(QLineEdit)
    for campo in campos:
        if "nombre" in campo.placeholderText().lower():
            campo.setText("PRUEBA NOMBRE")
        elif "dni" in campo.placeholderText().lower():
            campo.setText("12345678Z")
        elif "teléfono" in campo.placeholderText().lower() or "telefono" in campo.placeholderText().lower():
            campo.setText("612345678")

    # Aquí podrías simular pulsar aceptar si hay un botón, o confirmar mediante método
    assert any(c.text() for c in campos), "Algún campo debería tener texto"
