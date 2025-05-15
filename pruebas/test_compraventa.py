from unittest.mock import MagicMock
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox
from vistas.ventana_compraventa import VentanaCompraventa


def iniciar_ventana_compraventa():
    """
    Inicializa la ventana de compraventa con un layout de prueba.

    Se sustituyen dependencias externas como el controlador real por un mock.
    Se configura el layout con las secciones y widgets necesarios para pruebas.
    """
    ventana = VentanaCompraventa(None)
    ventana.controlador = MagicMock()

    # Crear manualmente las secciones necesarias para las pruebas
    ventana.seccion_cliente = ventana.crear_seccion_datos_cliente()
    ventana.seccion_vehiculo = ventana.crear_seccion_datos_vehiculo()
    ventana.seccion_operacion = ventana.crear_seccion_datos_operacion()

    # En caso de que el combo no se haya inicializado aún, lo añadimos
    if not hasattr(ventana, "combo_operacion"):
        ventana.combo_operacion = QComboBox()
        ventana.combo_operacion.addItems([
            "Seleccione la operación deseada",
            "Compra por parte del concesionario",
            "Venta por parte del concesionario"
        ])
        ventana.combo_operacion.setCurrentIndex(0)

    layout = QVBoxLayout()
    layout.addWidget(QLabel("Tipo de operación:"))
    layout.addWidget(ventana.combo_operacion)
    layout.addWidget(ventana.seccion_cliente['grupo'])
    layout.addWidget(ventana.seccion_vehiculo['grupo'])
    layout.addWidget(ventana.seccion_operacion['grupo'])
    layout.addWidget(ventana.mensaje_firma_compra.parentWidget())
    layout.addWidget(ventana.mensaje_firma_venta.parentWidget())

    ventana.setLayout(layout)
    return ventana


def test_ventana_compraventa_carga_correcta(qtbot):
    """
    Verifica que los campos de cliente y vehículo se puedan establecer correctamente.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)

    ventana.cliente_nombre.setText("SERGIO CABRERA PEÑA")
    ventana.vehiculo_marca.setText("SEAT")
    ventana.vehiculo_precio_compra.setText("8500")

    assert ventana.cliente_nombre.text() == "SERGIO CABRERA PEÑA"
    assert ventana.vehiculo_marca.text() == "SEAT"
    assert ventana.vehiculo_precio_compra.text() == "8500"


def test_actualizar_secciones_compra(qtbot):
    """
    Verifica que las secciones adecuadas se activen al seleccionar operación de compra.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()
    qtbot.waitExposed(ventana)

    ventana.actualizar_secciones("COMPRA POR PARTE DEL CONCESIONARIO")

    assert ventana.seccion_cliente['contenido'].isVisible()
    assert ventana.seccion_vehiculo['contenido'].isVisible()
    assert not ventana.seccion_operacion['contenido'].isVisible()


def test_actualizar_secciones_venta(qtbot):
    """
    Verifica que las secciones adecuadas se activen al seleccionar operación de venta.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()
    qtbot.waitExposed(ventana)

    ventana.actualizar_secciones("VENTA POR PARTE DEL CONCESIONARIO")

    assert ventana.seccion_cliente['contenido'].isVisible()
    assert ventana.seccion_operacion['contenido'].isVisible()
    assert not ventana.seccion_vehiculo['contenido'].isVisible()


def test_actualizar_secciones_seleccione(qtbot):
    """
    Verifica que todas las secciones se oculten al seleccionar la opción por defecto.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()
    qtbot.waitExposed(ventana)

    ventana.actualizar_secciones("Seleccione la operación deseada")

    assert not ventana.seccion_cliente['contenido'].isVisible()
    assert not ventana.seccion_vehiculo['contenido'].isVisible()
    assert not ventana.seccion_operacion['contenido'].isVisible()


def test_toggle_firma_compra(qtbot):
    """
    Verifica la activación y desactivación de la firma para la operación de compra.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()
    qtbot.wait(100)

    ventana.toggle_firma(ventana.capturador_firma, ventana.boton_activar_firma)
    assert ventana.firma_activa_compra
    assert ventana.mensaje_firma_compra.isVisible()

    ventana.toggle_firma(ventana.capturador_firma, ventana.boton_activar_firma)
    assert not ventana.firma_activa_compra
    assert not ventana.mensaje_firma_compra.isVisible()


def test_toggle_firma_venta(qtbot):
    """
    Verifica la activación y desactivación de la firma para la operación de venta.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()
    qtbot.wait(100)

    ventana.toggle_firma(ventana.capturador_firma_venta,
                         ventana.boton_activar_firma_venta)
    assert ventana.firma_activa_venta
    assert ventana.mensaje_firma_venta.isVisible()

    ventana.toggle_firma(ventana.capturador_firma_venta,
                         ventana.boton_activar_firma_venta)
    assert not ventana.firma_activa_venta
    assert not ventana.mensaje_firma_venta.isVisible()


def test_toggle_ruta_guardado_compra(qtbot):
    """
    Verifica que al desactivar el checkbox de ruta predeterminada se invoque correctamente el controlador.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.controlador.toggle_ruta_guardado = MagicMock()
    ventana.checkbox_ruta_predeterminada_compra.setChecked(False)

    ventana.controlador.toggle_ruta_guardado.assert_called_once_with(
        False,
        ventana.input_ruta_guardado_compra,
        ventana.boton_buscar_ruta_compra,
        "compra"
    )


def test_event_filter_enter_key_cierra_firma(qtbot):
    """
    Simula pulsación de tecla ENTER y verifica que se cierre la firma si está activa.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.toggle_firma(ventana.capturador_firma, ventana.boton_activar_firma)
    assert ventana.firma_activa_compra

    evento = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
    handled = ventana.eventFilter(ventana.capturador_firma, evento)

    assert handled is True
    assert not ventana.firma_activa_compra


def test_borrar_todo_resetea_campos(qtbot):
    """
    Verifica que el método borrar_todo limpie correctamente todos los campos y estados.
    """
    ventana = iniciar_ventana_compraventa()
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.cliente_nombre.setText("CRESNIK")
    ventana.combo_operacion.setCurrentIndex(1)
    ventana.firma_activa_compra = True
    ventana.mensaje_firma_compra.setVisible(True)

    ventana.borrar_todo()

    assert ventana.cliente_nombre.text() == ""
    assert ventana.combo_operacion.currentIndex() == 0
    assert not ventana.firma_activa_compra
    assert not ventana.mensaje_firma_compra.isVisible()
