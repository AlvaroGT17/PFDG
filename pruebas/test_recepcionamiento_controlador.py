"""
Tests unitarios para el controlador de recepcionamiento.

Estos tests comprueban el comportamiento del `RecepcionamientoControlador` 
utilizando mocks para simular la interfaz gráfica y las dependencias externas,
sin necesidad de interacción real con la base de datos ni la interfaz.

Se validan los siguientes aspectos:
- Inicialización del controlador.
- Asignación de ruta predeterminada.
- Filtrado dinámico de tipos por categoría seleccionada.
- Configuración de autocompletado en matrículas.
- Validación de datos antes de confirmar recepcionamiento.
- Generación de PDF y su impresión o envío por correo.
"""

import pytest
from unittest.mock import MagicMock, patch, call
from controladores.recepcionamiento_controlador import RecepcionamientoControlador


@pytest.fixture
def vista_mock():
    """
    Crea un objeto simulado de la vista con valores por defecto 
    para los controles más relevantes usados en los tests.
    """
    vista = MagicMock()
    vista.checkbox_ruta_predeterminada.isChecked.return_value = True
    vista.input_ruta_guardado.text.return_value = "ruta/ficticia"
    vista.combo_categoria.currentText.return_value = "Turismo"
    return vista


@pytest.fixture
def datos_mock():
    """
    Devuelve un diccionario simulado con los datos necesarios 
    para inicializar el controlador (usuario, categorías, tipos, etc.).
    """
    return {
        "usuario_id": 1,
        "categorias": ["Turismo", "Camión"],
        "combustibles": ["Gasolina", "Diésel"],
        "tipos": [
            {"nombre": "SUV", "categoria": "Turismo"},
            {"nombre": "Pickup", "categoria": "Camión"},
        ],
        "motivos": [{"id": 1, "nombre": "Revisión"}],
        "urgencias": [{"id": 2, "descripcion": "Alta"}],
    }


@patch("controladores.recepcionamiento_controlador.obtener_siguiente_numero_recepcionamiento", return_value=42)
def test_controlador_se_inicializa_correctamente(mock_num, vista_mock, datos_mock):
    """
    Verifica que al iniciar el controlador se asigna correctamente 
    el número de recepcionamiento con formato cero-rellenado.
    """
    RecepcionamientoControlador(vista_mock, datos_mock)
    vista_mock.input_numero_recepcion.setText.assert_called_with("00042")


def test_ruta_predeterminada_se_asigna(vista_mock, datos_mock):
    """
    Comprueba que se establece automáticamente la ruta predeterminada 
    al campo de guardado si la casilla está marcada.
    """
    with patch("controladores.recepcionamiento_controlador.obtener_ruta_predeterminada_recepcionamientos", return_value="/ruta/defecto"):
        RecepcionamientoControlador(vista_mock, datos_mock)
        vista_mock.input_ruta_guardado.setText.assert_called_with(
            "/ruta/defecto")


def test_filtrar_tipos_por_categoria(vista_mock, datos_mock):
    """
    Verifica que al filtrar los tipos según la categoría seleccionada, 
    solo se muestran los tipos correspondientes.
    """
    ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
    vista_mock.combo_tipo.clear.reset_mock()
    ctrl._filtrar_tipos_por_categoria()
    vista_mock.combo_tipo.addItems.assert_called_with(["SUV"])


def test_configurar_autocompletado_matricula_asigna_completer(vista_mock, datos_mock):
    """
    Comprueba que se configura correctamente el autocompletado para matrículas existentes.
    """
    with patch("controladores.recepcionamiento_controlador.obtener_matriculas_existentes", return_value=["1234ABC", "5678XYZ"]):
        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        completer = vista_mock.input_matricula.setCompleter.call_args[0][0]
        assert completer.model().stringList() == ["1234ABC", "5678XYZ"]


def test_confirmar_recepcionamiento_muestra_warning_si_sin_ruta(vista_mock, datos_mock):
    """
    Verifica que se muestra una advertencia si se intenta confirmar 
    un recepcionamiento sin haber indicado la ruta de guardado.
    """
    vista_mock.input_ruta_guardado.text.return_value = ""
    vista_mock.input_correo.text.return_value.strip.return_value = ""

    with patch("controladores.recepcionamiento_controlador.QMessageBox.warning") as mock_warn:
        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        ctrl._recopilar_datos = MagicMock(return_value={
            "DNI": "00000000Z",
            "Motivo": "Revisión",
            "Matrícula": "1234ABC",
            "Email": ""
        })
        ctrl.confirmar_recepcionamiento()

        mock_warn.assert_called_once()


def test_confirmar_recepcionamiento_rechaza_correo_invalido(vista_mock, datos_mock):
    """
    Verifica que si el usuario activa el envío por correo pero el email es inválido,
    se lanza una advertencia y no se continúa con el proceso.
    """
    vista_mock.checkbox_enviar_correo.isChecked.return_value = True
    vista_mock.input_correo.text.return_value = "correo#invalido"
    with patch("controladores.recepcionamiento_controlador.validar_correo", return_value=False), \
            patch("controladores.recepcionamiento_controlador.QMessageBox.warning") as mock_warn:
        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        ctrl._recopilar_datos = MagicMock(return_value={
            "DNI": "00000000Z",
            "Motivo": "Revisión",
            "Matrícula": "1234ABC",
            "Email": "correo#invalido"
        })
        ctrl.confirmar_recepcionamiento()
        mock_warn.assert_called()


