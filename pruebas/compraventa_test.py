import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_compraventa import VentanaCompraventa


def cargar_datos_prueba(ventana):
    # Seleccionar tipo de operación automáticamente
    ventana.combo_operacion.setCurrentText(
        "Compra por parte del concesionario")
    ventana.actualizar_secciones("COMPRA POR PARTE DEL CONCESIONARIO")

    # Simular cliente real
    ventana.cliente_nombre.setText("SERGIO CABRERA PEÑA")
    ventana.cliente_dni.setText("99001122T")
    ventana.cliente_telefono.setText("437913693")
    ventana.cliente_email.setText("sergio.c@example.com")
    ventana.cliente_direccion.setText("Calle Alta 22")
    ventana.cliente_localidad.setText("Badajoz")
    ventana.cliente_provincia.setText("Extremadura")
    ventana.cliente_observaciones.setText(
        "Cliente habitual. Buen estado financiero.")

    # Simular datos del vehículo
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_dummy = VentanaCompraventa(None)
    cargar_datos_prueba(ventana_dummy)
    ventana_dummy.show()
    sys.exit(app.exec())

# para ejecutar el test, usar el siguiente comando en la terminal:
# python -m pruebas.compraventa_test
