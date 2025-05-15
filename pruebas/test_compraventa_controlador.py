"""
Módulo de pruebas unitarias para el controlador CompraventaControlador.

Este archivo verifica el correcto funcionamiento de las funciones principales del controlador
responsable de la lógica de la ventana de compra-venta de vehículos.

Las pruebas se realizan con una clase `VistaDummy` que simula los elementos visuales 
sin necesidad de lanzar la interfaz gráfica real. Se emplean mocks para evitar accesos
reales a disco, navegador o base de datos, permitiendo testear la lógica de forma aislada.
"""

import sys
import pytest
import webbrowser
from unittest.mock import MagicMock
from PySide6.QtWidgets import (
    QApplication, QComboBox, QLineEdit, QTextEdit, QMessageBox
)
from controladores.compraventa_controlador import CompraventaControlador


@pytest.fixture(scope="session", autouse=True)
def app():
    """
    Crea una única instancia de QApplication para todos los tests que
    interactúan con widgets de PySide6. Es obligatoria para evitar errores de entorno.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


class VistaDummy:
    """
    Vista simulada para pruebas unitarias del controlador de compra-venta.

    Contiene todos los atributos y métodos necesarios para simular
    la interacción del controlador con la interfaz real.
    """

    def __init__(self):
        # Campos de cliente
        self.cliente_nombre = QLineEdit()
        self.cliente_dni = QLineEdit()
        self.cliente_telefono = QLineEdit()
        self.cliente_email = QLineEdit()
        self.cliente_direccion = QLineEdit()
        self.cliente_localidad = QLineEdit()
        self.cliente_provincia = QLineEdit()
        self.cliente_observaciones = QTextEdit()

        # Campos de ruta de guardado
        self.input_ruta_guardado_compra = QLineEdit()
        self.input_ruta_guardado_venta = QLineEdit()
        self.checkbox_ruta_predeterminada_compra = MagicMock()
        self.checkbox_ruta_predeterminada_venta = MagicMock()
        self.boton_buscar_ruta_compra = MagicMock()
        self.boton_buscar_ruta_venta = MagicMock()

        # Combos para filtros de búsqueda
        self.filtros = {
            "marca": QComboBox(),
            "anio": QComboBox(),
            "color": QComboBox(),
            "combustible": QComboBox(),
            "kilometros": QComboBox(),
            "potencia_cv": QComboBox(),
            "cambio": QComboBox(),
            "puertas": QComboBox(),
            "plazas": QComboBox(),
            "precio_venta": QComboBox(),
        }

        # Tabla de vehículos y campos asociados
        self.tabla_vehiculos = MagicMock()
        self.vehiculos_disponibles = []
        self.vehiculos_filtrados = []

        self.vehiculo_marca = QLineEdit()
        self.vehiculo_modelo = QLineEdit()
        self.vehiculo_version = QLineEdit()
        self.vehiculo_anio = QLineEdit()
        self.vehiculo_matricula = QLineEdit()
        self.vehiculo_bastidor = QLineEdit()
        self.vehiculo_color = QLineEdit()
        self.vehiculo_combustible = QLineEdit()
        self.vehiculo_km = QLineEdit()
        self.vehiculo_cv = QLineEdit()
        self.vehiculo_cambio = QLineEdit()
        self.vehiculo_puertas = QLineEdit()
        self.vehiculo_plazas = QLineEdit()
        self.vehiculo_precio_compra = QLineEdit()
        self.vehiculo_precio_venta = QLineEdit()
        self.vehiculo_descuento = QLineEdit()


# ───────────────────────────────────────────────
# TESTS UNITARIOS PARA EL CONTROLADOR
# ───────────────────────────────────────────────

def test_inicializar_autocompletado_nombre_no_falla():
    """Verifica que el autocompletado de nombre se inicializa sin errores."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    controlador.inicializar_autocompletado_nombre()


def test_inicializar_autocompletado_dni_no_falla():
    """Verifica que el autocompletado de DNI se inicializa sin errores."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    controlador.inicializar_autocompletado_dni()


def test_autocompletar_por_nombre_dispara_busqueda():
    """Verifica que al completar nombre se dispare la búsqueda correspondiente."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    controlador.buscar_cliente_por_nombre = MagicMock()
    controlador.autocompletar_por_nombre("CRESNIK TEST")
    controlador.buscar_cliente_por_nombre.assert_called_once()


