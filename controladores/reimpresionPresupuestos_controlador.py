import os
import webbrowser
from datetime import datetime
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion
from utilidades.correo_renviarPresupuestos import enviar_correo_presupuesto
from utilidades.rutas import obtener_ruta_absoluta


class ReimpresionPresupuestosControlador:
    def __init__(self, main_app, nombre_usuario, rol_usuario):
        self.main_app = main_app
        self.nombre = nombre_usuario
        self.rol = rol_usuario

        self.ventana = VentanaReimpresionPresupuestos(
            nombre_usuario=self.nombre,
            rol_usuario=self.rol,
            volver_callback=self.volver_a_inicio
        )

        # Conectar botones
        self.ventana.btn_enviar.clicked.connect(self.enviar_documento)
        self.ventana.btn_imprimir.clicked.connect(self.imprimir_documento)

        self.ventana.show()
        self.cargar_documentos()

    def volver_a_inicio(self):
        self.ventana.close()
        self.main_app.mostrar_ventana_inicio(self.nombre, self.rol)

    def cargar_documentos(self):
        print("🔄 Cargando documentos de presupuestos...")
        ruta_base = obtener_ruta_absoluta("documentos/presupuestos")
        if not os.path.exists(ruta_base):
            print("❌ Carpeta no encontrada:", ruta_base)
            return

        filas = []

        for raiz, _, archivos in os.walk(ruta_base):
            for archivo in archivos:
                if archivo.lower().endswith(".pdf"):
                    ruta_completa = os.path.join(raiz, archivo)
                    print(f"📄 Documento detectado: {ruta_completa}")

                    nombre_carpeta = os.path.basename(
                        os.path.dirname(ruta_completa))
                    try:
                        fecha = datetime.strptime(nombre_carpeta, "%B_%Y")
                        mes_legible = fecha.strftime("%B %Y").capitalize()
                    except ValueError:
                        mes_legible = nombre_carpeta.capitalize()

                    filas.append((mes_legible, archivo, ruta_completa))

        self.ventana.tabla.setRowCount(len(filas))
        for i, (mes, archivo, ruta) in enumerate(filas):
            self.ventana.tabla.setItem(i, 0, QTableWidgetItem(mes))
            self.ventana.tabla.setItem(i, 1, QTableWidgetItem(archivo))
            self.ventana.tabla.setItem(i, 2, QTableWidgetItem(ruta))

    def obtener_documento_seleccionado(self):
        fila = self.ventana.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self.ventana, "Sin selección",
                                "Por favor, selecciona un documento.")
            return None
        ruta = self.ventana.tabla.item(fila, 2).text()
        return ruta if os.path.exists(ruta) else None

    def imprimir_documento(self):
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        try:
            webbrowser.open_new(ruta)
        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", str(e))

    def enviar_documento(self):
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        # Extraer nombre de cliente del archivo, si es posible
        nombre_archivo = os.path.basename(ruta)
        cliente_extraido = "Cliente"
        partes = nombre_archivo.split("_")
        if len(partes) >= 2:
            cliente_extraido = partes[1].capitalize()

        dialogo = VentanaCorreoConfirmacion(
            correo_defecto="cliente@ejemplo.com", parent=self.ventana)
        if dialogo.exec():
            correo = dialogo.correo_seleccionado
            if correo:
                datos_dummy = {
                    "cliente": cliente_extraido
                }
                exito, error = enviar_correo_presupuesto(
                    correo, ruta, datos_dummy)
                if exito:
                    QMessageBox.information(self.ventana, "Éxito",
                                            "Documento enviado correctamente.")
                else:
                    QMessageBox.critical(self.ventana, "Error",
                                         f"No se pudo enviar el documento:\n{error}")
