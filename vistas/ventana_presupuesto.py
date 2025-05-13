from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QFormLayout, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QWidget, QCheckBox
)
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import Qt
from vistas.ventana_anadirTareaPresupuesto import DialogoTarea
from utilidades.rutas import obtener_ruta_absoluta
from datetime import datetime


class VentanaPresupuesto(QDialog):
    def __init__(self, ventana_padre=None):
        super().__init__(ventana_padre)
        self.ventana_padre = ventana_padre
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.forzar_cierre = False

        self.setWindowTitle("ReyBoxes - Presupuestos")
        self.setMinimumSize(600, 600)
        self.resize(600, 700)

        self.cargar_estilos()
        self.init_ui()

    def cargar_estilos(self):
        QFontDatabase.addApplicationFont(
            "font/Montserrat-Italic-VariableFont_wght.ttf")
        try:
            with open("css/presupuesto.css", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("No se pudo cargar el CSS:", e)

    def init_ui(self):
        layout_principal = QVBoxLayout(self)

        # Título
        titulo = QLabel("Gestión de Presupuestos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #e30613;")
        layout_principal.addWidget(titulo)

        # Selector de recepción
        layout_busqueda = QHBoxLayout()
        self.combo_recepciones = QComboBox()
        self.combo_recepciones.setObjectName("combo_recepciones")
        self.combo_recepciones.addItem("Elige una recepción")
        self.combo_recepciones.currentIndexChanged.connect(
            self.recepcion_seleccionada)
        layout_busqueda.addWidget(QLabel("Recepción:"))
        layout_busqueda.addWidget(self.combo_recepciones)
        layout_principal.addLayout(layout_busqueda)

        # Datos de la recepción
        formulario = QFormLayout()
        self.campo_cliente = QLineEdit()
        self.campo_cliente.setReadOnly(True)
        self.campo_vehiculo = QLineEdit()
        self.campo_vehiculo.setReadOnly(True)
        self.campo_fecha = QLineEdit()
        self.campo_fecha.setReadOnly(True)
        self.campo_limite = QLineEdit()
        self.campo_limite.setReadOnly(True)
        formulario.addRow("Cliente:", self.campo_cliente)
        formulario.addRow("Vehículo:", self.campo_vehiculo)
        formulario.addRow("Fecha recepción:", self.campo_fecha)
        formulario.addRow("Precio máx autorizado:", self.campo_limite)
        layout_principal.addLayout(formulario)

        # Observaciones
        self.texto_observaciones = QTextEdit(
            "Observaciones registradas en la recepción")
        self.texto_observaciones.setReadOnly(True)
        layout_principal.addWidget(self.texto_observaciones)

        # Scroll con tabla
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_contenedor_tabla")

        contenedor_tabla = QWidget()
        layout_tabla = QVBoxLayout(contenedor_tabla)

        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(4)
        self.tabla_tareas.setHorizontalHeaderLabels(
            ["Tarea", "Horas", "Precio", "Total"])
        self.tabla_tareas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_tareas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_tareas.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_tareas.verticalHeader().setVisible(False)
        self.tabla_tareas.setColumnWidth(1, 70)
        self.tabla_tareas.setColumnWidth(2, 90)
        self.tabla_tareas.setColumnWidth(3, 90)
        self.tabla_tareas.horizontalHeader().setStretchLastSection(False)
        self.tabla_tareas.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        alto_fila = self.tabla_tareas.verticalHeader().defaultSectionSize()
        alto_header = self.tabla_tareas.horizontalHeader().height()
        self.tabla_tareas.setFixedHeight(alto_fila * 5 + alto_header + 2)

        layout_tabla.addWidget(self.tabla_tareas)
        self.scroll_area.setWidget(contenedor_tabla)
        layout_principal.addWidget(self.scroll_area)

        # Botones tareas
        layout_botones_tareas = QHBoxLayout()
        self.boton_anadir_tarea = QPushButton("   Añadir tarea")
        self.boton_anadir_tarea.setIcon(
            QIcon(obtener_ruta_absoluta("img/anadir.png")))
        self.boton_anadir_tarea.clicked.connect(self.abrir_dialogo_tarea)
        self.boton_anadir_tarea.setEnabled(False)
        layout_botones_tareas.addWidget(self.boton_anadir_tarea)

        self.boton_eliminar_tarea = QPushButton("   Eliminar tarea")
        self.boton_eliminar_tarea.setIcon(
            QIcon(obtener_ruta_absoluta("img/eliminar.png")))
        self.boton_eliminar_tarea.clicked.connect(
            self.eliminar_tarea_seleccionada)
        layout_botones_tareas.addWidget(self.boton_eliminar_tarea)

        self.boton_subir_tarea = QPushButton("   Subir")
        self.boton_subir_tarea.setIcon(
            QIcon(obtener_ruta_absoluta("img/menos.png")))
        self.boton_subir_tarea.clicked.connect(self.subir_fila)
        layout_botones_tareas.addWidget(self.boton_subir_tarea)

        self.boton_bajar_tarea = QPushButton("   Bajar")
        self.boton_bajar_tarea.setIcon(
            QIcon(obtener_ruta_absoluta("img/mas.png")))
        self.boton_bajar_tarea.clicked.connect(self.bajar_fila)
        layout_botones_tareas.addWidget(self.boton_bajar_tarea)

        layout_principal.addLayout(layout_botones_tareas)

        # Coste total
        layout_coste = QHBoxLayout()
        layout_coste.addWidget(QLabel("Coste total estimado:"))
        self.campo_coste_total = QLineEdit("0.00 €")
        self.campo_coste_total.setReadOnly(True)
        layout_coste.addWidget(self.campo_coste_total)
        layout_principal.addLayout(layout_coste)

        # Autorización
        self.etiqueta_autorizado = QLabel("✓ Autorizado automáticamente")
        self.etiqueta_autorizado.setVisible(False)
        layout_principal.addWidget(self.etiqueta_autorizado)

        # Respuesta cliente
        layout_principal.addWidget(
            QLabel("Respuesta del cliente (si aplica):"))
        self.combo_respuesta = QComboBox()
        self.combo_respuesta.addItems(
            ["", "Aceptado", "Rechazado", "En espera"])
        layout_principal.addWidget(self.combo_respuesta)

        # Checkboxes
        layout_checkboxes = QHBoxLayout()
        self.checkbox_imprimir = QCheckBox("Imprimir presupuesto")
        self.checkbox_email = QCheckBox("Enviar por email")
        layout_checkboxes.addWidget(self.checkbox_imprimir)
        layout_checkboxes.addWidget(self.checkbox_email)
        layout_principal.addLayout(layout_checkboxes)

        # Botones finales
        layout_botones = QHBoxLayout()
        self.boton_guardar = QPushButton("   Guardar presupuesto")
        self.boton_guardar.setIcon(
            QIcon(obtener_ruta_absoluta("img/guardar.png")))
        self.boton_guardar.setEnabled(False)
        self.boton_guardar.clicked.connect(self.guardar_presupuesto)

        self.boton_volver = QPushButton("   Volver")
        self.boton_volver.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_volver.clicked.connect(self.volver)

        layout_botones.addWidget(self.boton_guardar)
        layout_botones.addWidget(self.boton_volver)
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

    def recepcion_seleccionada(self, index):
        if index <= 0 or not hasattr(self, "controlador"):
            self.campo_cliente.clear()
            self.campo_vehiculo.clear()
            self.campo_fecha.clear()
            self.campo_limite.clear()
            self.texto_observaciones.clear()
            self._actualizar_estado_guardar()
            return

        datos = self.controlador.recepciones[index - 1]
        self.campo_cliente.setText(datos.get("cliente", ""))
        self.campo_vehiculo.setText(datos.get("matricula", ""))
        fecha = datos.get("fecha", None)
        self.campo_fecha.setText(
            fecha.strftime("%d/%m/%Y %H:%M") if isinstance(fecha,
                                                           datetime) else "(sin fecha)"
        )

        precio_max = datos.get("precio_max_autorizado", None)
        self.campo_limite.setText(f"{precio_max:.2f} €" if precio_max else "")
        self.texto_observaciones.setText(datos.get("observaciones", ""))

        self._actualizar_estado_guardar()

    def abrir_dialogo_tarea(self):
        dialogo = DialogoTarea()
        if dialogo.exec():
            datos = dialogo.obtener_datos()
            if datos:
                tarea, horas, precio, total = datos
                fila = self.tabla_tareas.rowCount()
                self.tabla_tareas.insertRow(fila)
                self.tabla_tareas.setItem(fila, 0, QTableWidgetItem(tarea))
                self.tabla_tareas.setItem(
                    fila, 1, QTableWidgetItem(f"{horas:.2f}"))
                self.tabla_tareas.setItem(
                    fila, 2, QTableWidgetItem(f"{precio:.2f} €"))
                self.tabla_tareas.setItem(
                    fila, 3, QTableWidgetItem(f"{total:.2f} €"))
                self.actualizar_coste_total()
                self._actualizar_estado_guardar()

    def eliminar_tarea_seleccionada(self):
        fila = self.tabla_tareas.currentRow()
        if fila != -1:
            self.tabla_tareas.removeRow(fila)
            self.actualizar_coste_total()
            self._actualizar_estado_guardar()

    def actualizar_coste_total(self):
        total = 0
        for fila in range(self.tabla_tareas.rowCount()):
            item = self.tabla_tareas.item(fila, 3)
            if item:
                texto = item.text().replace("€", "").strip()
                try:
                    total += float(texto)
                except ValueError:
                    pass
        self.campo_coste_total.setText(f"{total:.2f} €")

        try:
            limite = float(self.campo_limite.text().replace("€", "").strip())
            if total <= limite:
                self.combo_respuesta.setCurrentText("Aceptado")
            else:
                self.combo_respuesta.setCurrentText("En espera")
        except ValueError:
            self.combo_respuesta.setCurrentText("")

    def subir_fila(self):
        fila = self.tabla_tareas.currentRow()
        if fila > 0:
            self._intercambiar_filas(fila, fila - 1)
            self.tabla_tareas.selectRow(fila - 1)

    def bajar_fila(self):
        fila = self.tabla_tareas.currentRow()
        if fila != -1 and fila < self.tabla_tareas.rowCount() - 1:
            self._intercambiar_filas(fila, fila + 1)
            self.tabla_tareas.selectRow(fila + 1)

    def _intercambiar_filas(self, fila1, fila2):
        for col in range(self.tabla_tareas.columnCount()):
            texto1 = self.tabla_tareas.item(fila1, col).text()
            texto2 = self.tabla_tareas.item(fila2, col).text()
            self.tabla_tareas.setItem(fila1, col, QTableWidgetItem(texto2))
            self.tabla_tareas.setItem(fila2, col, QTableWidgetItem(texto1))

    def _actualizar_estado_guardar(self):
        index = self.combo_recepciones.currentIndex()
        tiene_recepcion_valida = index > 0 and hasattr(self, "controlador")
        tiene_tareas = self.tabla_tareas.rowCount() > 0
        self.boton_guardar.setEnabled(tiene_recepcion_valida and tiene_tareas)
        self.boton_anadir_tarea.setEnabled(tiene_recepcion_valida)

    def guardar_presupuesto(self):
        imprimir = self.checkbox_imprimir.isChecked()
        enviar = self.checkbox_email.isChecked()
        total = self.campo_coste_total.text()
        respuesta = self.combo_respuesta.currentText()
        print("➡ Guardando presupuesto:")
        print(f"   - Imprimir: {imprimir}")
        print(f"   - Enviar por email: {enviar}")
        print(f"   - Total estimado: {total}")
        print(f"   - Respuesta cliente: {respuesta}")

    def cargar_presupuesto(self, datos_presupuesto):
        self.combo_recepciones.setCurrentIndex(0)
        self.combo_recepciones.setEnabled(False)
        self.boton_anadir_tarea.setEnabled(False)

        self.campo_cliente.setText(datos_presupuesto.get("cliente", ""))
        self.campo_vehiculo.setText(datos_presupuesto.get("vehiculo", ""))
        fecha = datos_presupuesto.get("fecha", None)
        self.campo_fecha.setText(fecha.strftime(
            "%d/%m/%Y %H:%M") if isinstance(fecha, datetime) else "(sin fecha)")
        precio_max = datos_presupuesto.get("precio_max_autorizado", None)
        self.campo_limite.setText(f"{precio_max:.2f} €" if precio_max else "")
        self.texto_observaciones.setText(
            datos_presupuesto.get("observaciones", ""))

        self.tabla_tareas.setRowCount(0)
        for tarea in datos_presupuesto.get("tareas", []):
            fila = self.tabla_tareas.rowCount()
            self.tabla_tareas.insertRow(fila)
            self.tabla_tareas.setItem(
                fila, 0, QTableWidgetItem(tarea["descripcion"]))
            self.tabla_tareas.setItem(
                fila, 1, QTableWidgetItem(f"{tarea['horas']:.2f}"))
            self.tabla_tareas.setItem(fila, 2, QTableWidgetItem(
                f"{tarea['precio_hora']:.2f} €"))
            self.tabla_tareas.setItem(
                fila, 3, QTableWidgetItem(f"{tarea['total']:.2f} €"))

        self.actualizar_coste_total()

    def closeEvent(self, event):
        event.accept() if self.forzar_cierre else event.ignore()

    def volver(self):
        self.forzar_cierre = True
        self.close()
