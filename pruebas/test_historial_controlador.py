"""
Tests funcionales para el controlador `HistorialControlador`.

Estas pruebas validan:
- La carga de datos de fichajes según el rol del usuario (personal o global).
- La exportación correcta a CSV y PDF utilizando mocks para evitar acceso real a disco o diálogos.

Se utilizan decoradores `@patch` para interceptar llamadas a funciones de sistema o biblioteca.
"""

from datetime import datetime
import pytest
from unittest.mock import patch, MagicMock, mock_open
from controladores.historial_controlador import HistorialControlador


@patch("controladores.historial_controlador.obtener_fichajes_personales", return_value=[(datetime(2025, 5, 1, 8, 0), "ENTRADA")])
@patch("controladores.historial_controlador.obtener_nombre_usuario", return_value="CRESNIK")
def test_carga_datos_usuario(mock_nombre, mock_fichajes, qtbot):
    """
    Verifica que al crear el controlador en modo no administrador,
    se cargan los fichajes personales y se añade el nombre del usuario.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)
    assert mock_fichajes.called
    assert mock_nombre.called
    assert controlador.fichajes[0][2] == "CRESNIK"


@patch("controladores.historial_controlador.obtener_fichajes_globales", return_value=[
    (datetime(2025, 5, 1, 8, 0), "ENTRADA", "ADMIN")
])
def test_carga_datos_admin(mock_fichajes, qtbot):
    """
    Verifica que si el usuario es administrador, se cargan los fichajes globales
    directamente sin necesidad de obtener nombre individual.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=True)
    qtbot.addWidget(controlador.ventana)
    assert mock_fichajes.called
    assert controlador.fichajes[0][2] == "ADMIN"


@patch("controladores.historial_controlador.QFileDialog.getSaveFileName", return_value=("fichajes_test.csv", None))
@patch("controladores.historial_controlador.open", new_callable=mock_open)
@patch("controladores.historial_controlador.QMessageBox.information")
@patch("controladores.historial_controlador.obtener_fichajes_personales", return_value=[(datetime(2025, 5, 1, 8, 0), "ENTRADA")])
@patch("controladores.historial_controlador.obtener_nombre_usuario", return_value="CRESNIK")
def test_exportar_csv(mock_nombre, mock_fichajes, mock_info, mock_openfile, mock_dialog, qtbot):
    """
    Verifica que el método `exportar_csv()`:
    - Llama correctamente al diálogo de guardado.
    - Escribe en el archivo usando `open`.
    - Muestra un mensaje de éxito.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)
    controlador.exportar_csv()
    mock_openfile.assert_called_once()
    mock_info.assert_called_once()


@patch("controladores.historial_controlador.QMessageBox.information")
@patch("controladores.historial_controlador.QFileDialog.getSaveFileName", return_value=("historial_test.pdf", None))
@patch("controladores.historial_controlador.SimpleDocTemplate.build")
@patch("controladores.historial_controlador.obtener_fichajes_personales", return_value=[(datetime(2025, 5, 1, 8, 0), "ENTRADA")])
@patch("controladores.historial_controlador.obtener_nombre_usuario", return_value="CRESNIK")
def test_exportar_pdf(mock_nombre, mock_fichajes, mock_build, mock_dialog, mock_info, qtbot):
    """
    Verifica que el método `exportar_pdf()`:
    - Construye correctamente el documento PDF usando `SimpleDocTemplate`.
    - Muestra un mensaje de confirmación tras generar el informe.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    controlador.exportar_pdf()

    mock_info.assert_called_once_with(
        controlador.ventana, "Exportación PDF", "✅ Informe PDF generado correctamente.")
