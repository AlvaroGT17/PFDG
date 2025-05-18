"""
Módulo de pruebas unitarias para `ClientesControlador`.

Este archivo verifica las funcionalidades principales del controlador de clientes:
- Registro de cliente con validaciones (nombre, DNI, email).
- Modificación de datos de clientes existentes.
- Eliminación de clientes con confirmación.
- Respuesta a eventos de búsqueda por nombre (autocompletado con Enter).

Se utilizan mocks para simular el comportamiento de funciones externas (como
las consultas a base de datos o validaciones de DNI) y centrarse exclusivamente
en la lógica del controlador.

"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from controladores.clientes_controlador import ClientesControlador


@pytest.fixture
def controlador(qtbot):
    """
    Fixture que crea y destruye una instancia de ClientesControlador correctamente.
    """
    ventana_anterior = MagicMock()
    controlador = ClientesControlador(ventana_anterior)
    qtbot.addWidget(controlador.ventana)
    controlador.ventana.show()
    yield controlador
    controlador.ventana.close()
    controlador.ventana.deleteLater()


def test_registro_falla_sin_nombre_dni(qtbot, controlador):
    """
    Verifica que el registro falla si los campos obligatorios están vacíos.
    """
    controlador.ventana.input_nombre.setText("")
    controlador.ventana.input_apellido1.setText("")
    controlador.ventana.input_dni.setText("")

    with patch.object(controlador, "mostrar_error") as mock_error:
        controlador.registrar_cliente()
        mock_error.assert_called_once_with(
            "Nombre, primer apellido y DNI son obligatorios."
        )


def test_registro_falla_dni_invalido(qtbot, controlador):
    """
    Verifica que el registro falla si el DNI no es válido.
    """
    controlador.ventana.input_nombre.setText("Nombre")
    controlador.ventana.input_apellido1.setText("Apellido")
    controlador.ventana.input_dni.setText("12345678A")

    with patch("controladores.clientes_controlador.DNIUtils.validar_dni", return_value=False), \
            patch.object(controlador, "mostrar_error") as mock_error:
        controlador.registrar_cliente()
        mock_error.assert_called_once_with("El DNI introducido no es válido.")


def test_registro_falla_email_invalido(qtbot, controlador):
    """
    Verifica que el registro falla si el correo electrónico no tiene un formato válido.
    """
    controlador.ventana.input_nombre.setText("Juan")
    controlador.ventana.input_apellido1.setText("Perez")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_email.setText("email_mal_formado")

    with patch("controladores.clientes_controlador.DNIUtils.validar_dni", return_value=True), \
            patch("controladores.clientes_controlador.dni_ya_existe", return_value=False), \
            patch.object(controlador, "mostrar_error") as mock_error:
        controlador.registrar_cliente()
        mock_error.assert_called_once_with(
            "El correo electrónico no tiene un formato válido.")


def test_registro_falla_dni_duplicado(qtbot, controlador):
    """
    Verifica que el registro falla si el DNI ya está registrado en la base de datos.
    """
    controlador.ventana.input_nombre.setText("Ana")
    controlador.ventana.input_apellido1.setText("Lopez")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_email.setText("ana@example.com")

    with patch("controladores.clientes_controlador.DNIUtils.validar_dni", return_value=True), \
            patch("controladores.clientes_controlador.dni_ya_existe", return_value=True), \
            patch.object(controlador, "mostrar_error") as mock_error:
        controlador.registrar_cliente()
        mock_error.assert_called_once_with("Ya existe un cliente con ese DNI.")


def test_registro_exitoso(qtbot, controlador):
    """
    Verifica que el registro se completa correctamente si todos los datos son válidos.
    """
    controlador.ventana.input_nombre.setText("Luis")
    controlador.ventana.input_apellido1.setText("Gomez")
    controlador.ventana.input_dni.setText("11111111H")
    controlador.ventana.input_email.setText("luis@example.com")

    with patch("controladores.clientes_controlador.DNIUtils.validar_dni", return_value=True), \
            patch("controladores.clientes_controlador.dni_ya_existe", return_value=False), \
            patch("controladores.clientes_controlador.crear_cliente", return_value=True), \
            patch.object(controlador, "mostrar_info") as mock_info, \
            patch.object(controlador, "limpiar_campos") as mock_limpiar:
        controlador.registrar_cliente()
        mock_info.assert_called_once_with("Cliente registrado correctamente.")
        mock_limpiar.assert_called_once()


def test_modificar_cliente_sin_seleccionar(qtbot, controlador):
    """
    Verifica que no se puede modificar un cliente si no se ha seleccionado previamente.
    """
    controlador.cliente_seleccionado_id = None
    with patch.object(controlador, "mostrar_error") as mock_error:
        controlador.modificar_cliente()
        mock_error.assert_called_once_with(
            "Primero debes buscar y seleccionar un cliente."
        )


def test_modificar_cliente_email_invalido(qtbot, controlador):
    """
    Verifica que la modificación falla si el email del cliente no es válido.
    """
    controlador.cliente_seleccionado_id = 1
    controlador.lista_clientes = [{"id": 1, "dni": "12345678Z"}]

    controlador.ventana.input_email.setText("email_mal")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_nombre.setText("Juan")
    controlador.ventana.input_apellido1.setText("Pérez")

    with patch.object(controlador, "mostrar_error") as mock_error:
        controlador.modificar_cliente()
        mock_error.assert_called_once_with(
            "El correo electrónico no tiene un formato válido.")


def test_modificar_cliente_exitoso(qtbot, controlador):
    """
    Verifica que la modificación de un cliente se realiza correctamente si todos los datos son válidos.
    """
    controlador.cliente_seleccionado_id = 1
    controlador.lista_clientes = [{"id": 1, "dni": "12345678Z"}]

    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_nombre.setText("Pedro")
    controlador.ventana.input_apellido1.setText("Martinez")
    controlador.ventana.input_email.setText("pedro@example.com")

    with patch("controladores.clientes_controlador.actualizar_cliente", return_value=True), \
            patch.object(controlador, "mostrar_info") as mock_info, \
            patch.object(controlador, "limpiar_campos") as mock_limpiar:
        controlador.modificar_cliente()
        mock_info.assert_called_once_with("Cliente modificado correctamente.")
        mock_limpiar.assert_called_once()


def test_eliminar_cliente_sin_seleccionar(qtbot, controlador):
    """
    Verifica que no se puede eliminar un cliente si no se ha seleccionado previamente.
    """
    controlador.cliente_seleccionado_id = None
    with patch.object(controlador, "mostrar_error") as mock_error:
        controlador.eliminar_cliente()
        mock_error.assert_called_once_with(
            "Primero debes seleccionar un cliente para eliminar.")


def test_eliminar_cliente_cancelado(qtbot, controlador):
    """
    Verifica que al cancelar el cuadro de confirmación, no se elimina el cliente.
    """
    controlador.cliente_seleccionado_id = 1
    with patch("controladores.clientes_controlador.QMessageBox.question", return_value=QMessageBox.No), \
            patch("modelos.clientes_consultas.eliminar_cliente_por_id") as mock_eliminar:
        controlador.eliminar_cliente()
        mock_eliminar.assert_not_called()


def test_eliminar_cliente_exitoso(qtbot, controlador):
    """
    Verifica que un cliente se elimina correctamente tras confirmar la acción.
    """
    controlador.cliente_seleccionado_id = 1
    controlador.lista_clientes = [{"id": 1, "dni": "12345678Z"}]

    with patch("controladores.clientes_controlador.QMessageBox.question", return_value=QMessageBox.Yes), \
            patch("modelos.clientes_consultas.eliminar_cliente_por_id", return_value=True), \
            patch.object(controlador, "mostrar_info") as mock_info, \
            patch.object(controlador, "limpiar_campos") as mock_limpiar, \
            patch("controladores.clientes_controlador.obtener_todos_los_clientes", return_value=[]):
        controlador.eliminar_cliente()
        mock_info.assert_called_once_with("Cliente eliminado correctamente.")
        mock_limpiar.assert_called_once()


def test_event_filter_nombre_detecta_cliente(qtbot, controlador):
    """
    Simula que se pulsa Enter sobre el campo de búsqueda por nombre, y verifica que se rellenan los campos del cliente.
    """
    mock_cliente = {
        "id": 1, "nombre": "Ana", "primer_apellido": "Pérez",
        "segundo_apellido": "", "dni": "11111111A"
    }
    controlador.dict_nombres = {"Ana Pérez": mock_cliente}
    controlador.ventana.input_buscar_nombre.setText("Ana Pérez")

    class MockEvent:
        def type(self): return 6  # QEvent.KeyPress
        def key(self): return Qt.Key_Return

    with patch.object(controlador, "rellenar_campos") as mock_rellenar:
        handled = controlador.eventFilter(
            controlador.ventana.input_buscar_nombre, MockEvent())
        assert handled is True
        mock_rellenar.assert_called_once_with(mock_cliente)
