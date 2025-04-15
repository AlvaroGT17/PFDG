from PySide6.QtWidgets import QMessageBox, QCompleter
from PySide6.QtCore import Qt
from utilidades.recepcionamiento_utilidades import validar_correo, generar_documento_pdf
from modelos.clientes_consultas import obtener_clientes
from utilidades.rutas_guardado import obtener_ruta_predeterminada_recepcionamientos
from modelos.recepcionamiento_consultas import (
    obtener_matriculas_existentes,
    obtener_siguiente_numero_recepcionamiento,
    obtener_datos_vehiculo_por_matricula,
    obtener_matriculas_por_cliente,
)


class RecepcionamientoControlador:
    def __init__(self, vista, datos):
        self.vista = vista
        self.datos = datos
        self._conectar_eventos()
        self._cargar_datos_completos()
        self._configurar_autocompletado_clientes()
        self._configurar_autocompletado_matricula()
        self._asignar_numero_recepcionamiento()
        self._activar_ruta_predeterminada()

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

        firma_pixmap = self.vista.zona_firma.obtener_firma()
        ruta_firma = "firma_temporal.png"
        firma_pixmap.save(ruta_firma, "PNG")

        ruta_guardado = self.vista.input_ruta_guardado.text().strip()
        if not ruta_guardado:
            QMessageBox.warning(self.vista, "Ruta no válida",
                                "Debe especificar una ruta de guardado válida.")
            return

        ruta_pdf = generar_documento_pdf(datos, ruta_firma, ruta_guardado)

        QMessageBox.information(
            self.vista, "Recepcionamiento generado", f"Documento generado:\n{ruta_pdf}")
        self.vista.close()

    def _cargar_datos_completos(self):
        self.tipos_vehiculos = self.datos.get("tipos", [])

        self.vista.combo_categoria.clear()
        self.vista.combo_categoria.addItem("Seleccione la categoría")
        self.vista.combo_categoria.addItems(self.datos.get("categorias", []))

        self.vista.combo_tipo.clear()
        self.vista.combo_tipo.addItem("Seleccione el tipo")

        self.vista.combo_combustible.clear()
        self.vista.combo_combustible.addItem("Seleccione el combustible")
        self.vista.combo_combustible.addItems(
            self.datos.get("combustibles", []))

        self.vista.combo_motivo.clear()
        self.motivos_dict = {}
        for item in self.datos.get("motivos", []):
            self.vista.combo_motivo.addItem(item["nombre"])
            self.motivos_dict[item["nombre"]] = item["id"]

        self.vista.combo_urgencia.clear()
        self.urgencias_dict = {}
        for item in self.datos.get("urgencias", []):
            self.vista.combo_urgencia.addItem(item["descripcion"])
            self.urgencias_dict[item["descripcion"]] = item["id"]

    def _recopilar_datos(self):
        return {
            # Datos del cliente
            "Nombre": self.vista.input_nombre.text(),
            "DNI": self.vista.input_dni.text(),
            "Teléfono": self.vista.input_telefono.text(),
            "Email": self.vista.input_email.text(),
            "Dirección": self.vista.input_direccion.text(),

            # Datos del vehículo
            "Matrícula": self.vista.input_matricula.currentText(),
            "Marca": self.vista.input_marca.text(),
            "Modelo": self.vista.input_modelo.text(),
            "Color": self.vista.input_color.text(),
            "Año": self.vista.input_anio.text(),
            "Kilómetros": self.vista.input_kilometros.text(),
            "Combustible": self.vista.combo_combustible.currentText(),
            "VIN": self.vista.input_vin.text(),
            "Tipo de vehículo": self.vista.combo_tipo.currentText(),

            # Motivo de recepción
            "Motivo": self.vista.combo_motivo.currentText(),
            "Urgencia": self.vista.combo_urgencia.currentText(),
            "FechaRecepcion": self.vista.fecha_recepcion.text(),

            "Arranca": "Sí" if self.vista.check_arranca.isChecked() else "No",
            "Grúa": "Sí" if self.vista.check_grua.isChecked() else "No",
            "ITV": "Sí" if self.vista.check_itv.isChecked() else "No",
            "Presupuesto": "Sí" if self.vista.check_presupuesto_escrito.isChecked() else "No",

            "Seguro": "Sí" if self.vista.check_seguro.isChecked() else "No",
            "SeguroCompania": self.vista.input_compania.text(),

            "UltimaRevision": self.vista.input_ultima_revision.text(),
            "ReparacionHasta": self.vista.input_max_autorizado.text(),
            "ValorEstimado": self.vista.input_valor_estimado.text(),

            "EstadoExterior": self.vista.input_estado_exterior.toPlainText(),
            "EstadoInterior": self.vista.input_estado_interior.toPlainText(),
            "Observaciones": self.vista.input_observaciones.toPlainText(),

            # Número de recepción para el nombre del archivo
            "NumeroRecepcion": self.vista.input_numero_recepcion.text(),
        }

    def _configurar_autocompletado_clientes(self):
        self.datos_clientes = obtener_clientes()

        nombres = [f"{c['nombre']} {c['primer_apellido']} {c['segundo_apellido']}".strip()
                   for c in self.datos_clientes]
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
        cliente = next((c for c in self.datos_clientes
                        if f"{c['nombre']} {c['primer_apellido']} {c['segundo_apellido']}".strip().upper() == texto),
                       None)
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

    def _filtrar_tipos_por_categoria(self):
        categoria_seleccionada = self.vista.combo_categoria.currentText()
        self.vista.combo_tipo.clear()
        self.vista.combo_tipo.addItem("Seleccione el tipo")
        tipos_filtrados = [tipo['nombre']
                           for tipo in self.tipos_vehiculos if tipo['categoria'] == categoria_seleccionada]
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
        self.vista.input_numero_recepcion.setText(str(numero).zfill(5))
        self.vista.input_numero_recepcion.setReadOnly(True)

    def _activar_ruta_predeterminada(self):
        if self.vista.checkbox_ruta_predeterminada.isChecked():
            ruta = obtener_ruta_predeterminada_recepcionamientos()
            self.vista.input_ruta_guardado.setText(ruta)

        self.vista.checkbox_ruta_predeterminada.toggled.connect(
            self._manejar_checkbox_ruta)

    def _manejar_checkbox_ruta(self, estado):
        if estado:
            ruta = obtener_ruta_predeterminada_recepcionamientos()
            self.vista.input_ruta_guardado.setText(ruta)
            self.vista.input_ruta_guardado.setDisabled(True)
            self.vista.boton_buscar_ruta.setDisabled(True)
        else:
            self.vista.input_ruta_guardado.clear()
            self.vista.input_ruta_guardado.setDisabled(False)
            self.vista.boton_buscar_ruta.setDisabled(False)
