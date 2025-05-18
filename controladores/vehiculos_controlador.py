"""
Controlador para la gestión de vehículos en el sistema.

Este controlador conecta la vista `VentanaVehiculos` con los modelos de datos,
permitiendo:

- Buscar, crear, modificar y eliminar vehículos.
- Buscar clientes por nombre o DNI.
- Crear nuevos clientes desde un diálogo si no existen.
- Autocompletar campos con datos existentes.
- Validar formularios antes de realizar operaciones.
- Gestionar interacciones entre vehículos y clientes.
"""
from PySide6.QtCore import QObject, Qt, QEvent
from PySide6.QtWidgets import QMessageBox, QCompleter
from vistas.ventana_vehiculos import VentanaVehiculos
from modelos.vehiculos_consultas import (
    buscar_vehiculo_por_matricula,
    crear_vehiculo,
    modificar_vehiculo,
    eliminar_vehiculo,
    obtener_categorias,
    obtener_tipos_por_categoria,
    obtener_matriculas_existentes,
    obtener_combustibles,
)
from modelos.clientes_consultas import obtener_cliente_por_id, obtener_clientes
from controladores.crear_cliente_rapido_controlador import CrearClienteRapidoControlador


class VehiculosControlador(QObject):
    """
    Clase que controla la ventana de gestión de vehículos.

    Permite realizar búsquedas por matrícula, nombre o DNI, así como registrar,
    modificar o eliminar vehículos asociados a un cliente. También permite crear
    clientes rápidamente si no existen.

    Métodos clave:
        - buscar_vehiculo
        - guardar_vehiculo
        - modificar_vehiculo
        - eliminar_vehiculo
        - crear_cliente_dialogo
    """

    def __init__(self, ventana_anterior):
        """
        Inicializa el controlador cargando la vista, los datos de clientes,
        categorías, combustibles, y conectando eventos.

        Args:
            ventana_anterior: Referencia a la ventana desde la que se abrió esta.
        """
        super().__init__()
        self.ventana = VentanaVehiculos()
        self.ventana_anterior = ventana_anterior
        self.vehiculo_id_actual = None
        self.cliente_id_actual = None

        # Obtener y mapear clientes
        self.lista_clientes = obtener_clientes()
        self.clientes_dict_nombre = {
            f"{c['nombre']} {c['primer_apellido']} {c.get('segundo_apellido', '')}".strip().upper(): c["id"]
            for c in self.lista_clientes
        }
        self.clientes_dict_dni = {
            c["dni"].upper(): c["id"] for c in self.lista_clientes
        }

        # Autocompletado
        completer_nombre = QCompleter(list(self.clientes_dict_nombre.keys()))
        completer_nombre.setCaseSensitivity(Qt.CaseInsensitive)
        self.ventana.input_buscar_nombre.setCompleter(completer_nombre)

        completer_dni = QCompleter(list(self.clientes_dict_dni.keys()))
        completer_dni.setCaseSensitivity(Qt.CaseInsensitive)
        self.ventana.input_buscar_dni.setCompleter(completer_dni)

        # Autocompletado rápido para matrículas
        self.lista_matriculas = obtener_matriculas_existentes()
        completer_matriculas = QCompleter(self.lista_matriculas)
        completer_matriculas.setCaseSensitivity(Qt.CaseInsensitive)
        self.ventana.input_buscar_matricula.setCompleter(completer_matriculas)

        # Conexiones
        self.ventana.input_buscar_matricula.setObjectName(
            "input_buscar_matricula")
        self.ventana.input_buscar_matricula.returnPressed.connect(
            self.buscar_vehiculo_desde_input)
        self.ventana.input_buscar_nombre.installEventFilter(self)
        self.ventana.input_buscar_dni.installEventFilter(self)

        self.ventana.boton_guardar.clicked.connect(self.guardar_vehiculo)
        self.ventana.boton_modificar.clicked.connect(self.modificar_vehiculo)
        self.ventana.boton_eliminar.clicked.connect(self.eliminar_vehiculo)
        self.ventana.boton_volver.clicked.connect(self.volver)
        self.ventana.boton_limpiar.clicked.connect(self.limpiar_campos)

        self.ventana.boton_modificar.setEnabled(False)
        self.ventana.boton_eliminar.setEnabled(False)

        self.ventana.combo_tipo.setEnabled(False)
        self.ventana.combo_categoria.currentIndexChanged.connect(
            self.actualizar_tipos_por_categoria)

        categorias = obtener_categorias()
        self.ventana.combo_categoria.addItems(categorias)

        # Cargar combustibles
        self.lista_combustibles = obtener_combustibles()
        self.ventana.combo_combustible.addItem("Selecciona combustible", -1)
        for combustible in self.lista_combustibles:
            self.ventana.combo_combustible.addItem(
                combustible["nombre"], combustible["id"])

        self.ventana.show()

    def eventFilter(self, source, event):
        """
        Captura eventos de teclado para autocompletar clientes al pulsar Enter.

        Args:
            source: Campo de texto que origina el evento.
            event (QEvent): Evento recibido.

        Returns:
            bool: True si el evento fue manejado, False en caso contrario.
        """
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if source == self.ventana.input_buscar_nombre:
                    self.buscar_cliente_por_nombre()
                    return True
                elif source == self.ventana.input_buscar_dni:
                    self.buscar_cliente_por_dni()
                    return True
        return super().eventFilter(source, event)

    def buscar_vehiculo_desde_input(self):
        """
        Llama a `buscar_vehiculo` usando el texto introducido en el campo de matrícula.
        """
        matricula = self.ventana.input_buscar_matricula.text().strip().upper()
        self.buscar_vehiculo(matricula)

    def buscar_cliente_por_nombre(self):
        """
        Busca un cliente por nombre completo. Si no se encuentra, ofrece crearlo.
        """
        texto = self.ventana.input_buscar_nombre.text().strip().upper()
        if texto in self.clientes_dict_nombre:
            cliente_id = self.clientes_dict_nombre[texto]
            cliente = obtener_cliente_por_id(cliente_id)
            if cliente:
                self.cliente_id_actual = cliente_id
                self.rellenar_datos_cliente(cliente)
        else:
            self.crear_cliente_dialogo(self.ventana.input_buscar_nombre)

    def buscar_cliente_por_dni(self):
        """
        Busca un cliente por su DNI. Si no se encuentra, ofrece crearlo.
        """
        dni = self.ventana.input_buscar_dni.text().strip().upper()
        if dni in self.clientes_dict_dni:
            cliente_id = self.clientes_dict_dni[dni]
            cliente = obtener_cliente_por_id(cliente_id)
            if cliente:
                self.cliente_id_actual = cliente_id
                self.rellenar_datos_cliente(cliente)
        else:
            self.crear_cliente_dialogo(self.ventana.input_buscar_dni)

    def rellenar_datos_cliente(self, cliente):
        """
        Rellena los campos de cliente en la vista con los datos proporcionados.

        Args:
            cliente (dict): Diccionario con los datos del cliente.
        """
        self.ventana.input_nombre.setText(cliente["nombre"])
        self.ventana.input_apellido1.setText(cliente["primer_apellido"])
        self.ventana.input_apellido2.setText(
            cliente.get("segundo_apellido", ""))
        self.ventana.input_dni.setText(cliente["dni"])
        self.ventana.input_telefono.setText(cliente["telefono"] or "")
        self.ventana.input_email.setText(cliente["email"] or "")
        self.ventana.input_direccion.setText(cliente["direccion"] or "")
        self.ventana.input_cp.setText(cliente["codigo_postal"] or "")
        self.ventana.input_localidad.setText(cliente["localidad"] or "")
        self.ventana.input_provincia.setText(cliente["provincia"] or "")

    def crear_cliente_dialogo(self, campo_foco):
        """
        Muestra un diálogo para crear un cliente si no existe.

        Args:
            campo_foco: Campo que recupera el foco si se cancela la creación.
        """
        respuesta = QMessageBox.question(
            self.ventana,
            "Cliente no encontrado",
            "No se encontró ese cliente. ¿Deseas crearlo?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.ventana_crear_cliente = CrearClienteRapidoControlador(
                self.ventana)
            self.ventana_crear_cliente.cliente_creado.connect(
                self.cliente_creado)
            self.ventana_crear_cliente.ventana.show()  # <- aquí está el cambio
        else:
            campo_foco.setFocus()

    def cliente_creado(self, datos_cliente):
        """
        Se ejecuta cuando un cliente es creado desde el diálogo rápido.

        Actualiza los campos visuales y los autocompletadores.

        Args:
            datos_cliente (dict): Información del nuevo cliente.
        """
        self.lista_clientes = obtener_clientes()
        self.clientes_dict_nombre = {
            f"{c['nombre']} {c['primer_apellido']} {c.get('segundo_apellido', '')}".strip().upper(): c["id"]
            for c in self.lista_clientes
        }
        self.clientes_dict_dni = {
            c["dni"].upper(): c["id"] for c in self.lista_clientes
        }

        # Actualizar completers
        completer_nombre = QCompleter(list(self.clientes_dict_nombre.keys()))
        completer_nombre.setCaseSensitivity(Qt.CaseInsensitive)
        self.ventana.input_buscar_nombre.setCompleter(completer_nombre)

        completer_dni = QCompleter(list(self.clientes_dict_dni.keys()))
        completer_dni.setCaseSensitivity(Qt.CaseInsensitive)
        self.ventana.input_buscar_dni.setCompleter(completer_dni)

        # Rellenar campos visuales
        self.ventana.input_buscar_nombre.setText(
            f"{datos_cliente['nombre']} {datos_cliente['primer_apellido']}")
        self.ventana.input_nombre.setText(datos_cliente["nombre"])
        self.ventana.input_apellido1.setText(datos_cliente["primer_apellido"])
        self.ventana.input_apellido2.setText(
            datos_cliente.get("segundo_apellido", ""))
        self.ventana.input_dni.setText(datos_cliente["dni"])
        self.ventana.input_telefono.setText(datos_cliente["telefono"])
        self.ventana.input_email.setText(datos_cliente["email"])
        self.cliente_id_actual = datos_cliente["id"]

    def buscar_vehiculo(self, matricula):
        """
        Busca un vehículo por matrícula y muestra sus datos junto con los del cliente asociado.

        Args:
            matricula (str): Matrícula del vehículo.
        """
        datos = buscar_vehiculo_por_matricula(matricula)
        if not datos:
            self.mostrar_info(
                "No se encontró ningún vehículo con esa matrícula.")
            return

        self.vehiculo_id_actual = datos["id"]
        self.cliente_id_actual = datos["cliente_id"]

        # Cliente
        cliente = obtener_cliente_por_id(datos["cliente_id"])
        if cliente:
            nombre_completo = f"{cliente['nombre']} {cliente['primer_apellido']} {cliente.get('segundo_apellido', '')}".strip(
            )
            self.ventana.input_buscar_nombre.setText(nombre_completo)
            self.rellenar_datos_cliente(cliente)

        # Vehículo
        self.ventana.input_matricula.setText(datos["matricula"])
        self.ventana.input_marca.setText(datos["marca"])
        self.ventana.input_modelo.setText(datos["modelo"])
        self.ventana.input_color.setText(datos["color"])
        self.ventana.input_anyo.setText(str(datos["anyo"]))
        self.ventana.input_observaciones.setPlainText(
            datos["observaciones"] or "")

        self.ventana.input_numero_bastidor.setText(
            datos["numero_bastidor"] or "")

        # Seleccionar combustible
        index_combustible = self.ventana.combo_combustible.findData(
            datos["combustible_id"])
        if index_combustible != -1:
            self.ventana.combo_combustible.setCurrentIndex(index_combustible)
        else:
            self.ventana.combo_combustible.setCurrentIndex(0)

        # Seleccionar categoría
        indice_categoria = self.ventana.combo_categoria.findText(
            datos["categoria"], Qt.MatchFixedString
        )
        if indice_categoria >= 0:
            self.ventana.combo_categoria.setCurrentIndex(indice_categoria)

            # ⬇️ Actualiza combo de tipo antes de seleccionar
            self.actualizar_tipos_por_categoria()

            # 🟦 Seleccionar tipo
            indice_tipo = self.ventana.combo_tipo.findText(
                datos["tipo_nombre"], Qt.MatchFixedString
            )
            if indice_tipo >= 0:
                self.ventana.combo_tipo.setCurrentIndex(indice_tipo)

        self.ventana.boton_modificar.setEnabled(True)
        self.ventana.boton_eliminar.setEnabled(True)

    def guardar_vehiculo(self):
        """
        Guarda un nuevo vehículo si los datos son válidos.
        Actualiza autocompletado de matrículas.
        """
        if not self.obtener_datos_y_validar():
            return

        exito = crear_vehiculo(
            self.matricula, self.marca, self.modelo, self.color,
            self.tipo, self.cliente_id_actual,
            self.numero_bastidor, self.combustible_id, self.anio,
            self.observaciones
        )

        if exito:
            self.mostrar_info("Vehículo registrado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("No se pudo registrar el vehículo.")

        self.lista_matriculas = obtener_matriculas_existentes()
        self.ventana.input_buscar_matricula.setCompleter(
            QCompleter(self.lista_matriculas))

    def modificar_vehiculo(self):
        """
        Modifica un vehículo existente si ha sido previamente cargado y los datos son válidos.
        """
        if not self.vehiculo_id_actual:
            self.mostrar_error("Primero debes buscar un vehículo.")
            return

        if not self.obtener_datos_y_validar():
            return

        exito = modificar_vehiculo(
            self.vehiculo_id_actual,
            self.matricula, self.marca, self.modelo, self.color,
            self.tipo, self.cliente_id_actual,
            self.numero_bastidor, self.combustible_id, self.anio,
            self.observaciones
        )

        if exito:
            self.mostrar_info("Vehículo modificado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("No se pudo modificar el vehículo.")

        self.lista_matriculas = obtener_matriculas_existentes()
        self.ventana.input_buscar_matricula.setCompleter(
            QCompleter(self.lista_matriculas))

    def eliminar_vehiculo(self):
        """
        Elimina el vehículo actualmente cargado tras confirmación del usuario.
        """
        if not self.vehiculo_id_actual:
            self.mostrar_error("Primero debes buscar un vehículo.")
            return

        confirmar = QMessageBox.question(
            self.ventana, "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar este vehículo?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            exito = eliminar_vehiculo(self.vehiculo_id_actual)
            if exito:
                self.mostrar_info("Vehículo eliminado correctamente.")
                self.limpiar_campos()
            else:
                self.mostrar_error("No se pudo eliminar el vehículo.")

    def obtener_datos_y_validar(self):
        """
        Extrae y valida los datos introducidos en el formulario.

        Returns:
            bool: True si todos los campos obligatorios son válidos, False en caso contrario.
        """
        nombre_cliente = self.ventana.input_buscar_nombre.text().strip().upper()
        self.matricula = self.ventana.input_matricula.text().strip().upper()
        self.marca = self.ventana.input_marca.text().strip()
        self.modelo = self.ventana.input_modelo.text().strip()
        self.color = self.ventana.input_color.text().strip()
        self.anio = self.ventana.input_anyo.text().strip()
        self.tipo = self.ventana.combo_tipo.currentIndex()
        self.numero_bastidor = self.ventana.input_numero_bastidor.text().strip().upper()
        self.combustible_id = self.ventana.combo_combustible.currentData()
        self.observaciones = self.ventana.input_observaciones.toPlainText().strip()

        if not nombre_cliente or nombre_cliente not in self.clientes_dict_nombre:
            self.mostrar_error("Debes seleccionar un cliente válido.")
            return False

        self.cliente_id_actual = self.clientes_dict_nombre[nombre_cliente]

        if not self.matricula or not self.marca or not self.modelo:
            self.mostrar_error("Matrícula, marca y modelo son obligatorios.")
            return False

        if not self.numero_bastidor:
            self.mostrar_error("El número de bastidor es obligatorio.")
            return False

        if self.combustible_id == -1:
            self.mostrar_error("Debes seleccionar un tipo de combustible.")
            return False

        if self.tipo <= 0:
            self.mostrar_error("Debes seleccionar un tipo de vehículo.")
            return False

        return True

    def limpiar_campos(self):
        """
        Limpia todos los campos de la interfaz, reseteando el estado del formulario.
        """
        self.vehiculo_id_actual = None
        self.cliente_id_actual = None
        self.ventana.input_buscar_matricula.clear()
        self.ventana.input_buscar_nombre.clear()
        self.ventana.input_buscar_dni.clear()

        self.ventana.input_nombre.clear()
        self.ventana.input_apellido1.clear()
        self.ventana.input_apellido2.clear()
        self.ventana.input_dni.clear()
        self.ventana.input_telefono.clear()
        self.ventana.input_email.clear()
        self.ventana.input_direccion.clear()
        self.ventana.input_cp.clear()
        self.ventana.input_localidad.clear()
        self.ventana.input_provincia.clear()

        self.ventana.input_matricula.clear()
        self.ventana.input_marca.clear()
        self.ventana.input_modelo.clear()
        self.ventana.input_color.clear()
        self.ventana.input_anyo.clear()
        self.ventana.combo_tipo.setCurrentIndex(0)
        self.ventana.input_observaciones.clear()

        self.ventana.boton_modificar.setEnabled(False)
        self.ventana.input_numero_bastidor.clear()
        self.ventana.combo_combustible.setCurrentIndex(0)
        self.ventana.boton_eliminar.setEnabled(False)

    def volver(self):
        """
        Cierra esta ventana y vuelve a la anterior.
        """
        self.ventana.deleteLater()
        self.ventana_anterior.show()

    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error.

        Args:
            mensaje (str): Texto del mensaje a mostrar.
        """
        QMessageBox.critical(self.ventana, "Error", mensaje)

    def mostrar_info(self, mensaje):
        """
        Muestra un mensaje informativo.

        Args:
            mensaje (str): Texto del mensaje a mostrar.
        """
        QMessageBox.information(self.ventana, "Información", mensaje)

    def actualizar_tipos_por_categoria(self):
        """
        Carga los tipos de vehículo correspondientes a la categoría seleccionada.
        """
        categoria = self.ventana.combo_categoria.currentText()
        if categoria != "Selecciona categoría":
            tipos = obtener_tipos_por_categoria(categoria)
            self.ventana.combo_tipo.clear()
            self.ventana.combo_tipo.addItem("Selecciona tipo de vehículo")
            self.ventana.combo_tipo.addItems(tipos)
            self.ventana.combo_tipo.setEnabled(True)
        else:
            self.ventana.combo_tipo.setEnabled(False)
            self.ventana.combo_tipo.clear()
            self.ventana.combo_tipo.addItem("Selecciona tipo de vehículo")
