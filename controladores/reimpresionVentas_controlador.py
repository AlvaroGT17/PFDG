"""
Controlador para la reimpresión de documentos de ventas.

Permite al usuario:
- Visualizar documentos PDF generados de ventas.
- Imprimir un documento seleccionado.
- Reenviar por correo electrónico el documento a un destinatario elegido.

Conecta con:
- `VentanaReimpresionVentas`: vista principal de reimpresión.
- `VentanaCorreoConfirmacion`: diálogo para ingresar el correo destino.
- `enviar_correo_reimpresion_venta`: utilidad para envío del documento por correo.
"""
from vistas.ventana_reimpresionVentas import VentanaReimpresionVentas
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion
from utilidades.rutas import obtener_ruta_absoluta
from utilidades.correo_reenviarVentas import enviar_correo_reimpresion_venta

from PySide6.QtWidgets import QMessageBox
import subprocess
import os


class ReimpresionVentasControlador:
    """
    Controlador de la ventana de reimpresión de documentos de ventas.

    Permite seleccionar, imprimir o reenviar un documento generado
    previamente. Está asociado a un usuario y su rol correspondiente.
    """

    def __init__(self, main_app, nombre_usuario, rol_usuario):
        """
        Inicializa la vista de reimpresión y conecta los botones principales.

        Args:
            main_app: Instancia principal de la aplicación, usada para volver al inicio.
            nombre_usuario (str): Nombre del usuario activo.
            rol_usuario (str): Rol del usuario activo.
        """
        self.main_app = main_app
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario

        self.ventana = VentanaReimpresionVentas(
            nombre_usuario=nombre_usuario,
            rol_usuario=rol_usuario,
            volver_callback=self.volver_a_inicio
        )

        self.ventana.btn_enviar.clicked.connect(self.enviar_documento)
        self.ventana.btn_imprimir.clicked.connect(self.imprimir_documento)

        self.ventana.show()

    def volver_a_inicio(self):
        """
        Cierra la ventana actual y vuelve al menú principal.
        """
        self.ventana.close()
        self.main_app.mostrar_ventana_inicio(
            self.nombre_usuario, self.rol_usuario
        )

    def obtener_documento_seleccionado(self):
        """
        Recupera la ruta del documento actualmente seleccionado en la tabla.

        Returns:
            str or None: Ruta al archivo PDF si está seleccionada, None si no hay selección o hay error.
        """
        fila = self.ventana.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self.ventana, "Sin selección",
                                "Selecciona un documento para continuar.")
            return None
        ruta_item = self.ventana.tabla.item(fila, 2)
        if not ruta_item:
            QMessageBox.critical(self.ventana, "Error",
                                 "No se pudo obtener la ruta del documento.")
            return None
        return ruta_item.text()

    def imprimir_documento(self):
        """
        Envía a imprimir el documento seleccionado, abriéndolo con la aplicación predeterminada del sistema.
        """
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return
        if not os.path.exists(ruta):
            QMessageBox.warning(
                self.ventana, "Archivo no encontrado", "El archivo seleccionado no existe.")
            return
        try:
            subprocess.Popen(["start", ruta], shell=True)
            QMessageBox.information(
                self.ventana, "Impresión", "El documento se ha enviado a imprimir.")
        except Exception as e:
            QMessageBox.critical(self.ventana, "Error",
                                 f"No se pudo imprimir el documento:\n{str(e)}")

    def enviar_documento(self):
        """
        Abre un cuadro de diálogo para confirmar y enviar el documento PDF por correo.

        Si el usuario acepta y proporciona un correo válido, el archivo se envía
        como adjunto usando `enviar_correo_reimpresion_venta`.
        """
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        dialogo = VentanaCorreoConfirmacion("cliente@ejemplo.com")
        if dialogo.exec():
            correo = dialogo.correo_seleccionado
            if correo:
                exito, error = enviar_correo_reimpresion_venta(correo, ruta)
                if exito:
                    QMessageBox.information(
                        self.ventana, "Enviado", "Correo enviado correctamente.")
                else:
                    QMessageBox.critical(
                        self.ventana, "Error", f"No se pudo enviar el correo:\n{error}")
