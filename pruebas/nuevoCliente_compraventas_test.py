if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from vistas.ventana_nuevoCliente_compraventas import VentanaNuevoClienteCompraventas

    def guardar_cliente(datos):
        print("Datos del nuevo cliente:", datos)

    app = QApplication(sys.argv)
    ventana = VentanaNuevoClienteCompraventas(callback_guardar=guardar_cliente)
    ventana.show()
    sys.exit(app.exec())

# Para poder ejecutar, en la terminal de la carpeta del proyecto, ejecutar:
#     python -m pruebas.nuevoCliente_compraventas_test