def test_toggle_ruta_guardado_activa_input():
    """Verifica que al desactivar la ruta predeterminada, el input se habilite."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    controlador.toggle_ruta_guardado(
        False, vista.input_ruta_guardado_compra, vista.boton_buscar_ruta_compra, tipo="compra")
    assert vista.input_ruta_guardado_compra.isEnabled()


def test_toggle_ruta_guardado_predeterminado():
    """Verifica que al activar la ruta predeterminada, se rellene el input automáticamente."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    controlador.toggle_ruta_guardado(
        True, vista.input_ruta_guardado_venta, vista.boton_buscar_ruta_venta, tipo="venta")
    assert vista.input_ruta_guardado_venta.text() != ""


def test_actualizar_tabla_vehiculos_filtra_disponibles_y_reservados():
    """Verifica que el filtrado solo incluya vehículos disponibles o reservados."""
    vista = VistaDummy()
    vista.vehiculos_disponibles = [
        {"estado": "DISPONIBLE"},
        {"estado": "RESERVADO"},
        {"estado": "VENDIDO"},
    ]
    for combo in vista.filtros.values():
        combo.addItem("Cualquiera")
        combo.setCurrentIndex(0)

    controlador = CompraventaControlador(vista)
    controlador.actualizar_tabla_vehiculos()

    estados = [veh["estado"] for veh in vista.vehiculos_filtrados]
    assert all(e in ("DISPONIBLE", "RESERVADO") for e in estados)


def test_llenar_valores_filtros_funciona_correctamente():
    """Verifica que los filtros se llenan correctamente a partir de los vehículos disponibles."""
    vista = VistaDummy()
    vista.vehiculos_disponibles = [{
        "marca": "Toyota", "anio": "2021", "color": "Rojo", "combustible": "Gasolina",
        "kilometros": "30000", "potencia_cv": "100", "cambio": "Manual",
        "puertas": "5", "plazas": "5", "precio_venta": "12000"
    }]
    controlador = CompraventaControlador(vista)
    controlador.llenar_valores_filtros()
    for combo in vista.filtros.values():
        assert combo.count() > 0


def test_buscar_cliente_por_nombre_encuentra(monkeypatch):
    """Verifica que si el cliente existe, se rellena automáticamente."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    vista.cliente_nombre.setText("CLIENTE EXISTENTE")

    dummy_cliente = (1, "CLIENTE", "", "", "", "123456789",
                     "test@email.com", "Calle Falsa", "", "Ciudad", "Provincia", "Obs")

    monkeypatch.setattr(
        "controladores.compraventa_controlador.obtener_datos_cliente_por_nombre", lambda nombre: dummy_cliente)
    controlador.rellenar_datos_cliente = MagicMock()

    controlador.buscar_cliente_por_nombre()
    controlador.rellenar_datos_cliente.assert_called_once_with(dummy_cliente)
    assert controlador.cliente_id == 1


def test_buscar_cliente_por_nombre_no_encuentra(monkeypatch):
    """Verifica que si no se encuentra el cliente, se propone crear uno nuevo."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)
    vista.cliente_nombre.setText("CLIENTE DESCONOCIDO")

    monkeypatch.setattr(
        "modelos.nuevoCliente_compraventa_consulta.obtener_datos_cliente_por_nombre", lambda nombre: None)
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.question",
                        lambda *a, **k: QMessageBox.No)

    controlador.abrir_ventana_nuevo_cliente = MagicMock()
    controlador.buscar_cliente_por_nombre()
    controlador.abrir_ventana_nuevo_cliente.assert_not_called()


def test_obtener_vehiculo_seleccionado_devuelve_correcto():
    """Verifica que se obtenga correctamente el vehículo seleccionado en la tabla."""
    vista = VistaDummy()
    vista.vehiculos_filtrados = [{"id": 1}, {"id": 2}, {"id": 3}]
    vista.tabla_vehiculos.currentRow = MagicMock(return_value=1)

    controlador = CompraventaControlador(vista)
    vehiculo = controlador.obtener_vehiculo_seleccionado()
    assert vehiculo == {"id": 2}


