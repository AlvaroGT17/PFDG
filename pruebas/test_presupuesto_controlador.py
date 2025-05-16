# pruebas/test_presupuesto_controlador.py
"""
Tests para el controlador de presupuestos (`PresupuestoControlador`).

Objetivos:
- Verificar la inicialización del controlador.
- Verificar el comportamiento cuando no hay recepciones disponibles.
- Comprobar que se genera correctamente un PDF simulado.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from controladores.presupuesto_controlador import PresupuestoControlador
from vistas.ventana_presupuesto import VentanaPresupuesto


@pytest.fixture
def mock_ventana(qtbot):
    ventana = VentanaPresupuesto()
    qtbot.addWidget(ventana)
    return ventana


def test_init_conecta_controlador_y_boton(mock_ventana):
    with patch("controladores.presupuesto_controlador.obtener_recepciones_para_presupuesto", return_value=[]):
        controlador = PresupuestoControlador(mock_ventana)
        assert controlador.ventana == mock_ventana
        assert hasattr(mock_ventana, "controlador")
        assert isinstance(controlador.recepciones, list)


def test_cargar_recepciones_vacia(mock_ventana):
    with patch("controladores.presupuesto_controlador.obtener_recepciones_para_presupuesto", return_value=[]):
        controlador = PresupuestoControlador(mock_ventana)
        assert mock_ventana.combo_recepciones.count() == 1
        assert mock_ventana.combo_recepciones.currentText() == "No hay recepciones disponibles"
        assert not mock_ventana.combo_recepciones.isEnabled()


def test_generar_pdf_presupuesto_crea_archivo(tmp_path):
    datos = {
        "cliente": "Juan Pérez",
        "matricula": "1234ABC",
        "fecha_recepcion": "01/01/2025 10:00",
        "precio_max": "500.00",
        "respuesta_cliente": "Aceptado",
        "observaciones": "Revisión general",
        "total_estimado": "450.00",
        "tareas": [
            {"descripcion": "Cambio de aceite", "horas": 1.5,
                "precio_hora": 40, "total": 60},
            {"descripcion": "Filtro aire", "horas": 1,
                "precio_hora": 30, "total": 30}
        ]
    }

    with patch("controladores.presupuesto_controlador.Template.render", return_value="<html></html>"), \
            patch("controladores.presupuesto_controlador.HTML.write_pdf") as mock_write, \
            patch("controladores.presupuesto_controlador.os.makedirs"):

        controlador = PresupuestoControlador(MagicMock())
        ruta = controlador.generar_pdf_presupuesto(datos)

    mock_write.assert_called_once()
    assert ruta.endswith(".pdf")