def test_confirmar_recepcionamiento_inserta_si_valido(vista_mock, datos_mock):
    """
    Verifica que cuando los datos introducidos son correctos, 
    se realiza la inserción en la base de datos y se informa al usuario.
    """
    vista_mock.checkbox_enviar_correo.isChecked.return_value = False
    with patch("controladores.recepcionamiento_controlador.obtener_cliente_id_por_dni", return_value=1), \
            patch("controladores.recepcionamiento_controlador.obtener_vehiculo_id_por_matricula", return_value=2), \
            patch("controladores.recepcionamiento_controlador.obtener_estado_id_por_defecto", return_value=3), \
            patch("controladores.recepcionamiento_controlador.generar_documento_pdf", return_value="ruta/pdf"), \
            patch("controladores.recepcionamiento_controlador.insertar_recepcionamiento_en_bd", return_value=(True, None)) as mock_insert, \
            patch("controladores.recepcionamiento_controlador.QMessageBox.information") as mock_info:

        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        ctrl._recopilar_datos = MagicMock(return_value={
            "DNI": "12345678Z", "Matrícula": "1111ZZZ",
            "Email": "", "Motivo": "Revisión", "UltimaRevision": "01/01/2024",
            "ValorEstimado": "100", "ReparacionHasta": "200", "NúmeroRecepcion": "00042",
            "EstadoExterior": "Bien", "EstadoInterior": "Normal", "Observaciones": "Ninguna",
            "Arranca": "Sí", "Grúa": "No", "Seguro": "Sí", "Presupuesto": "No", "ITV": "Sí",
            "SeguroCompania": "Allianz", "Urgencia": "Alta"
        })
        ctrl.confirmar_recepcionamiento()

        mock_insert.assert_called()
        mock_info.assert_called()


def test_envio_correo_realizado_si_activo(vista_mock, datos_mock):
    """
    Comprueba que si el envío por correo está activado y el email es válido,
    se realiza correctamente el envío del PDF por correo electrónico.
    """
    vista_mock.checkbox_enviar_correo.isChecked.return_value = True
    vista_mock.input_correo.text.return_value = "cliente@correo.com"
    with patch("controladores.recepcionamiento_controlador.validar_correo", return_value=True), \
            patch("controladores.recepcionamiento_controlador.obtener_cliente_id_por_dni", return_value=1), \
            patch("controladores.recepcionamiento_controlador.obtener_vehiculo_id_por_matricula", return_value=2), \
            patch("controladores.recepcionamiento_controlador.obtener_estado_id_por_defecto", return_value=3), \
            patch("controladores.recepcionamiento_controlador.generar_documento_pdf", return_value="ruta/pdf"), \
            patch("controladores.recepcionamiento_controlador.insertar_recepcionamiento_en_bd", return_value=(True, None)), \
            patch("controladores.recepcionamiento_controlador.enviar_correo_con_pdf", return_value=(True, None)) as mock_correo:

        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        ctrl._recopilar_datos = MagicMock(return_value={
            "DNI": "00000000Z", "Email": "", "Motivo": "Revisión", "Matrícula": "1234ABC",
            "UltimaRevision": "", "ValorEstimado": "", "ReparacionHasta": "", "NúmeroRecepcion": "00001",
            "EstadoExterior": "", "EstadoInterior": "", "Observaciones": "",
            "Arranca": "No", "Grúa": "No", "Seguro": "No", "Presupuesto": "No", "ITV": "No",
            "SeguroCompania": "", "Urgencia": "Alta"
        })
        ctrl.confirmar_recepcionamiento()

        mock_correo.assert_called_once()


@patch("controladores.recepcionamiento_controlador.platform.system", return_value="Windows")
@patch("controladores.recepcionamiento_controlador.os.startfile")
def test_impresion_windows_activada(mock_startfile, mock_platform, vista_mock, datos_mock):
    """
    Comprueba que, si el usuario marca la opción de imprimir y el sistema es Windows,
    el PDF generado se manda a imprimir automáticamente usando `os.startfile(..., 'print')`.
    """
    vista_mock.checkbox_enviar_correo.isChecked.return_value = False
    vista_mock.checkbox_imprimir.isChecked.return_value = True
    vista_mock.input_correo.text.return_value.strip.return_value = ""

    with patch("controladores.recepcionamiento_controlador.obtener_cliente_id_por_dni", return_value=1), \
            patch("controladores.recepcionamiento_controlador.obtener_vehiculo_id_por_matricula", return_value=2), \
            patch("controladores.recepcionamiento_controlador.obtener_estado_id_por_defecto", return_value=3), \
            patch("controladores.recepcionamiento_controlador.generar_documento_pdf", return_value="ruta.pdf"), \
            patch("controladores.recepcionamiento_controlador.insertar_recepcionamiento_en_bd", return_value=(True, None)):

        ctrl = RecepcionamientoControlador(vista_mock, datos_mock)
        ctrl._recopilar_datos = MagicMock(return_value={
            "DNI": "00000000Z", "Email": "", "Motivo": "Revisión",
            "UltimaRevision": "", "ValorEstimado": "", "ReparacionHasta": "", "NúmeroRecepcion": "00001",
            "EstadoExterior": "", "EstadoInterior": "", "Observaciones": "",
            "Arranca": "No", "Grúa": "No", "Seguro": "No", "Presupuesto": "No", "ITV": "No",
            "SeguroCompania": "", "Urgencia": "Alta",
            "Matrícula": "1234ABC"
        })
        ctrl.confirmar_recepcionamiento()
        mock_startfile.assert_called_once_with("ruta.pdf", "print")