def test_simular_contrato_compra_abre_navegador(monkeypatch):
    """Verifica que se genera el contrato de compra y se abre en el navegador correctamente."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)

    # Simulamos generación de HTML
    controlador.generar_contrato_compra_html = MagicMock(
        return_value="ruta/ficticia.html")
    monkeypatch.setattr("webbrowser.open", MagicMock())
    monkeypatch.setattr(
        "PySide6.QtWidgets.QMessageBox.information", lambda *a, **k: None)

    # Datos necesarios
    vista.capturador_firma = MagicMock(
        obtener_imagen_base64=MagicMock(return_value="base64data"))
    vista.cliente_nombre.setText("CRESNIK")
    vista.cliente_dni.setText("12345678A")
    vista.cliente_direccion.setText("Calle A")
    vista.cliente_localidad.setText("Ciudad")
    vista.cliente_provincia.setText("Provincia")
    vista.cliente_telefono.setText("600000000")
    vista.vehiculo_precio_compra.setText("10000")
    vista.vehiculo_matricula.setText("1234ABC")
    vista.vehiculo_marca.setText("Marca")
    vista.vehiculo_modelo.setText("Modelo")
    vista.vehiculo_version.setText("Versión")
    vista.vehiculo_bastidor.setText("Bast123")
    vista.vehiculo_anio.setText("2024")
    vista.vehiculo_km.setText("50000")
    vista.vehiculo_color.setText("Rojo")

    controlador.simular_contrato_compra()
    controlador.generar_contrato_compra_html.assert_called_once()
    webbrowser.open.assert_called_once()


def test_aceptar_contrato_compra_guarda_pdf(monkeypatch, tmp_path):
    """Verifica que se genere correctamente el PDF del contrato y se guarde sin errores."""
    vista = VistaDummy()
    controlador = CompraventaControlador(vista)

    # Cliente
    vista.cliente_nombre.setText("Test Cliente")
    vista.cliente_dni.setText("12345678A")
    vista.cliente_telefono.setText("600000000")
    vista.cliente_email.setText("test@correo.com")
    vista.cliente_direccion.setText("Calle A")
    vista.cliente_localidad.setText("Ciudad")
    vista.cliente_provincia.setText("Provincia")
    vista.cliente_observaciones.setText("Sin observaciones")

    # Vehículo
    vista.vehiculo_marca.setText("Toyota")
    vista.vehiculo_modelo.setText("Yaris")
    vista.vehiculo_version.setText("Sport")
    vista.vehiculo_anio.setText("2023")
    vista.vehiculo_matricula.setText("1234ABC")
    vista.vehiculo_bastidor.setText("BAS123")
    vista.vehiculo_color.setText("Rojo")
    vista.vehiculo_combustible.setText("Gasolina")
    vista.vehiculo_km.setText("50000")
    vista.vehiculo_cv.setText("90")
    vista.vehiculo_cambio.setText("Manual")
    vista.vehiculo_puertas.setText("5")
    vista.vehiculo_plazas.setText("5")
    vista.vehiculo_precio_compra.setText("8000")
    vista.vehiculo_precio_venta.setText("12000")
    vista.vehiculo_descuento.setText("0")
    vista.input_ruta_guardado_compra.setText(str(tmp_path))

    # Parcheo de funciones externas
    monkeypatch.setattr("os.makedirs", lambda *args, **kwargs: None)
    monkeypatch.setattr("shutil.copy", lambda *args, **kwargs: None)
    monkeypatch.setattr("shutil.copy2", lambda *args, **kwargs: None)
    monkeypatch.setattr("os.path.exists", lambda path: False)
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MagicMock(
        __enter__=lambda s: MagicMock(write=lambda x: None),
        __exit__=lambda *a: None
    ))
    monkeypatch.setattr("weasyprint.HTML.write_pdf", lambda self, target: None)
    monkeypatch.setattr(
        "controladores.compraventa_controlador.obtener_id_cliente", lambda dni: 999)
    monkeypatch.setattr(
        "controladores.compraventa_controlador.insertar_nuevo_vehiculo", lambda datos: None)
    monkeypatch.setattr(
        "PySide6.QtWidgets.QMessageBox.critical", lambda *a, **k: None)
    monkeypatch.setattr(
        "PySide6.QtWidgets.QMessageBox.warning", lambda *a, **k: None)

    # No enviar correo ni imprimir
    vista.checkbox_correo_compra = MagicMock(
        isChecked=MagicMock(return_value=False))
    vista.checkbox_imprimir_compra = MagicMock(
        isChecked=MagicMock(return_value=False))

    controlador.aceptar_contrato_compra()
