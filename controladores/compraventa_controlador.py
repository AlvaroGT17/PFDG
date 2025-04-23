import os
import shutil
import tempfile
import webbrowser
import base64
import pdfkit
from weasyprint import HTML
from datetime import datetime
from jinja2 import Template
from utilidades.rutas import obtener_ruta_absoluta
from PySide6.QtWidgets import QMessageBox, QCompleter, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt
from vistas.ventana_nuevoCliente_compraventas import VentanaNuevoClienteCompraventas
from modelos.conexion_bd import obtener_conexion
from utilidades.mensajes import mostrar_mensaje_personalizado
from modelos.compraventa_consulta import insertar_nuevo_vehiculo, obtener_id_cliente, registrar_venta
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion
from utilidades.correo_contratos import enviar_correo_contrato
from utilidades.imprimir import imprimir_pdf
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


class CompraventaControlador:
    def __init__(self, vista):
        self.vista = vista
        self.cliente_id = None

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
            callback_guardar=guardar_cliente)
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
        nombre_completo = " ".join(filter(None, [
            cliente.get('nombre', ''),
            cliente.get('primer_apellido', ''),
            cliente.get('segundo_apellido', '')
        ])).strip()

        self.vista.cliente_nombre.setText(nombre_completo)
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
            ruta = obtener_ruta_predeterminada_compras(
            ) if tipo == "compra" else obtener_ruta_predeterminada_ventas()
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

    def simular_contrato(self, tipo):
        if tipo == "venta":
            self.simular_contrato_venta()
        elif tipo == "compra":
            self.simular_contrato_compra()

    def simular_contrato_compra(self):
        try:
            firma_cliente_base64 = self.vista.capturador_firma.obtener_imagen_base64()

            datos_cliente = {
                "nombre_completo": self.vista.cliente_nombre.text(),
                "dni": self.vista.cliente_dni.text(),
                "direccion": self.vista.cliente_direccion.text(),
                "localidad": self.vista.cliente_localidad.text(),
                "provincia": self.vista.cliente_provincia.text(),
                "telefono": self.vista.cliente_telefono.text(),
                "precio_final": self.vista.vehiculo_precio_compra.text(),
                "fecha_seguro": "31/12/2025"
            }

            datos_vehiculo = {
                "matricula": self.vista.vehiculo_matricula.text(),
                "marca": self.vista.vehiculo_marca.text(),
                "modelo": self.vista.vehiculo_modelo.text(),
                "version": self.vista.vehiculo_version.text(),
                "bastidor": self.vista.vehiculo_bastidor.text(),
                "anio": self.vista.vehiculo_anio.text(),
                "km": self.vista.vehiculo_km.text(),
                "color": self.vista.vehiculo_color.text()
            }

            ruta_html = self.generar_contrato_compra_html(
                datos_cliente, datos_vehiculo, firma_cliente_base64)
            if ruta_html:
                webbrowser.open(f"file:///{os.path.abspath(ruta_html)}")
                QMessageBox.information(self.vista, "Simulación generada",
                                        "✅ El contrato de compra ha sido generado correctamente.")
            else:
                QMessageBox.critical(self.vista, "Error",
                                     "❌ No se pudo generar el contrato HTML.")

        except Exception as e:
            QMessageBox.critical(
                self.vista, "Error", f"❌ Error al simular contrato de compra:\n{str(e)}")

    def simular_contrato_venta(self):
        try:
            import shutil
            from jinja2 import Template

            # 1. Obtener la plantilla HTML
            with open("plantillas/contrato_venta_concesionario.html", "r", encoding="utf-8") as f:
                plantilla = Template(f.read())

            # 2. Obtener el vehículo seleccionado
            vehiculo = self.obtener_vehiculo_seleccionado()
            if not vehiculo:
                QMessageBox.warning(
                    self.vista, "Vehículo no seleccionado", "Debes seleccionar un vehículo de la tabla.")
                return

            # 3. Obtener la firma en base64 desde el capturador
            firma_cliente_base64 = self.vista.capturador_firma_venta.obtener_imagen_base64()

            # 4. Construir los datos a renderizar
            datos = {
                "fecha_actual": datetime.now().strftime("%d/%m/%Y"),
                "nombre_completo": self.vista.cliente_nombre.text(),
                "dni": self.vista.cliente_dni.text(),
                "direccion": self.vista.cliente_direccion.text(),
                "localidad": self.vista.cliente_localidad.text(),
                "provincia": self.vista.cliente_provincia.text(),
                "telefono": self.vista.cliente_telefono.text(),
                "precio_final": vehiculo["precio_venta"],
                "fecha_seguro": "31/12/2025",
                "firma_cliente": f"data:image/png;base64,{firma_cliente_base64}",
                "firma_taller": "img/firmataller.png",
                "matricula": vehiculo["matricula"],
                "marca": vehiculo["marca"],
                "modelo": vehiculo["modelo"],
                "version": vehiculo["version"],
                "bastidor": vehiculo["bastidor"],
                "anio": vehiculo["anio"],
                "km": vehiculo["kilometros"],
                "color": vehiculo["color"]
            }

            # 5. Renderizar HTML
            html_renderizado = plantilla.render(**datos)

            # 6. Obtener la ruta de guardado
            ruta_base = self.vista.input_ruta_guardado_venta.text()
            if not ruta_base:
                QMessageBox.warning(
                    self.vista, "Ruta no especificada", "Debes seleccionar una ruta de guardado.")
                return

            ruta_temp = os.path.join(ruta_base, "temp")
            os.makedirs(ruta_temp, exist_ok=True)

            # 7. Copiar CSS y recursos
            css_origen = os.path.abspath("plantillas/contrato_compraventa.css")
            css_destino = os.path.join(ruta_temp, "contrato_venta.css")
            shutil.copy(css_origen, css_destino)

            shutil.copy("img/logo.jpg", os.path.join(ruta_temp, "logo.jpg"))
            shutil.copy("img/firmataller.png",
                        os.path.join(ruta_temp, "firmataller.png"))

            # 8. Inyectar CSS al HTML
            html_con_css = f'<link rel="stylesheet" href="contrato_venta.css">\n{html_renderizado}'

            # 9. Guardar HTML generado
            ruta_final = os.path.join(
                ruta_temp, "contrato_venta_generado.html")
            with open(ruta_final, "w", encoding="utf-8") as f:
                f.write(html_con_css)

            # 10. Abrir navegador
            webbrowser.open(f"file:///{ruta_final}")

            # 11. Confirmación
            QMessageBox.information(self.vista, "Simulación generada",
                                    "El contrato de venta ha sido generado correctamente.")

        except Exception as e:
            print(f"❌ Error al simular contrato de venta: {e}")

    def obtener_vehiculo_seleccionado(self):
        fila = self.vista.tabla_vehiculos.currentRow()
        if fila == -1:
            return None
        return self.vista.vehiculos_filtrados[fila]

    def aceptar_contrato_compra(self):
        try:
            from weasyprint import HTML
            from jinja2 import Template

            # Obtener datos del formulario
            datos = {
                "marca": self.vista.vehiculo_marca.text().strip(),
                "modelo": self.vista.vehiculo_modelo.text().strip(),
                "version": self.vista.vehiculo_version.text().strip(),
                "anio": int(self.vista.vehiculo_anio.text()),
                "matricula": self.vista.vehiculo_matricula.text().strip(),
                "bastidor": self.vista.vehiculo_bastidor.text().strip(),
                "color": self.vista.vehiculo_color.text().strip(),
                "combustible": self.vista.vehiculo_combustible.text().strip(),
                "kilometros": int(self.vista.vehiculo_km.text()) if self.vista.vehiculo_km.text() else None,
                "potencia_cv": int(self.vista.vehiculo_cv.text()) if self.vista.vehiculo_cv.text() else None,
                "cambio": self.vista.vehiculo_cambio.text().strip(),
                "puertas": int(self.vista.vehiculo_puertas.text()) if self.vista.vehiculo_puertas.text() else None,
                "plazas": int(self.vista.vehiculo_plazas.text()) if self.vista.vehiculo_plazas.text() else None,
                "precio_compra": float(self.vista.vehiculo_precio_compra.text()),
                "precio_venta": float(self.vista.vehiculo_precio_venta.text()) if self.vista.vehiculo_precio_venta.text() else None,
                "descuento_maximo": float(self.vista.vehiculo_descuento.text()) if self.vista.vehiculo_descuento.text() else 0.00,
                "estado": "DISPONIBLE",
                "cliente_id": obtener_id_cliente(self.vista.cliente_dni.text().strip()),
                "origen_compra": "CLIENTE" if self.vista.cliente_nombre.text().strip() or self.vista.cliente_dni.text().strip() else "SUBASTA",
                "observaciones": self.vista.cliente_observaciones.toPlainText().strip(),
                "descuento_max": float(self.vista.vehiculo_descuento.text()) if self.vista.vehiculo_descuento.text() else 0.00,
                "dir_contrato": self.vista.input_ruta_guardado_compra.text().strip()
            }

            # Validar ruta personalizada
            if not datos["dir_contrato"]:
                QMessageBox.warning(self.vista, "Ruta no válida",
                                    "❌ No se ha especificado ninguna ruta de guardado del contrato.")
                return

            try:
                os.makedirs(datos["dir_contrato"], exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self.vista, "Error al crear carpeta",
                                    f"❌ No se pudo crear la carpeta de guardado:\n{str(e)}")
                return

            # Insertar vehículo en base de datos
            insertar_nuevo_vehiculo(datos)

            # Definir rutas
            ruta_temp_dir = obtener_ruta_absoluta(
                os.path.join("documentos", "compras", "temp"))
            os.makedirs(ruta_temp_dir, exist_ok=True)

            html_generado = os.path.join(
                ruta_temp_dir, "contrato_compra_generado.html")
            contrato_temp = os.path.join(
                ruta_temp_dir, "contrato_compra_temp.pdf")
            ruta_destino = os.path.join(
                datos["dir_contrato"], f"CONTRATO_COMPRA_{datos['matricula']}.pdf")

            # 1. Eliminar PDF temporal anterior si existía
            if os.path.exists(contrato_temp):
                try:
                    os.remove(contrato_temp)
                except Exception as e:
                    QMessageBox.warning(self.vista, "Error al eliminar PDF anterior",
                                        f"No se pudo eliminar el archivo temporal previo:\n{str(e)}")
                    return

            # 🧩 NUEVO: Renderizar HTML desde plantilla y guardarlo
            try:
                with open("plantillas/contrato_compra_concesionario.html", "r", encoding="utf-8") as f:
                    plantilla = Template(f.read())
                html_renderizado = plantilla.render(**datos)

                with open(html_generado, "w", encoding="utf-8") as f:
                    f.write(
                        f'<link rel="stylesheet" href="contrato_compra.css">\n{html_renderizado}')

                shutil.copy("plantillas/contrato_compraventa.css",
                            os.path.join(ruta_temp_dir, "contrato_compra.css"))
                shutil.copy("img/logo.jpg",
                            os.path.join(ruta_temp_dir, "logo.jpg"))
                shutil.copy("img/firmataller.png",
                            os.path.join(ruta_temp_dir, "firmataller.png"))
            except Exception as e:
                QMessageBox.critical(self.vista, "Error al preparar HTML",
                                     f"❌ No se pudo preparar el HTML para generar el contrato:\n{str(e)}")
                return

            # 2. Generar el PDF con WeasyPrint
            try:
                HTML(html_generado).write_pdf(contrato_temp)
            except Exception as e:
                QMessageBox.critical(self.vista, "Error al generar PDF",
                                     f"No se pudo generar el PDF con WeasyPrint:\n{str(e)}")
                return

            # 3. Copiar el PDF a la carpeta personalizada del usuario
            try:
                shutil.copy2(contrato_temp, ruta_destino)
            except Exception as e:
                QMessageBox.critical(self.vista, "Error al copiar PDF a carpeta destino",
                                     f"No se pudo copiar el PDF a la ruta seleccionada:\n{str(e)}")
                return

            # 4. Copiar también a la carpeta mensual (ej: documentos/compras/ABRIL_2025)
            nombre_mes = datetime.now().strftime("%B").upper()
            anio = datetime.now().year
            carpeta_mensual = os.path.join(
                "documentos", "compras", f"{nombre_mes}_{anio}")
            os.makedirs(carpeta_mensual, exist_ok=True)

            ruta_pdf_mensual = os.path.join(
                carpeta_mensual, f"CONTRATO_COMPRA_{datos['matricula']}.pdf")
            try:
                shutil.copy2(contrato_temp, ruta_pdf_mensual)
            except Exception as e:
                QMessageBox.warning(self.vista, "Advertencia",
                                    f"No se pudo copiar el PDF a la carpeta mensual:\n{str(e)}")

            # 5. Eliminar HTML temporal
            if os.path.exists(html_generado):
                os.remove(html_generado)
            if os.path.exists(contrato_temp):
                os.remove(contrato_temp)

            QMessageBox.information(self.vista, "Contrato registrado",
                                    "✅ El contrato de compra ha sido registrado correctamente.")

            self.vista.borrar_todo()

            # Enviar por correo si está marcado
            if self.vista.checkbox_correo_compra.isChecked():
                ventana_correo = VentanaCorreoConfirmacion(
                    self.vista.cliente_email.text(), self.vista)
                if ventana_correo.exec():
                    correo_destino = ventana_correo.correo_seleccionado
                    if correo_destino == "DEFECTO":
                        correo_destino = self.vista.cliente_email.text().strip()

                    datos_cliente = {
                        "Nombre": self.vista.cliente_nombre.text().strip()
                    }

                    exito, error = enviar_correo_contrato(
                        destinatario=correo_destino,
                        ruta_pdf=ruta_destino,
                        datos=datos_cliente,
                        tipo="compra"
                    )

                    if exito:
                        QMessageBox.information(self.vista, "Correo enviado",
                                                "📩 El contrato ha sido enviado correctamente por correo.")
                    else:
                        QMessageBox.warning(self.vista, "Error al enviar correo",
                                            f"❌ No se pudo enviar el correo:\n{error}")

            # ✅ Imprimir directamente (al estilo del módulo de ventas)
            if self.vista.checkbox_imprimir_compra.isChecked():
                try:
                    if os.path.isfile(ruta_destino):
                        print(f"🖨 Enviando a imprimir: {ruta_destino}")
                        os.startfile(ruta_destino, "print")
                    else:
                        QMessageBox.warning(self.vista, "Archivo no encontrado",
                                            "❌ El archivo PDF no existe o la ruta no es válida.\nNo se pudo imprimir el contrato.")
                except Exception as e:
                    QMessageBox.critical(self.vista, "Error al imprimir",
                                         f"❌ No se pudo enviar el contrato a la impresora predeterminada.\n\nDetalle del error:\n{str(e)}")

        except Exception as e:
            QMessageBox.critical(
                self.vista, "Error", f"❌ No se pudo registrar el contrato:\n{str(e)}")

    def generar_contrato_compra_html(self, datos_cliente, datos_vehiculo, firma_base64):
        from jinja2 import Template

        try:
            # 1. Plantilla
            with open("plantillas/contrato_compra_concesionario.html", "r", encoding="utf-8") as f:
                plantilla = Template(f.read())

            # 2. Renderizado
            datos = {
                "fecha_actual": datetime.now().strftime("%d/%m/%Y"),
                "firma_cliente": f"data:image/png;base64,{firma_base64}",
                "firma_taller": "img/firmataller.png",
                **datos_cliente,
                **datos_vehiculo
            }
            html_renderizado = plantilla.render(**datos)

            # 3. Rutas
            ruta_temp_dir = os.path.join("documentos", "compras", "temp")
            os.makedirs(ruta_temp_dir, exist_ok=True)
            ruta_css = os.path.join(ruta_temp_dir, "contrato_compra.css")
            ruta_html = os.path.join(
                ruta_temp_dir, "contrato_compra_generado.html")

            # 4. Copiar recursos
            shutil.copy("plantillas/contrato_compraventa.css", ruta_css)
            shutil.copy("img/logo.jpg",
                        os.path.join(ruta_temp_dir, "logo.jpg"))
            shutil.copy("img/firmataller.png",
                        os.path.join(ruta_temp_dir, "firmataller.png"))

            # 5. Insertar CSS en HTML
            html_con_css = f'<link rel="stylesheet" href="contrato_compra.css">\n{html_renderizado}'
            with open(ruta_html, "w", encoding="utf-8") as f:
                f.write(html_con_css)

            return ruta_html

        except Exception as e:
            print(f"❌ Error al generar HTML contrato compra: {e}")
            return None

    def aceptar_contrato_venta(self):
        try:
            from weasyprint import HTML

            vehiculo = self.obtener_vehiculo_seleccionado()
            if not vehiculo:
                QMessageBox.warning(self.vista, "Vehículo no seleccionado",
                                    "Debes seleccionar un vehículo de la tabla.")
                return

            firma_cliente_base64 = self.vista.capturador_firma_venta.obtener_imagen_base64()

            datos_cliente = {
                "nombre_completo": self.vista.cliente_nombre.text(),
                "dni": self.vista.cliente_dni.text(),
                "direccion": self.vista.cliente_direccion.text(),
                "localidad": self.vista.cliente_localidad.text(),
                "provincia": self.vista.cliente_provincia.text(),
                "telefono": self.vista.cliente_telefono.text(),
                "precio_final": vehiculo["precio_venta"],
                "fecha_seguro": "31/12/2025",
                "firma_cliente": f"data:image/png;base64,{firma_cliente_base64}",
                "firma_taller": "img/firmataller.png",
                **vehiculo
            }

            # Renderizar HTML desde plantilla
            with open("plantillas/contrato_venta_concesionario.html", "r", encoding="utf-8") as f:
                plantilla = Template(f.read())

            html_renderizado = plantilla.render(**datos_cliente)

            # Crear carpeta temporal
            ruta_temp = os.path.join("documentos", "ventas", "temp")
            os.makedirs(ruta_temp, exist_ok=True)

            html_path = os.path.join(ruta_temp, "contrato_venta_generado.html")
            pdf_temp = os.path.join(ruta_temp, "contrato_venta_temp.pdf")

            # Guardar HTML y recursos
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(
                    f'<link rel="stylesheet" href="contrato_venta.css">\n{html_renderizado}')
            shutil.copy("plantillas/contrato_compraventa.css",
                        os.path.join(ruta_temp, "contrato_venta.css"))
            shutil.copy("img/logo.jpg", os.path.join(ruta_temp, "logo.jpg"))
            shutil.copy("img/firmataller.png",
                        os.path.join(ruta_temp, "firmataller.png"))

            # Generar PDF
            HTML(html_path).write_pdf(pdf_temp)

            # Guardar en ruta personalizada
            ruta_usuario = self.vista.input_ruta_guardado_venta.text().strip()
            if not ruta_usuario:
                QMessageBox.warning(self.vista, "Ruta no válida",
                                    "Debes especificar una ruta para guardar el contrato.")
                return

            os.makedirs(ruta_usuario, exist_ok=True)

            # 🔧 AQUÍ definimos correctamente ruta_destino
            ruta_destino = os.path.join(
                ruta_usuario, f"CONTRATO_VENTA_{vehiculo['matricula']}.pdf")

            shutil.copy2(pdf_temp, ruta_destino)

            # Guardar en carpeta mensual
            nombre_mes = datetime.now().strftime("%B").upper()
            anio = datetime.now().year
            carpeta_mensual = os.path.join(
                "documentos", "ventas", f"{nombre_mes}_{anio}")
            os.makedirs(carpeta_mensual, exist_ok=True)

            ruta_pdf_mensual = os.path.join(
                carpeta_mensual, f"CONTRATO_VENTA_{vehiculo['matricula']}.pdf")
            shutil.copy2(pdf_temp, ruta_pdf_mensual)

            # Registrar venta
            cliente_id = obtener_id_cliente(
                self.vista.cliente_dni.text().strip())
            vehiculo_id = vehiculo["id"]
            precio_final = vehiculo["precio_venta"]
            registrar_venta(cliente_id, vehiculo_id, precio_final,
                            ruta_destino, ruta_usuario)

            # Imprimir si está marcado
            import subprocess

            # Enviar por correo si está marcado
            if self.vista.checkbox_correo_venta.isChecked():
                ventana_correo = VentanaCorreoConfirmacion(
                    self.vista.cliente_email.text(), self.vista)
                if ventana_correo.exec():
                    correo_destino = ventana_correo.correo_seleccionado
                    if correo_destino == "DEFECTO":
                        correo_destino = self.vista.cliente_email.text().strip()

                    datos_mail = {
                        "Nombre": self.vista.cliente_nombre.text().strip()
                    }
                    exito, error = enviar_correo_contrato(
                        destinatario=correo_destino,
                        ruta_pdf=ruta_destino,
                        datos=datos_mail,
                        tipo="venta"
                    )

                    if exito:
                        QMessageBox.information(self.vista, "Correo enviado",
                                                "📩 El contrato ha sido enviado correctamente.")
                    else:
                        QMessageBox.warning(self.vista, "Error al enviar correo",
                                            f"❌ No se pudo enviar el correo:\n{error}")

            # Eliminar temporales
            if os.path.exists(html_path):
                os.remove(html_path)
            if os.path.exists(pdf_temp):
                os.remove(pdf_temp)

            # Imprimir el contrato si está marcada la opción
            # ✅ Imprimir directamente (estilo RECOMENDADO)
            if self.vista.checkbox_imprimir_venta.isChecked():  # O el nombre que uses en la venta
                try:
                    if os.path.isfile(ruta_destino):
                        print(f"🖨 Enviando a imprimir: {ruta_destino}")
                        os.startfile(ruta_destino, "print")
                    else:
                        QMessageBox.warning(self.vista, "Archivo no encontrado",
                                            "❌ El archivo PDF no existe o la ruta no es válida.\nNo se pudo imprimir el contrato.")
                except Exception as e:
                    QMessageBox.critical(self.vista, "Error al imprimir",
                                         f"❌ No se pudo enviar el contrato a la impresora predeterminada.\n\nDetalle del error:\n{str(e)}")

            QMessageBox.information(self.vista, "Contrato registrado",
                                    "✅ El contrato de venta ha sido registrado correctamente.")

            self.vista.borrar_todo()

        except Exception as e:
            QMessageBox.critical(
                self.vista, "Error", f"❌ Error al aceptar contrato de venta:\n{str(e)}")
