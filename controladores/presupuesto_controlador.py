from modelos.presupuesto_consultas import (
    obtener_recepciones_para_presupuesto,
    insertar_presupuesto,
    insertar_tarea_presupuesto
)
from utilidades.correo_presupuesto import enviar_correo_presupuesto
from vistas.ventana_dialogoCorreoPresupuesto import VentanaDialogoCorreoPresupuesto
from datetime import datetime
from PySide6.QtWidgets import QMessageBox
from jinja2 import Template
from weasyprint import HTML, CSS
import os
from calendar import month_name


class PresupuestoControlador:
    def __init__(self, ventana):
        print("🟢 PresupuestoControlador inicializado")
        self.ventana = ventana
        self.ventana.controlador = self
        self.recepciones = []
        self.cargar_recepciones()

        self.ventana.boton_guardar.clicked.disconnect()
        self.ventana.boton_guardar.clicked.connect(self.guardar_presupuesto)

    def cargar_recepciones(self):
        print("🔄 Cargando recepciones...")
        self.ventana.combo_recepciones.clear()
        self.recepciones = obtener_recepciones_para_presupuesto()
        print(f"📋 Recepcionamientos disponibles: {len(self.recepciones)}")
        self.ventana.combo_recepciones.clear()

        if not self.recepciones:
            self.ventana.combo_recepciones.addItem(
                "No hay recepciones disponibles")
            self.ventana.combo_recepciones.setEnabled(False)
            return

        self.ventana.combo_recepciones.addItem("Elige una recepción")
        self.ventana.combo_recepciones.setEnabled(True)

        for recepcion in self.recepciones:
            texto = f"#{recepcion['num_recepcionamiento']} - {recepcion['cliente']} - {recepcion['matricula']}"
            self.ventana.combo_recepciones.addItem(
                texto, userData=recepcion["id"])

    def guardar_presupuesto(self):
        index = self.ventana.combo_recepciones.currentIndex()
        if index <= 0:
            QMessageBox.warning(self.ventana, "Aviso",
                                "Debes seleccionar una recepción válida.")
            return

        recepcion = self.recepciones[index - 1]
        recepcion_id = self.ventana.combo_recepciones.itemData(index)
        respuesta_cliente = self.ventana.combo_respuesta.currentText()
        imprimir = self.ventana.checkbox_imprimir.isChecked()
        enviar = False
        correo_destino = None

        if self.ventana.checkbox_email.isChecked():
            correo_defecto = recepcion.get(
                "correo_cliente", "") or "cliente@ejemplo.com"
            dialogo = VentanaDialogoCorreoPresupuesto(
                correo_defecto, self.ventana)
            if dialogo.exec():
                correo_destino = dialogo.obtener_correo()
                enviar = True
            else:
                enviar = False  # Cancelado

        try:
            total = float(
                self.ventana.campo_coste_total.text().replace("€", "").strip())
        except ValueError:
            total = 0.0

        tareas = []
        for fila in range(self.ventana.tabla_tareas.rowCount()):
            descripcion = self.ventana.tabla_tareas.item(fila, 0).text()
            horas = float(self.ventana.tabla_tareas.item(fila, 1).text())
            precio_hora = float(self.ventana.tabla_tareas.item(
                fila, 2).text().replace("€", "").strip())
            total_tarea = float(self.ventana.tabla_tareas.item(
                fila, 3).text().replace("€", "").strip())

            tareas.append({
                "descripcion": descripcion,
                "horas": horas,
                "precio_hora": precio_hora,
                "total": total_tarea
            })

        datos_pdf = {
            "cliente": recepcion["cliente"],
            "matricula": recepcion["matricula"],
            "fecha_recepcion": recepcion["fecha"].strftime("%d/%m/%Y %H:%M") if isinstance(recepcion["fecha"], datetime) else "",
            "precio_max": f"{recepcion.get('precio_max_autorizado', 0):.2f}",
            "respuesta_cliente": respuesta_cliente,
            "observaciones": recepcion.get("observaciones", ""),
            "total_estimado": f"{total:.2f}",
            "tareas": tareas
        }

        ruta_pdf = self.generar_pdf_presupuesto(datos_pdf)

        presupuesto_id = insertar_presupuesto(
            recepcion_id=recepcion_id,
            total=total,
            respuesta=respuesta_cliente,
            ruta_pdf=ruta_pdf
        )

        for tarea in tareas:
            insertar_tarea_presupuesto(
                presupuesto_id,
                tarea["descripcion"],
                tarea["horas"],
                tarea["precio_hora"],
                tarea["total"]
            )

        if enviar and correo_destino:
            exito, error = enviar_correo_presupuesto(
                correo_destino, ruta_pdf, datos_pdf)
            if not exito:
                QMessageBox.critical(
                    self.ventana, "Error al enviar", f"No se pudo enviar el correo:\n{error}")

        if imprimir:
            import subprocess
            subprocess.Popen(["start", ruta_pdf], shell=True)

        QMessageBox.information(
            self.ventana, "Presupuesto guardado", "Presupuesto guardado correctamente.")
        self.ventana.resetear_formulario()
        self.cargar_recepciones()

    def generar_pdf_presupuesto(self, datos):
        fecha_actual = datetime.now()
        mes = month_name[fecha_actual.month].capitalize()
        carpeta_mes = f"{mes}_{fecha_actual.year}"

        ruta_directorio = os.path.join(
            "documentos", "presupuestos", carpeta_mes)
        os.makedirs(ruta_directorio, exist_ok=True)

        nombre_archivo = f"Presupuesto_{datos['matricula'].replace(' ', '_')}_{fecha_actual.strftime('%Y%m%d_%H%M')}.pdf"
        ruta_pdf = os.path.join(ruta_directorio, nombre_archivo)

        with open("plantillas/plantilla_presupuesto.html", "r", encoding="utf-8") as f:
            html_base = f.read()

        filas_html = ""
        for tarea in datos["tareas"]:
            fila = f"""
            <tr>
                <td>{tarea['descripcion']}</td>
                <td>{tarea['horas']:.2f}</td>
                <td>{tarea['precio_hora']:.2f} €</td>
                <td>{tarea['total']:.2f} €</td>
            </tr>"""
            filas_html += fila

        plantilla = Template(html_base)
        html_renderizado = plantilla.render(
            fecha_actual=fecha_actual.strftime("%d/%m/%Y"),
            cliente=datos["cliente"],
            matricula=datos["matricula"],
            fecha_recepcion=datos["fecha_recepcion"],
            precio_max=datos["precio_max"],
            respuesta_cliente=datos["respuesta_cliente"],
            observaciones=datos["observaciones"],
            total_estimado=datos["total_estimado"],
            filas_tareas=filas_html
        )

        css_path = "plantillas/plantilla_presupuesto.css"
        HTML(string=html_renderizado, base_url=".").write_pdf(
            ruta_pdf, stylesheets=[CSS(css_path)]
        )

        return ruta_pdf

    def resetear_formulario(self):
        self.combo_recepciones.setCurrentIndex(0)
        self.combo_recepciones.setEnabled(True)
        self.campo_cliente.clear()
        self.campo_vehiculo.clear()
        self.campo_fecha.clear()
        self.campo_limite.clear()
        self.texto_observaciones.clear()
        self.tabla_tareas.setRowCount(0)
        self.campo_coste_total.setText("0.00 €")
        self.combo_respuesta.setCurrentIndex(0)
        self.checkbox_imprimir.setChecked(False)
        self.checkbox_email.setChecked(False)
        self.etiqueta_autorizado.setVisible(False)
        self._actualizar_estado_guardar()
