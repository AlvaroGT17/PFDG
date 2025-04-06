from PySide6.QtWidgets import QMessageBox
from utilidades.recepcionamiento_utilidades import validar_correo, generar_documento_pdf, capturar_firma


class RecepcionamientoControlador:
    def __init__(self, vista):
        """
        Inicializa el controlador con la vista asociada.
        """
        self.vista = vista
        self._conectar_eventos()

    def _conectar_eventos(self):
        """
        Conecta señales de la vista con funciones del controlador.
        """
        self.vista.boton_confirmar.clicked.connect(
            self.confirmar_recepcionamiento)
        self.vista.boton_cancelar.clicked.connect(self.vista.close)

    def confirmar_recepcionamiento(self):
        """
        Lógica principal al pulsar el botón de confirmar recepcionamiento.
        """
        datos = self._recopilar_datos()

        if self.vista.checkbox_enviar_correo.isChecked():
            correo = self.vista.input_correo.text().strip()
            if not validar_correo(correo):
                QMessageBox.warning(self.vista, "Correo inválido",
                                    "El correo electrónico introducido no es válido.")
                return
            datos["Correo destino"] = correo

        # Captura firma (futura integración con tableta)
        firma = capturar_firma()  # Por ahora devuelve None

        # Generar documento PDF
        ruta_pdf = generar_documento_pdf(datos, firma)

        # Mostrar confirmación (puede imprimirse, enviarse por correo, etc.)
        QMessageBox.information(
            self.vista, "Recepcionamiento generado", f"Documento generado:\n{ruta_pdf}")

        # TODO: Lógica adicional para guardar en base de datos y enviar si es necesario

        self.vista.close()

    def _recopilar_datos(self):
        """
        Extrae todos los datos del formulario en un diccionario plano.
        """
        motivo = None
        if self.vista.radio_reparacion.isChecked():
            motivo = "REPARACION"
        elif self.vista.radio_tasacion.isChecked():
            motivo = "TASACION"
        elif self.vista.radio_presupuesto.isChecked():
            motivo = "PRESUPUESTO"
        elif self.vista.radio_mantenimiento.isChecked():
            motivo = "MANTENIMIENTO"

        return {
            "Nombre": self.vista.input_nombre.text(),
            "DNI": self.vista.input_dni.text(),
            "Teléfono": self.vista.input_telefono.text(),
            "Email": self.vista.input_email.text(),
            "Dirección": self.vista.input_direccion.text(),

            "Matrícula": self.vista.input_matricula.text(),
            "Marca": self.vista.input_marca.text(),
            "Modelo": self.vista.input_modelo.text(),
            "Color": self.vista.input_color.text(),
            "Año": self.vista.input_anio.text(),
            "Kilómetros": self.vista.input_kilometros.text(),
            "Combustible": self.vista.input_combustible.text(),
            "VIN": self.vista.input_vin.text(),
            "Tipo de vehículo": self.vista.combo_tipo.currentText(),

            "Motivo": motivo,
        }
