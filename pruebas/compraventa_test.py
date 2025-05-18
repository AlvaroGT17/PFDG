"""
Módulo de prueba para preparar y lanzar la ventana de compraventa (`VentanaCompraventa`) con datos simulados.

Este script:
- Simula la selección de operación (compra/venta).
- Rellena todos los campos del formulario con datos ficticios.
- Configura un controlador simulado (`MagicMock`) para evitar llamadas reales.

Diseñado para pruebas visuales y desarrollo de interfaz en el sistema ReyBoxes.
"""

from PySide6.QtWidgets import QComboBox
from vistas.ventana_compraventa import VentanaCompraventa
from unittest.mock import MagicMock


def simular_secciones(ventana):
    """
    Prepara y asigna manualmente las secciones del formulario.

    Esto es necesario antes de llamar a `actualizar_secciones()` ya que normalmente
    estas secciones se crean dinámicamente tras la selección del tipo de operación.

    Args:
        ventana (VentanaCompraventa): Instancia de la ventana a modificar.
    """
    ventana.seccion_cliente = ventana.crear_seccion_datos_cliente()
    ventana.seccion_vehiculo = ventana.crear_seccion_datos_vehiculo()
    ventana.seccion_operacion = ventana.crear_seccion_datos_operacion()


def cargar_datos_prueba(ventana):
    """
    Carga datos ficticios en todos los campos del formulario.

    Estos datos se usan para simular un contrato de compraventa sin depender de entrada manual.

    Args:
        ventana (VentanaCompraventa): Instancia de la ventana a rellenar.
    """
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
    """
    Inicializa una instancia de `VentanaCompraventa` con todos los datos necesarios simulados.

    Incluye:
    - ComboBox con operación seleccionada.
    - Controlador simulado (`MagicMock`) para evitar dependencias externas.
    - Campos de cliente y vehículo con información ficticia.

    Returns:
        VentanaCompraventa: Instancia completamente configurada lista para mostrar.
    """
    ventana = VentanaCompraventa(None)

    # Añadir combo simulado para seleccionar operación
    combo = QComboBox()
    combo.addItems([
        "Seleccione la operación deseada",
        "Compra por parte del concesionario",
        "Venta por parte del concesionario"
    ])
    combo.setCurrentText("Compra por parte del concesionario")
    ventana.combo_operacion = combo

    # Asignar controlador simulado
    ventana.controlador = MagicMock()
    ventana.controlador.toggle_ruta_guardado = MagicMock()
    ventana.controlador.simular_contrato = MagicMock()
    ventana.controlador.aceptar_contrato_compra = MagicMock()

    # Crear y asignar secciones manualmente
    simular_secciones(ventana)

    # Simular selección para activar la interfaz
    ventana.actualizar_secciones("Compra por parte del concesionario")

    # Cargar campos con datos ficticios
    cargar_datos_prueba(ventana)

    return ventana

# para ejecutar el modulo desde consola:
# python -m pruebas.compraventa_test
