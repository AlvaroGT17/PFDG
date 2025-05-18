"""
Controlador para la reimpresión de documentos de recepcionamiento.

Este módulo permite:
- Visualizar los documentos PDF generados en recepcionamientos.
- Reenviar un documento por correo electrónico a un cliente.
- Imprimir (abrir) el documento seleccionado con el visor predeterminado del sistema.
- Volver al menú principal de la aplicación.

Conecta con:
- `VentanaReimpresionRecepcionamiento`: Interfaz de usuario.
- `VentanaCorreoConfirmacion`: Diálogo para selección de correo destino.
- `enviar_correo_recepcionamiento`: Utilidad para enviar PDFs por correo.
"""

import os
import locale
import webbrowser
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from datetime import datetime
from vistas.ventana_reimpresionRecepcionamiento import VentanaReimpresionRecepcionamiento
from utilidades.correo_reenviar_recepcionamiento import enviar_correo_recepcionamiento
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion


class ReimpresionRecepcionamientoControlador:
    """
    Controlador que gestiona la ventana de reimpresión de recepcionamientos.

    Permite al usuario imprimir o enviar por correo documentos PDF generados previamente,
    y volver al menú principal.
    """

    def __init__(self, main_app, nombre_usuario, rol_usuario):
        """
        Inicializa la ventana, conecta eventos y carga documentos disponibles.

        Args:
            main_app: Instancia principal de la aplicación.
            nombre_usuario (str): Nombre del usuario actual.
            rol_usuario (str): Rol del usuario actual.
        """
        self.main_app = main_app
        self.nombre = nombre_usuario
        self.rol = rol_usuario

        self.ventana = VentanaReimpresionRecepcionamiento(
            nombre_usuario=self.nombre,
            rol_usuario=self.rol,
            volver_callback=self.volver_a_inicio
        )

        # Conectar botones
        self.ventana.btn_enviar.clicked.connect(self.enviar_documento)
        self.ventana.btn_imprimir.clicked.connect(self.imprimir_documento)

        self.ventana.show()
        self.cargar_documentos()

    def obtener_documento_seleccionado(self):
        """
        Devuelve la ruta del documento seleccionado en la tabla.

        Returns:
            str or None: Ruta del archivo seleccionado o None si no hay selección o no existe.
        """
        fila = self.ventana.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self.ventana, "Sin selección",
                                "Por favor, selecciona un documento.")
            return None

        ruta = self.ventana.tabla.item(fila, 2).text()
        return ruta if os.path.exists(ruta) else None

    def enviar_documento(self):
        """
        Abre un diálogo para seleccionar el correo destino y envía el PDF por email.

        Utiliza `enviar_correo_recepcionamiento` para enviar el archivo adjunto.
        """
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        # Simulamos un nombre de cliente para este ejemplo
        nombre_cliente = self.nombre.capitalize()

        # Ventana para elegir a qué correo enviar
        dialogo = VentanaCorreoConfirmacion(
            "cliente@ejemplo.com", parent=self.ventana)
        if dialogo.exec():
            destino = dialogo.correo_seleccionado

            if destino == "DEFECTO":
                # Aquí podrías buscar el correo real del cliente desde BD si lo tienes
                destino = "cliente@ejemplo.com"

            exito, error = enviar_correo_recepcionamiento(
                destino, ruta, nombre_cliente)
            if exito:
                QMessageBox.information(
                    self.ventana, "Correo enviado", f"El documento se ha enviado correctamente a {destino}.")
            else:
                QMessageBox.critical(self.ventana, "Error",
                                     f"No se pudo enviar el correo:\n{error}")

    def imprimir_documento(self):
        """
        Abre el documento PDF seleccionado con el visor de archivos predeterminado del sistema.
        """
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        try:
            # Abrimos el PDF con el visor predeterminado del sistema
            webbrowser.open_new(ruta)

        except Exception as e:
            QMessageBox.critical(
                self.ventana,
                "Error al imprimir",
                f"No se pudo abrir/imprimir el documento:\n{str(e)}"
            )

    def volver_a_inicio(self):
        """
        Cierra esta ventana y retorna al menú principal.
        """
        self.ventana.close()
        self.main_app.mostrar_ventana_inicio(self.nombre, self.rol)

    def cargar_documentos(self):
        """
        Recorre la carpeta de documentos de recepcionamiento y carga los PDF
        en la tabla visual, agrupándolos por mes si el nombre de la carpeta es YYYY-MM.
        """
        ruta_base = "documentos/recepcionamiento"
        if not os.path.exists(ruta_base):
            return

        filas = []

        for raiz, carpetas, archivos in os.walk(ruta_base):
            for archivo in archivos:
                if archivo.lower().endswith(".pdf"):
                    ruta_completa = os.path.join(raiz, archivo)
                    print("📄 Detectado:", ruta_completa)

                    # Obtener nombre de carpeta padre como "mes"
                    nombre_carpeta = os.path.basename(
                        os.path.dirname(ruta_completa))

                    try:
                        fecha = datetime.strptime(nombre_carpeta, "%Y-%m")
                        mes_legible = fecha.strftime("%B %Y").capitalize()
                    except ValueError:
                        mes_legible = nombre_carpeta.capitalize()

                    filas.append((mes_legible, archivo, ruta_completa))

        self.ventana.tabla.setRowCount(len(filas))
        for i, (mes, archivo, ruta) in enumerate(filas):
            self.ventana.tabla.setItem(i, 0, QTableWidgetItem(mes))
            self.ventana.tabla.setItem(i, 1, QTableWidgetItem(archivo))
            self.ventana.tabla.setItem(i, 2, QTableWidgetItem(ruta))
