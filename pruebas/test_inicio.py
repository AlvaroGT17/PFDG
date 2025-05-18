# pruebas/test_inicio.py
# ───────────────────────
"""
Pruebas unitarias para la clase `VentanaInicio` y su controlador `InicioControlador`.

Se valida:
- La correcta inicialización de la ventana principal.
- La visibilidad de atributos clave como botones, saludo y rol.
- El comportamiento del evento de cierre (forzado o restringido).
- Que cada acción de menú abre correctamente su controlador o ventana correspondiente.

Se utilizan mocks para evitar la ejecución real de controladores o diálogos.

"""

import pytest
from unittest.mock import patch, MagicMock
from controladores.inicio_controlador import InicioControlador
from vistas.ventana_inicio import VentanaInicio


def test_inicio_se_inicializa_correctamente(qtbot):
    """
    Verifica que la ventana de inicio se inicializa correctamente 
    con el nombre y rol en mayúsculas.
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert ventana.nombre == "CRESNIK"
        assert ventana.rol == "ADMINISTRADOR"


def test_inicio_tiene_botones(qtbot):
    """
    Comprueba que la ventana contiene el atributo `botones`,
    el cual es clave para las acciones del menú principal.
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert hasattr(ventana, "botones")


def test_saludo_y_rol_visibles(qtbot):
    """
    Verifica que los atributos `nombre` y `rol` están correctamente 
    inicializados y accesibles desde la instancia de la ventana.
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert ventana.nombre == "CRESNIK"
        assert ventana.rol == "ADMINISTRADOR"


def test_close_event_restringido(qtbot):
    """
    Simula un cierre no autorizado (`forzar_cierre = False`) y verifica
    que el evento de cierre es ignorado (la ventana no se cierra).
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Test", "ADMINISTRADOR")
        qtbot.addWidget(ventana)

        ventana.forzar_cierre = False

        class FakeEvent:
            def ignore(self, *_):
                ventana._cerrado = False

        evento = FakeEvent()
        ventana.closeEvent(evento)

        assert not getattr(ventana, "_cerrado", True)


def test_close_event_forzado(qtbot):
    """
    Simula un cierre autorizado (`forzar_cierre = True`) y verifica
    que el evento se acepta y se marca como cerrado.
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Test", "ADMINISTRADOR")
        qtbot.addWidget(ventana)

        ventana.forzar_cierre = True

        class FakeEvent:
            def accept(self, *_):
                ventana._cerrado = True

        evento = FakeEvent()
        ventana.closeEvent(evento)

        assert getattr(ventana, "_cerrado", False)


@pytest.fixture
def controlador():
    """
    Crea una instancia simulada de `InicioControlador` con los botones necesarios
    y un ID de usuario simulado. Evita cargar la interfaz gráfica real.
    """
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
    """
    Verifica que al abrir la opción de fichaje, se crea el controlador correspondiente
    y se llama al método `mostrar`.
    """
    with patch("controladores.inicio_controlador.FicharControlador") as mock_fichar:
        instancia = mock_fichar.return_value
        controlador.abrir_fichaje()
        instancia.mostrar.assert_called_once()


def test_abrir_historial_admin(controlador):
    """
    Verifica que se abre correctamente el historial de fichajes para el administrador.
    """
    with patch("controladores.inicio_controlador.HistorialControlador") as mock_historial:
        instancia = mock_historial.return_value
        controlador.abrir_historial()
        instancia.mostrar.assert_called_once()


def test_abrir_clientes(controlador):
    """
    Comprueba que se instancia el controlador de clientes al seleccionar dicha opción.
    """
    with patch("controladores.inicio_controlador.ClientesControlador") as mock_clientes:
        controlador.abrir_clientes()
        mock_clientes.assert_called_once()


def test_abrir_vehiculos(controlador):
    """
    Comprueba que se instancia el controlador de vehículos correctamente.
    """
    with patch("controladores.inicio_controlador.VehiculosControlador") as mock_vehiculos:
        controlador.abrir_vehiculos()
        mock_vehiculos.assert_called_once()


@patch("controladores.presupuesto_controlador.PresupuestoControlador")
@patch("controladores.inicio_controlador.VentanaPresupuesto")
def test_abrir_presupuestos(mock_dialogo, mock_presupuesto, controlador):
    """
    Verifica que al abrir presupuestos se muestra el diálogo modal correspondiente.
    """
    instancia = mock_dialogo.return_value
    instancia.exec = MagicMock()
    controlador.abrir_presupuestos()
    instancia.exec.assert_called_once()


def test_abrir_compraventa(controlador):
    """
    Verifica que se abre la ventana de compraventa correctamente al hacer clic en la opción.
    """
    with patch("controladores.inicio_controlador.VentanaCompraventa") as mock_ventana:
        instancia = mock_ventana.return_value
        controlador.abrir_compraventa()
        instancia.show.assert_called_once()


def test_abrir_reimpresiones(controlador):
    """
    Comprueba que al llamar a cada método de reimpresión se instancia correctamente
    el controlador asociado a: presupuestos, recepcionamientos, compras y ventas.
    """
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
