"""
Controlador para la reimpresión de documentos de compras.

Permite al usuario:
- Visualizar documentos PDF generados al registrar compras.
- Imprimir el documento seleccionado mediante el visor predeterminado del sistema.
- Enviar el documento por correo electrónico a un destinatario.

Utiliza:
- `VentanaReimpresionCompras`: Vista principal.
- `VentanaCorreoConfirmacion`: Diálogo para introducir el correo destino.
- `enviar_correo_reimpresion_compra`: Función para envío del documento PDF adjunto.
"""
from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion
from utilidades.rutas import obtener_ruta_absoluta
from utilidades.correo_reenviarCompras import enviar_correo_reimpresion_compra

from PySide6.QtWidgets import QMessageBox
import subprocess
import os


class ReimpresionComprasControlador:
    """
    Controlador encargado de gestionar la reimpresión de documentos de compras.

    Proporciona opciones para reenviar documentos PDF por correo electrónico
    o enviarlos a impresión mediante la aplicación predeterminada del sistema.
    """

    def __init__(self, main_app, nombre_usuario, rol_usuario):
        """
        Inicializa la vista de reimpresión de compras y conecta los botones de acción.

        Args:
            main_app: Instancia principal de la aplicación.
            nombre_usuario (str): Nombre del usuario activo.
            rol_usuario (str): Rol del usuario activo.
        """
        self.main_app = main_app
        self.nombre_usuario = nombre_usuario
        self.rol_usuario = rol_usuario

        self.ventana = VentanaReimpresionCompras(
            nombre_usuario=nombre_usuario,
            rol_usuario=rol_usuario,
            volver_callback=self.volver_a_inicio
        )

        self.ventana.btn_enviar.clicked.connect(self.enviar_documento)
        self.ventana.btn_imprimir.clicked.connect(self.imprimir_documento)

        self.ventana.show()

    def volver_a_inicio(self):
        """
        Cierra la ventana actual y retorna al menú principal.
        """
        self.ventana.close()
        self.main_app.mostrar_ventana_inicio(
            self.nombre_usuario, self.rol_usuario)

    def obtener_documento_seleccionado(self):
        """
        Obtiene la ruta del documento PDF actualmente seleccionado en la tabla.

        Returns:
            str or None: Ruta del archivo si se ha seleccionado una fila válida y existe,
                         o None en caso contrario.
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
        Envía el documento seleccionado a impresión abriéndolo con el visor de PDF del sistema.
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
        Abre un cuadro de diálogo para introducir el correo destino y,
        si se confirma, envía el documento PDF por correo electrónico.
        """
        ruta = self.obtener_documento_seleccionado()
        if not ruta:
            return

        dialogo = VentanaCorreoConfirmacion("cliente@ejemplo.com")
        if dialogo.exec():
            correo = dialogo.correo_seleccionado
            if correo:
                exito, error = enviar_correo_reimpresion_compra(correo, ruta)
                if exito:
                    QMessageBox.information(
                        self.ventana, "Enviado", "Correo enviado correctamente.")
                else:
                    QMessageBox.critical(
                        self.ventana, "Error", f"No se pudo enviar el correo:\n{error}")
