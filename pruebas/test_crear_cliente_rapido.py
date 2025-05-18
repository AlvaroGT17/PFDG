"""
Pruebas unitarias para la ventana `VentanaCrearClienteRapido`.

Estas pruebas validan:
- La presencia y correcto etiquetado de los campos de entrada.
- El comportamiento del botón "Crear" en función del estado de los campos obligatorios.
- La simulación de entrada del usuario en un flujo básico de uso.

Todas las interacciones se realizan usando `pytest-qt` para simular el entorno gráfico.

"""

from PySide6.QtWidgets import QLineEdit
from pruebas.crear_cliente_rapido_test import iniciar_ventana_crear_cliente_rapido


def test_campos_crear_cliente_rapido(qtbot):
    """
    Verifica que los campos esenciales ('nombre', 'dni' y 'teléfono')
    estén presentes en la ventana mediante los textos de placeholder.
    """
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    campos = ventana.findChildren(QLineEdit)
    textos = [c.placeholderText().lower() for c in campos]

    assert any("nombre" in t for t in textos)
    assert any("dni" in t for t in textos)
    assert any("teléfono" in t or "telefono" in t for t in textos)


def test_crear_cliente_rapido_interaccion(qtbot):
    """
    Simula la introducción de datos en los campos para verificar
    que el formulario acepta entrada válida en los campos clave.
    """
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    campos = ventana.findChildren(QLineEdit)
    for campo in campos:
        placeholder = campo.placeholderText().lower()
        if "nombre" in placeholder:
            campo.setText("PRUEBA NOMBRE")
        elif "dni" in placeholder:
            campo.setText("12345678Z")
        elif "teléfono" in placeholder or "telefono" in placeholder:
            campo.setText("612345678")

    assert any(c.text() for c in campos), "Algún campo debería tener texto"


def test_boton_crear_desactivado_al_inicio(qtbot):
    """
    Verifica que el botón 'Crear' esté desactivado al iniciar la ventana.
    """
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    assert not ventana.boton_crear.isEnabled()


def test_boton_crear_se_activa_con_campos(qtbot):
    """
    Al completar todos los campos obligatorios, el botón 'Crear' debe activarse.
    """
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.input_nombre.setText("Juan")
    ventana.input_apellido1.setText("Pérez")
    ventana.input_dni.setText("12345678Z")
    ventana.input_telefono.setText("600000000")

    assert ventana.boton_crear.isEnabled()


def test_boton_crear_se_desactiva_si_falta_campo(qtbot):
    """
    Si se borra un campo obligatorio tras haber completado el formulario,
    el botón 'Crear' debe volver a desactivarse.
    """
    ventana = iniciar_ventana_crear_cliente_rapido()
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.input_nombre.setText("Juan")
    ventana.input_apellido1.setText("Pérez")
    ventana.input_dni.setText("12345678Z")
    ventana.input_telefono.setText("600000000")

    assert ventana.boton_crear.isEnabled()

    ventana.input_dni.clear()
    assert not ventana.boton_crear.isEnabled()
