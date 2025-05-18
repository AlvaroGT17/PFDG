"""
Controlador de la ventana de Recepcionamiento de vehículos en taller.

Este módulo gestiona:
- Autocompletado de clientes y vehículos.
- Generación del documento PDF con los datos del formulario.
- Inserción de datos en la base de datos.
- Envío opcional del documento por correo.
- Impresión directa si se selecciona.

Utiliza:
- `vistas.ventana_recepcionamiento`: Interfaz gráfica.
- `utilidades.recepcionamiento_utilidades`: Utilidades para validación y generación de documentos.
- `modelos.recepcionamiento_consultas`: Acceso a la base de datos.
"""
import os
import smtplib
import subprocess
import platform
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QCompleter
from utilidades.correo_recepcionamiento import enviar_correo_con_pdf
from utilidades.recepcionamiento_utilidades import validar_correo, generar_documento_pdf
from modelos.clientes_consultas import obtener_clientes
from utilidades.rutas_guardado import obtener_ruta_predeterminada_recepcionamientos
from modelos.recepcionamiento_consultas import (
    obtener_matriculas_existentes,
    obtener_siguiente_numero_recepcionamiento,
    obtener_datos_vehiculo_por_matricula,
    obtener_matriculas_por_cliente,
)
from modelos.recepcionamiento_consultas import (
    obtener_cliente_id_por_dni,
    obtener_vehiculo_id_por_matricula,
    obtener_estado_id_por_defecto,
    insertar_recepcionamiento_en_bd,
)


