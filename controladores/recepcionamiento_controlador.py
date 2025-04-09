from PySide6.QtWidgets import QMessageBox, QCompleter
from PySide6.QtCore import Qt
from utilidades.recepcionamiento_utilidades import validar_correo, generar_documento_pdf, capturar_firma
from modelos.clientes_consultas import obtener_clientes
from modelos.recepcionamiento_consultas import (
    obtener_matriculas_existentes,
    obtener_siguiente_numero_recepcionamiento,
    obtener_datos_vehiculo_por_matricula,
    obtener_matriculas_por_cliente,
    obtener_categorias_vehiculo,
    obtener_tipos_vehiculo,
    obtener_combustibles
)


class RecepcionamientoControlador:
    def __init__(self, vista):
        self.vista = vista
        self._conectar_eventos()
        self._configurar_autocompletado_clientes()
        self._cargar_combobox_vehiculos()
        self._configurar_autocompletado_matricula()
        self._asignar_numero_recepcionamiento()

    def _conectar_eventos(self):
        self.vista.boton_confirmar.clicked.connect(
            self.confirmar_recepcionamiento)
        self.vista.boton_cancelar.clicked.connect(self.vista.close)
        self.vista.input_matricula.currentTextChanged.connect(
            self._autocompletar_datos_vehiculo)
        self.vista.combo_categoria.currentTextChanged.connect(
            self._filtrar_tipos_por_categoria)

    def confirmar_recepcionamiento(self):
        datos = self._recopilar_datos()

        if self.vista.checkbox_enviar_correo.isChecked():
            correo = self.vista.input_correo.text().strip()
            if not validar_correo(correo):
                QMessageBox.warning(self.vista, "Correo inválido",
                                    "El correo electrónico introducido no es válido.")
                return
            datos["Correo destino"] = correo

        firma = capturar_firma()  # Por ahora devuelve None
        ruta_pdf = generar_documento_pdf(datos, firma)

        QMessageBox.information(
            self.vista, "Recepcionamiento generado", f"Documento generado:\n{ruta_pdf}")

        self.vista.close()

    def _recopilar_datos(self):
        motivo = self.vista.combo_motivo.currentText()

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

    def _configurar_autocompletado_clientes(self):
        self.datos_clientes = obtener_clientes()

        nombres = [
            f"{c['nombre']} {c['primer_apellido']} {c['segundo_apellido']}".strip()
            for c in self.datos_clientes
        ]
        completer_nombres = QCompleter(nombres)
        completer_nombres.setCaseSensitivity(Qt.CaseInsensitive)
        self.vista.input_nombre.setCompleter(completer_nombres)
        self.vista.input_nombre.editingFinished.connect(
            self._autocompletar_por_nombre)

        dnis = [c['dni'] for c in self.datos_clientes if c['dni']]
        completer_dni = QCompleter(dnis)
        completer_dni.setCaseSensitivity(Qt.CaseInsensitive)
        self.vista.input_dni.setCompleter(completer_dni)
        self.vista.input_dni.editingFinished.connect(
            self._autocompletar_por_dni)

    def _autocompletar_por_nombre(self):
        texto = self.vista.input_nombre.text().strip().upper()
        cliente = next((c for c in self.datos_clientes if
                        f"{c['nombre']} {c['primer_apellido']} {c['segundo_apellido']}".strip().upper() == texto), None)
        if cliente:
            self._rellenar_campos_cliente(cliente)

    def _autocompletar_por_dni(self):
        texto = self.vista.input_dni.text().strip().upper()
        cliente = next(
            (c for c in self.datos_clientes if c['dni'].upper() == texto), None)
        if cliente:
            self._rellenar_campos_cliente(cliente)

    def _rellenar_campos_cliente(self, cliente):
        self.vista.input_nombre.setText(
            f"{cliente['nombre']} {cliente['primer_apellido']} {cliente['segundo_apellido']}".strip())
        self.vista.input_dni.setText(cliente['dni'])
        self.vista.input_telefono.setText(cliente['telefono'] or "")
        self.vista.input_email.setText(cliente['email'] or "")
        self.vista.input_direccion.setText(cliente['direccion'] or "")
        self._actualizar_autocompletado_matriculas(cliente['dni'])

    def _autocompletar_datos_vehiculo(self, matricula=None):
        matricula = matricula or self.vista.input_matricula.currentText().strip().upper()
        if not matricula or matricula == "Seleccione una matrícula":
            return

        datos = obtener_datos_vehiculo_por_matricula(matricula)
        if datos:
            self.vista.input_marca.setText(datos["marca"] or "")
            self.vista.input_modelo.setText(datos["modelo"] or "")
            self.vista.input_color.setText(datos["color"] or "")
            self.vista.input_anio.setText(
                str(datos["anio"]) if datos["anio"] else "")
            self.vista.input_kilometros.setText(
                str(datos["kilometros"]) if datos["kilometros"] else "")
            self.vista.combo_combustible.setCurrentText(
                datos["combustible"] or "")
            self.vista.input_vin.setText(datos["numero_bastidor"] or "")
            self.vista.combo_categoria.setCurrentText(datos["categoria"] or "")
            self.vista.combo_tipo.setCurrentText(datos["tipo"] or "")

    def _cargar_combobox_vehiculos(self):
        categorias = obtener_categorias_vehiculo()
        self.tipos_vehiculos = obtener_tipos_vehiculo()
        combustibles = obtener_combustibles()

        # CATEGORÍAS
        self.vista.combo_categoria.clear()
        self.vista.combo_categoria.addItem("Seleccione la categoría")
        self.vista.combo_categoria.addItems(categorias)

        # TIPOS
        self.vista.combo_tipo.clear()
        self.vista.combo_tipo.addItem("Seleccione el tipo")

        # Si hay al menos una categoría, precargar sus tipos correspondientes
        if categorias:
            tipos_filtrados = [
                tipo['nombre'] for tipo in self.tipos_vehiculos if tipo['categoria'] == categorias[0]]
            self.vista.combo_tipo.addItems(tipos_filtrados)

        # COMBUSTIBLES
        self.vista.combo_combustible.clear()
        self.vista.combo_combustible.addItem("Seleccione el combustible")
        self.vista.combo_combustible.addItems(combustibles)

        self.vista.combo_categoria.currentTextChanged.connect(
            self._filtrar_tipos_por_categoria)

    def _filtrar_tipos_por_categoria(self):
        categoria_seleccionada = self.vista.combo_categoria.currentText()
        tipos_filtrados = [
            tipo['nombre'] for tipo in self.tipos_vehiculos if tipo['categoria'] == categoria_seleccionada
        ]
        self.vista.combo_tipo.clear()
        self.vista.combo_tipo.addItems(tipos_filtrados)

    def _configurar_autocompletado_matricula(self):
        matriculas = obtener_matriculas_existentes()
        completer = QCompleter(matriculas)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.vista.input_matricula.setCompleter(completer)

    def _actualizar_autocompletado_matriculas(self, dni_cliente):
        self.vista.input_matricula.clear()
        self.vista.input_matricula.addItem("Seleccione una matrícula")

        matriculas = obtener_matriculas_por_cliente(dni_cliente)
        self.vista.input_matricula.addItems(matriculas)

    def _asignar_numero_recepcionamiento(self):
        numero = obtener_siguiente_numero_recepcionamiento()
        self.vista.input_numero_recepcion.setText(
            str(numero).zfill(5))  # Por ejemplo 00001
        self.vista.input_numero_recepcion.setReadOnly(True)
