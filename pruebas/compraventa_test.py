from PySide6.QtWidgets import QComboBox
from vistas.ventana_compraventa import VentanaCompraventa
from unittest.mock import MagicMock


def simular_secciones(ventana):
    """
    Prepara las secciones necesarias para que los atributos existan antes de cargar datos.
    """
    ventana.seccion_cliente = ventana.crear_seccion_datos_cliente()
    ventana.seccion_vehiculo = ventana.crear_seccion_datos_vehiculo()
    ventana.seccion_operacion = ventana.crear_seccion_datos_operacion()


def cargar_datos_prueba(ventana):
    ventana.cliente_nombre.setText("SERGIO CABRERA PEÑA")
    ventana.cliente_dni.setText("99001122T")
    ventana.cliente_telefono.setText("437913693")
    ventana.cliente_email.setText("sergio.c@example.com")
    ventana.cliente_direccion.setText("Calle Alta 22")
    ventana.cliente_localidad.setText("Badajoz")
    ventana.cliente_provincia.setText("Extremadura")
    ventana.cliente_observaciones.setText(
        "Cliente habitual. Buen estado financiero.")

    ventana.vehiculo_matricula.setText("1234ABC")
    ventana.vehiculo_marca.setText("SEAT")
    ventana.vehiculo_modelo.setText("Ibiza")
    ventana.vehiculo_version.setText("Style")
    ventana.vehiculo_anio.setText("2021")
    ventana.vehiculo_bastidor.setText("VSSZZZ6JZMR012345")
    ventana.vehiculo_color.setText("Rojo")
    ventana.vehiculo_cv.setText("95")
    ventana.vehiculo_combustible.setText("Gasolina")
    ventana.vehiculo_km.setText("43000")
    ventana.vehiculo_cambio.setText("Manual")
    ventana.vehiculo_puertas.setText("5")
    ventana.vehiculo_plazas.setText("5")
    ventana.vehiculo_precio_compra.setText("8500")
    ventana.vehiculo_precio_venta.setText("9990")
    ventana.vehiculo_descuento.setText("5")


def iniciar_ventana_compraventa():
    ventana = VentanaCompraventa(None)

    # Añadir combo simulado
    combo = QComboBox()
    combo.addItems([
        "Seleccione la operación deseada",
        "Compra por parte del concesionario",
        "Venta por parte del concesionario"
    ])
    combo.setCurrentText("Compra por parte del concesionario")
    ventana.combo_operacion = combo

    # Añadir un controlador simulado
    ventana.controlador = MagicMock()
    ventana.controlador.toggle_ruta_guardado = MagicMock()
    ventana.controlador.simular_contrato = MagicMock()
    ventana.controlador.aceptar_contrato_compra = MagicMock()

    # Crear secciones después de asignar el controlador
    simular_secciones(ventana)

    # Simular la selección para activar secciones
    ventana.actualizar_secciones("Compra por parte del concesionario")

    cargar_datos_prueba(ventana)

    return ventana