class RecepcionamientoControlador:
    """
    Controlador principal del formulario de recepcionamiento de vehículos.

    Se encarga de:
    - Inicializar la interfaz.
    - Cargar datos y configurar autocompletado.
    - Conectar eventos de la GUI.
    - Validar y guardar información.
    - Generar documentos PDF.
    - Gestionar el envío por correo e impresión.
    """

    def __init__(self, vista, datos):
        """
        Inicializa el controlador.

        Args:
            vista: Instancia de la ventana `VentanaRecepcionamiento`.
            datos: Diccionario con datos iniciales (motivos, urgencias, tipos, etc.).
        """
        self.vista = vista
        self.datos = datos
        self._conectar_eventos()
        self._cargar_datos_completos()
        self._configurar_autocompletado_clientes()
        self._configurar_autocompletado_matricula()
        self._activar_ruta_predeterminada()
        self._asignar_numero_recepcionamiento()

    def _conectar_eventos(self):
        """
        Conecta los eventos de la interfaz gráfica a los métodos del controlador.
        Incluye acciones para botones y cambios en los combos.
        """
        self.vista.boton_confirmar.clicked.connect(
            self.confirmar_recepcionamiento)
        self.vista.boton_cancelar.clicked.connect(self.vista.close)
        self.vista.input_matricula.currentTextChanged.connect(
            self._autocompletar_datos_vehiculo)
        self.vista.combo_categoria.currentTextChanged.connect(
            self._filtrar_tipos_por_categoria)

    def confirmar_recepcionamiento(self):
        """
        Procesa los datos introducidos por el usuario cuando pulsa "Confirmar".

        - Valida el formulario.
        - Genera el documento PDF.
        - Guarda la información en base de datos.
        - Envia el correo con el documento adjunto si está marcado.
        - Imprime automáticamente si el checkbox está activado.
        """
        datos = self._recopilar_datos()

        # Cliente
        print("🪪 DNI introducido por el usuario:", datos["DNI"])
        cliente_id = obtener_cliente_id_por_dni(datos["DNI"])
        print("👤 ID del cliente obtenido en base de datos:", cliente_id)

        # Usuario
        print("👨‍💻 ID del usuario (empleado) actual:",
              self.datos.get("usuario_id"))

        # Estado
        estado_id = obtener_estado_id_por_defecto()
        print("📥 ID del estado por defecto (Pendiente):", estado_id)

        # Motivo
        print(f"📝 Motivo seleccionado en el formulario:", datos["Motivo"])
        print(f"🆔 ID correspondiente del motivo:",
              self.motivos_dict.get(datos["Motivo"]))

        # Obtener correos
        correo_destino = self.vista.input_correo.text().strip()
        correo_cliente = datos["Email"].strip()

        correo_final = None

        if self.vista.checkbox_enviar_correo.isChecked():
            # Caso 1: el usuario no ha rellenado 'Correo destino'
            if not correo_destino:
                if correo_cliente:
                    correo_final = correo_cliente  # usamos el del cliente
                else:
                    QMessageBox.warning(
                        self.vista,
                        "Correo no disponible",
                        "No se ha especificado ningún correo para enviar el documento.\n"
                        "Rellena el campo 'Correo destino' o asegúrate de que el cliente tiene un correo registrado."
                    )
                    return
            else:
                # Si ha puesto uno en destino, lo usamos aunque el cliente tenga uno diferente
                correo_final = correo_destino

            # Validación del correo final
            if not validar_correo(correo_final):
                QMessageBox.warning(
                    self.vista,
                    "Correo inválido",
                    f"El correo '{correo_final}' no es válido. Corrige el campo antes de continuar."
                )
                return

            # lo añadimos a los datos para usarlo luego
            datos["Correo destino"] = correo_final

        # Obtener firma del cliente
        firma_pixmap = self.vista.zona_firma.obtener_firma()
        ruta_firma = "firma_temporal.png"
        firma_pixmap.save(ruta_firma, "PNG")

        # Ruta de guardado
        ruta_guardado = self.vista.input_ruta_guardado.text().strip()
        if not ruta_guardado:
            QMessageBox.warning(self.vista, "Ruta no válida",
                                "Debe especificar una ruta de guardado válida.")
            return

        # Generar PDF
        ruta_pdf = generar_documento_pdf(datos, ruta_firma, ruta_guardado)

        # Mostrar mensaje
        QMessageBox.information(
            self.vista, "Recepcionamiento generado", f"Documento generado:\n{ruta_pdf}"
        )

        # Guardar en la base de datos
        cliente_id = obtener_cliente_id_por_dni(datos["DNI"])
        vehiculo_id = obtener_vehiculo_id_por_matricula(datos["Matrícula"])
        estado_id = obtener_estado_id_por_defecto()
        # ← Asegúrate de tenerlo al instanciar
        usuario_id = self.datos.get("usuario_id")

        try:
            datos["UltimaRevision"] = datetime.strptime(
                datos["UltimaRevision"], "%d/%m/%Y").date()
        except Exception as e:
            datos["UltimaRevision"] = None  # o mostrar un mensaje si prefieres

        datos_bd = {
            "cliente_id": cliente_id,
            "usuario_id": usuario_id,
            "vehiculo_id": vehiculo_id,
            "estado_id": estado_id,
            "motivo_id": self.motivos_dict.get(datos["Motivo"]),
            "arranca": datos["Arranca"] == "Sí",
            "grua": datos["Grúa"] == "Sí",
            "seguro": datos["Seguro"] == "Sí",
            "compania_seguro": datos["SeguroCompania"],
            "valor_estimado": datos["ValorEstimado"],
            "presupuesto": datos["Presupuesto"] == "Sí",
            "itv": datos["ITV"] == "Sí",
            "ultima_revision": datos["UltimaRevision"],
            "desea_presupuesto": datos["Presupuesto"] == "Sí",
            "reparacion_hasta": datos["ReparacionHasta"],
            "estado_exterior": datos["EstadoExterior"],
            "estado_interior": datos["EstadoInterior"],
            "observaciones": datos["Observaciones"],
            "enviar_correo": "Correo destino" in datos,
            "entregar_impreso": False,  # luego puedes añadir un checkbox
            "ruta_pdf": ruta_pdf,
            "numero_recepcionamiento": datos["NúmeroRecepcion"],
            "urgencia_id": self.urgencias_dict.get(datos["Urgencia"]),
        }

        exito, error = insertar_recepcionamiento_en_bd(datos_bd)
        if not exito:
            QMessageBox.critical(
                self.vista,
                "Error al guardar",
                f"No se pudo guardar el recepcionamiento en la base de datos.\n\nDetalle: {error}"
            )
            return

        # Enviar por correo si está activado
        if self.vista.checkbox_enviar_correo.isChecked():
            exito, error = enviar_correo_con_pdf(correo_final, ruta_pdf, datos)
            if not exito:
                QMessageBox.critical(
                    self.vista,
                    "Error al enviar el correo",
                    f"No se pudo enviar el documento por correo.\n\nDetalle del error:\n{error}"
                )
            else:
                QMessageBox.information(
                    self.vista,
                    "Correo enviado",
                    f"El documento se ha enviado correctamente a:\n{correo_final}"
                )

        # Imprimir si está activado
        if self.vista.checkbox_imprimir.isChecked():
            try:
                if platform.system() == "Windows":
                    os.startfile(ruta_pdf, "print")
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["lp", ruta_pdf], check=True)
                else:  # Linux
                    subprocess.run(["lpr", ruta_pdf], check=True)
            except Exception as e:
                QMessageBox.critical(
                    self.vista,
                    "Error al imprimir",
                    f"No se pudo enviar el documento a la impresora predeterminada.\n\nDetalle del error:\n{str(e)}"
                )

        self.vista.close()

    def _cargar_datos_completos(self):
        """
        Carga los datos iniciales proporcionados al controlador
        en los combos de la interfaz (categorías, tipos, motivos, urgencias, combustibles).
        """
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
        """
        Recoge todos los valores del formulario y los empaqueta en un diccionario.

        Returns:
            dict: Datos recopilados del cliente, vehículo y estado del formulario.
        """
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
            "NúmeroRecepcion": self.vista.input_numero_recepcion.text(),

        }

    def _configurar_autocompletado_clientes(self):
        """
        Configura los autocompletadores para los campos de nombre y DNI del cliente,
        utilizando los clientes registrados en la base de datos.
        """
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
        """
        Busca coincidencias exactas por nombre completo del cliente
        e invoca el rellenado automático de campos si se encuentra uno.
        """
        texto = self.vista.input_nombre.text().strip().upper()
        cliente = next((c for c in self.datos_clientes
                        if f"{c['nombre']} {c['primer_apellido']} {c['segundo_apellido']}".strip().upper() == texto),
                       None)
        if cliente:
            self._rellenar_campos_cliente(cliente)

    def _autocompletar_por_dni(self):
        """
        Busca coincidencias exactas por DNI del cliente e invoca
        el rellenado automático si se encuentra un cliente válido.
        """
        texto = self.vista.input_dni.text().strip().upper()
        cliente = next(
            (c for c in self.datos_clientes if c['dni'].upper() == texto), None)
        if cliente:
            self._rellenar_campos_cliente(cliente)

    def _rellenar_campos_cliente(self, cliente):
        """
        Llena automáticamente los campos del formulario con los datos del cliente seleccionado.

        Args:
            cliente (dict): Diccionario con los datos del cliente.
        """
        self.vista.input_nombre.setText(
            f"{cliente['nombre']} {cliente['primer_apellido']} {cliente['segundo_apellido']}".strip())
        self.vista.input_dni.setText(cliente['dni'])
        self.vista.input_telefono.setText(cliente['telefono'] or "")
        self.vista.input_email.setText(cliente['email'] or "")
        self.vista.input_direccion.setText(cliente['direccion'] or "")
        self._actualizar_autocompletado_matriculas(cliente['dni'])

    def _autocompletar_datos_vehiculo(self, matricula=None):
        """
        Rellena automáticamente los campos del vehículo al seleccionar una matrícula conocida.

        Args:
            matricula (str, optional): Matrícula del vehículo. Si no se proporciona,
                                      se toma del combo correspondiente.
        """
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
        """
        Filtra y muestra los tipos de vehículo disponibles según la categoría seleccionada.
        """
        categoria_seleccionada = self.vista.combo_categoria.currentText()
        self.vista.combo_tipo.clear()
        self.vista.combo_tipo.addItem("Seleccione el tipo")
        tipos_filtrados = [tipo['nombre']
                           for tipo in self.tipos_vehiculos if tipo['categoria'] == categoria_seleccionada]
        self.vista.combo_tipo.addItems(tipos_filtrados)

    def _configurar_autocompletado_matricula(self):
        """
        Configura el autocompletado del campo de matrícula con las existentes en la base de datos.
        """
        matriculas = obtener_matriculas_existentes()
        completer = QCompleter(matriculas)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.vista.input_matricula.setCompleter(completer)

    def _actualizar_autocompletado_matriculas(self, dni_cliente):
        """
        Actualiza las opciones del combo de matrícula con las que están asociadas al cliente.

        Args:
            dni_cliente (str): DNI del cliente.
        """
        self.vista.input_matricula.clear()
        self.vista.input_matricula.addItem("Seleccione una matrícula")
        matriculas = obtener_matriculas_por_cliente(dni_cliente)
        self.vista.input_matricula.addItems(matriculas)

    def _asignar_numero_recepcionamiento(self):
        """
        Asigna el número de recepcionamiento siguiente disponible y lo muestra en el campo correspondiente.
        """
        numero = obtener_siguiente_numero_recepcionamiento()
        self.vista.input_numero_recepcion.setText(str(numero).zfill(5))
        self.vista.input_numero_recepcion.setReadOnly(True)

    def _activar_ruta_predeterminada(self):
        """
        Activa el uso de la ruta de guardado predeterminada si el checkbox correspondiente está activo.
        Conecta el evento `toggled` al método manejador.
        """
        if self.vista.checkbox_ruta_predeterminada.isChecked():
            ruta = obtener_ruta_predeterminada_recepcionamientos()
            self.vista.input_ruta_guardado.setText(ruta)

        self.vista.checkbox_ruta_predeterminada.toggled.connect(
            self._manejar_checkbox_ruta)

    def _manejar_checkbox_ruta(self, estado):
        """
        Activa o desactiva el campo de ruta manual según el estado del checkbox.

        Args:
            estado (bool): Estado del checkbox (True si está activado).
        """
        if estado:
            ruta = obtener_ruta_predeterminada_recepcionamientos()
            self.vista.input_ruta_guardado.setText(ruta)
            self.vista.input_ruta_guardado.setDisabled(True)
            self.vista.boton_buscar_ruta.setDisabled(True)
        else:
            self.vista.input_ruta_guardado.clear()
            self.vista.input_ruta_guardado.setDisabled(False)
            self.vista.boton_buscar_ruta.setDisabled(False)
