# pruebas/test_inicio.py
# ───────────────────────
"""
Pruebas unitarias para la clase VentanaInicio.

Se valida:
- Inicialización de la ventana.
- Existencia de atributos como botones, saludo y rol.
- Visibilidad de botones según rol.
- Comportamiento del evento de cierre.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""


import pytest
from unittest.mock import patch, MagicMock
from controladores.inicio_controlador import InicioControlador
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCloseEvent
from vistas.ventana_inicio import VentanaInicio


def test_inicio_se_inicializa_correctamente(qtbot):
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert ventana.nombre == "CRESNIK"
        assert ventana.rol == "ADMINISTRADOR"


def test_inicio_tiene_botones(qtbot):
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert hasattr(ventana, "botones")


def test_saludo_y_rol_visibles(qtbot):
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert ventana.nombre == "CRESNIK"
        assert ventana.rol == "ADMINISTRADOR"


def test_close_event_restringido(qtbot):
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Test", "ADMINISTRADOR")
        qtbot.addWidget(ventana)

        ventana.forzar_cierre = False

        class FakeEvent:
            def ignore(self, *_):  # <- acepta argumento
                ventana._cerrado = False

        evento = FakeEvent()
        ventana.closeEvent(evento)

        assert not getattr(ventana, "_cerrado", True)


def test_close_event_forzado(qtbot):
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Test", "ADMINISTRADOR")
        qtbot.addWidget(ventana)

        ventana.forzar_cierre = True

        class FakeEvent:
            def accept(self, *_):  # <- acepta argumento
                ventana._cerrado = True

        evento = FakeEvent()
        ventana.closeEvent(evento)

        assert getattr(ventana, "_cerrado", False)


@pytest.fixture
def controlador():
    with patch("controladores.inicio_controlador.VentanaInicio") as mock_ventana, \
            patch("controladores.inicio_controlador.InicioControlador.obtener_id_usuario", return_value=1):
        mock_ventana.return_value.botones = {
            "cerrar sesión": MagicMock(),
            "fichar": MagicMock(),
            "historial\nfichaje": MagicMock(),
            "crear usuarios": MagicMock(),
            "clientes": MagicMock(),
            "vehículos": MagicMock(),
            "recepcionamiento": MagicMock(),
            "presupuestos": MagicMock(),
            "compraventa": MagicMock(),
            "reimpresion\nrecepcionamientos": MagicMock(),
            "reimpresion\npresupuestos": MagicMock(),
            "reimpresion\ncompras": MagicMock(),
            "reimpresion\nventas": MagicMock()
        }
        return InicioControlador("Test", "ADMINISTRADOR")


def test_abrir_fichaje_dispara_mostrar(controlador):
    with patch("controladores.inicio_controlador.FicharControlador") as mock_fichar:
        instancia = mock_fichar.return_value
        controlador.abrir_fichaje()
        instancia.mostrar.assert_called_once()


def test_abrir_historial_admin(controlador):
    with patch("controladores.inicio_controlador.HistorialControlador") as mock_historial:
        instancia = mock_historial.return_value
        controlador.abrir_historial()
        instancia.mostrar.assert_called_once()


def test_abrir_clientes(controlador):
    with patch("controladores.inicio_controlador.ClientesControlador") as mock_clientes:
        controlador.abrir_clientes()
        mock_clientes.assert_called_once()


def test_abrir_vehiculos(controlador):
    with patch("controladores.inicio_controlador.VehiculosControlador") as mock_vehiculos:
        controlador.abrir_vehiculos()
        mock_vehiculos.assert_called_once()


@patch("controladores.presupuesto_controlador.PresupuestoControlador")
@patch("controladores.inicio_controlador.VentanaPresupuesto")
def test_abrir_presupuestos(mock_dialogo, mock_presupuesto, controlador):
    instancia = mock_dialogo.return_value
    instancia.exec = MagicMock()
    controlador.abrir_presupuestos()
    instancia.exec.assert_called_once()


def test_abrir_compraventa(controlador):
    with patch("controladores.inicio_controlador.VentanaCompraventa") as mock_ventana:
        instancia = mock_ventana.return_value
        controlador.abrir_compraventa()
        instancia.show.assert_called_once()


def test_abrir_reimpresiones(controlador):
    with patch("controladores.inicio_controlador.ReimpresionPresupuestosControlador") as mock_pre, \
            patch("controladores.inicio_controlador.ReimpresionRecepcionamientoControlador") as mock_rec, \
            patch("controladores.inicio_controlador.ReimpresionComprasControlador") as mock_com, \
            patch("controladores.inicio_controlador.ReimpresionVentasControlador") as mock_ven:

        controlador.abrir_reimpresion_presupuestos()
        controlador.abrir_reimpresion_recepcionamientos()
        controlador.abrir_reimpresion_compras()
        controlador.abrir_reimpresion_ventas()

        mock_pre.assert_called_once()
        mock_rec.assert_called_once()
        mock_com.assert_called_once()
        mock_ven.assert_called_once()
