from PySide6.QtWidgets import QMessageBox, QCompleter, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt
from vistas.ventana_nuevoCliente_compraventas import VentanaNuevoClienteCompraventas
from modelos.conexion_bd import obtener_conexion
from utilidades.mensajes import mostrar_mensaje_personalizado
from modelos.nuevoCliente_compraventa_consulta import (
    obtener_datos_cliente_por_nombre,
    obtener_cliente_por_id,
    crear_cliente_y_devolver_id,
    dni_ya_existe,
    obtener_cliente_por_id_por_dni
)
from utilidades.rutas import (
    obtener_ruta_predeterminada_compras,
    obtener_ruta_predeterminada_ventas
)
import os


class CompraventaControlador:
    def __init__(self, vista):
        self.vista = vista
        self.cliente_id = None

        # Conectar autocompletado
        self.vista.cliente_nombre.editingFinished.connect(
            self.buscar_cliente_por_nombre)
        self.vista.cliente_dni.editingFinished.connect(
            self.comprobar_dni_manualmente)
        self.inicializar_autocompletado_nombre()
        self.inicializar_autocompletado_dni()

    def inicializar_autocompletado_nombre(self):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT UPPER(nombre || ' ' || primer_apellido || ' ' || segundo_apellido)
                FROM clientes
            """)
            nombres = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"❌ Error al cargar nombres para autocompletado: {e}")
            nombres = []

        completer_nombre = QCompleter(nombres)
        completer_nombre.setCaseSensitivity(Qt.CaseInsensitive)
        completer_nombre.setFilterMode(Qt.MatchContains)
        completer_nombre.activated.connect(
            lambda texto: self.autocompletar_por_nombre(texto))
        self.vista.cliente_nombre.setCompleter(completer_nombre)

    def inicializar_autocompletado_dni(self):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT UPPER(dni) FROM clientes")
            dnis = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"❌ Error al cargar DNIs para autocompletado: {e}")
            dnis = []

        completer_dni = QCompleter(dnis)
        completer_dni.setCaseSensitivity(Qt.CaseInsensitive)
        completer_dni.setFilterMode(Qt.MatchContains)
        completer_dni.activated.connect(
            lambda texto: self.autocompletar_por_dni(texto))
        self.vista.cliente_dni.setCompleter(completer_dni)

    def buscar_cliente_por_nombre(self):
        nombre_completo = self.vista.cliente_nombre.text().strip().upper()
        if not nombre_completo:
            return

        cliente = obtener_datos_cliente_por_nombre(nombre_completo)

        if cliente:
            self.rellenar_datos_cliente(cliente)
            self.cliente_id = cliente[0]
        else:
            respuesta = QMessageBox.question(
                self.vista,
                "Cliente no encontrado",
                "No se ha encontrado un cliente con ese nombre.\n\n¿Deseas crear uno nuevo?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.abrir_ventana_nuevo_cliente(nombre=nombre_completo)

    def comprobar_dni_manualmente(self):
        dni = self.vista.cliente_dni.text().strip().upper()
        if not dni:
            return

        if self.cliente_id:
            cliente_actual = obtener_cliente_por_id(self.cliente_id)
            if cliente_actual and cliente_actual['dni'].upper() == dni:
                return

        if not dni_ya_existe(dni):
            respuesta = mostrar_mensaje_personalizado(
                self.vista,
                "DNI no encontrado",
                "El DNI introducido no corresponde a ningún cliente existente.\n\n¿Deseas crear uno nuevo?"
            )

            if respuesta == QMessageBox.Yes:
                self.abrir_ventana_nuevo_cliente(dni=dni)

    def abrir_ventana_nuevo_cliente(self, nombre="", dni=""):
        def guardar_cliente(nuevo_id):
            cliente_nuevo = obtener_cliente_por_id(nuevo_id)
            if cliente_nuevo:
                self.cliente_id = nuevo_id
                self.rellenar_datos_cliente_dict(cliente_nuevo)
                self.inicializar_autocompletado_nombre()
                self.inicializar_autocompletado_dni()
                self.vista.cliente_nombre.setFocus()

        self.ventana_nuevo = VentanaNuevoClienteCompraventas(
            callback_guardar=guardar_cliente
        )
        self.ventana_nuevo.nombre.setText(nombre)
        self.ventana_nuevo.dni.setText(dni)
        self.ventana_nuevo.show()

    def rellenar_datos_cliente(self, cliente):
        self.vista.cliente_dni.setText(cliente[4])
        self.vista.cliente_telefono.setText(cliente[5])
        self.vista.cliente_email.setText(cliente[6])
        self.vista.cliente_direccion.setText(cliente[7])
        self.vista.cliente_localidad.setText(cliente[9])
        self.vista.cliente_provincia.setText(cliente[10])
        self.vista.cliente_observaciones.setText(cliente[11])

    def rellenar_datos_cliente_dict(self, cliente):
        self.vista.cliente_nombre.setText(
            f"{cliente['nombre']} {cliente['primer_apellido']} {cliente['segundo_apellido']}")
        self.vista.cliente_dni.setText(cliente['dni'])
        self.vista.cliente_telefono.setText(cliente['telefono'])
        self.vista.cliente_email.setText(cliente['email'])
        self.vista.cliente_direccion.setText(cliente['direccion'])
        self.vista.cliente_localidad.setText(cliente['localidad'])
        self.vista.cliente_provincia.setText(cliente['provincia'])
        self.vista.cliente_observaciones.setText(cliente['observaciones'])

    def autocompletar_por_nombre(self, texto):
        self.vista.cliente_nombre.setText(texto)
        self.buscar_cliente_por_nombre()

    def autocompletar_por_dni(self, texto):
        self.vista.cliente_dni.setText(texto)
        self.comprobar_dni_manualmente()

    def recargar_vehiculos(self):
        from modelos.compraventa_consulta import obtener_vehiculos_disponibles
        self.vista.vehiculos_disponibles = obtener_vehiculos_disponibles()
        # print(f"🔄 Vehículos cargados: {len(self.vista.vehiculos_disponibles)}")
        # for v in self.vista.vehiculos_disponibles:print(f"  - {v['marca']} {v['modelo']} ({v['estado']})")
        self.vista.vehiculos_filtrados = self.vista.vehiculos_disponibles.copy()
        self.llenar_valores_filtros()
        self.actualizar_tabla_vehiculos()

    def llenar_valores_filtros(self):
        valores = {campo: set() for campo in self.vista.filtros}
        for veh in self.vista.vehiculos_disponibles:
            for campo in valores:
                valores[campo].add(str(veh.get(campo, "")))

        rangos = {
            "kilometros": ["0-25k", "25k-50k", "50k-100k", "100k-150k", "150k+"],
            "potencia_cv": ["0-75", "75-100", "100-150", "150-200", "200+"],
            "precio_venta": ["0-5k", "5k-10k", "10k-15k", "15k-20k", "20k+"]
        }

        for campo, combo in self.vista.filtros.items():
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("Cualquiera")

            if campo in rangos:
                for rango in rangos[campo]:
                    combo.addItem(rango)
            else:
                for val in sorted(valores[campo]):
                    combo.addItem(val)

            combo.blockSignals(False)

    def actualizar_tabla_vehiculos(self):
        def coincide_rango(valor, texto_rango):
            try:
                val = float(valor)
                if texto_rango.endswith("+"):
                    return val >= float(texto_rango[:-1].replace("k", "000"))
                minimo, maximo = texto_rango.replace("k", "000").split("-")
                return float(minimo) <= val < float(maximo)
            except:
                return False

        self.vista.vehiculos_filtrados = []

        for veh in self.vista.vehiculos_disponibles:
            if veh.get("estado") not in ("DISPONIBLE", "RESERVADO"):
                continue

            incluir = True
            for campo, combo in self.vista.filtros.items():
                filtro = combo.currentText()
                if filtro == "Cualquiera":
                    continue
                valor = str(veh.get(campo, ""))

                if campo in ("kilometros", "potencia_cv", "precio_venta"):
                    if not coincide_rango(valor, filtro):
                        incluir = False
                        break
                else:
                    if filtro != valor:
                        incluir = False
                        break

            if incluir:
                self.vista.vehiculos_filtrados.append(veh)

        self.cargar_tabla_filtrada()

    def cargar_tabla_filtrada(self):
        tabla = self.vista.tabla_vehiculos
        tabla.setRowCount(len(self.vista.vehiculos_filtrados))

        for fila, vehiculo in enumerate(self.vista.vehiculos_filtrados):
            for columna, clave in enumerate(vehiculo):
                item = QTableWidgetItem(str(vehiculo[clave]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                tabla.setItem(fila, columna, item)

        tabla.verticalHeader().setVisible(False)
        tabla.setWordWrap(False)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setAlternatingRowColors(True)

    def toggle_ruta_guardado(self, estado, input_ruta, boton, tipo="compra"):
        input_ruta.setDisabled(estado)
        boton.setDisabled(estado)

        if estado:
            if tipo == "compra":
                ruta = obtener_ruta_predeterminada_compras()
            else:
                ruta = obtener_ruta_predeterminada_ventas()

            os.makedirs(ruta, exist_ok=True)
            input_ruta.setText(ruta)
        else:
            input_ruta.clear()

    def seleccionar_ruta_guardado_compra(self):
        ruta = QFileDialog.getExistingDirectory(
            self.vista, "Seleccionar carpeta de guardado")
        if ruta:
            self.vista.input_ruta_guardado_compra.setText(ruta)

    def seleccionar_ruta_guardado_venta(self):
        ruta = QFileDialog.getExistingDirectory(
            self.vista, "Seleccionar carpeta de guardado")
        if ruta:
            self.vista.input_ruta_guardado_venta.setText(ruta)

    def inicializar_datos_vehiculos(self):
        self.recargar_vehiculos()
