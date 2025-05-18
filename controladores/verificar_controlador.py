"""
Controlador de la ventana de verificación de código OTP.

Gestiona:
- La cuenta atrás de expiración del código (5 minutos).
- La validación y verificación del código introducido.
- La transición hacia la pantalla de restablecimiento de contraseña si el código es válido.
- El retorno a la pantalla anterior si el usuario cancela.

Se conecta con `VentanaVerificar` y utiliza `verificar_codigo_recuperacion` del modelo `login_consultas`.
"""

import re
from PySide6.QtCore import QObject, Signal, QTimer, QTime
from PySide6.QtWidgets import QMessageBox
from vistas.ventana_verificar import VentanaVerificar
from modelos.login_consultas import verificar_codigo_recuperacion


class VerificarControlador(QObject):
    """
    Controlador que gestiona la lógica de la ventana de verificación del código OTP.

    Señales:
        senal_codigo_valido (str): Emitida si el código es correcto, para avanzar al cambio de contraseña.
        senal_volver_recuperar (): Emitida al cerrar o pulsar "Volver", para regresar a la pantalla de recuperación.

    Métodos:
        mostrar(): Muestra la ventana.
        cerrar(): Cierra la ventana y detiene el temporizador.
        volver(): Emite la señal de retorno y cierra la ventana.
        handle_cierre_ventana(event): Gestiona el cierre con el aspa (❌).
        validar_codigo(): Habilita el botón solo si el código es numérico y de 6 cifras.
        verificar(): Llama a la función del modelo para validar el código OTP.
        actualizar_tiempo(): Actualiza el temporizador en pantalla y detecta expiración.
        volver_al_login(): Se llama al finalizar correctamente la verificación.
    """

    senal_codigo_valido = Signal(str)
    senal_volver_recuperar = Signal()

    def __init__(self, email):
        """
        Inicializa la ventana de verificación con temporizador y eventos conectados.

        Args:
            email (str): Correo electrónico del usuario al que se le envió el código.
        """
        super().__init__()
        self.email = email
        self.ventana = VentanaVerificar()

        # 🕒 Inicializar cuenta atrás (5 minutos)
        self.tiempo_restante = QTime(0, 5, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.timer.start(1000)  # cada segundo

        self.actualizar_tiempo()  # mostrar inmediatamente

        # Conectar eventos
        self.ventana.btn_verificar.clicked.connect(self.verificar)
        self.ventana.btn_volver.clicked.connect(self.volver)
        self.ventana.input_codigo.textChanged.connect(self.validar_codigo)
        self.ventana.closeEvent = self.handle_cierre_ventana

    def mostrar(self):
        """Muestra la ventana de verificación."""
        self.ventana.show()

    def cerrar(self):
        """Cierra la ventana y detiene el temporizador."""
        self.timer.stop()
        self.ventana.close()

    def volver(self):
        """Acción del botón 'Volver'. Cierra la ventana y emite señal de regreso."""
        self.cerrar()
        self.senal_volver_recuperar.emit()

    def handle_cierre_ventana(self, event):
        """
        Gestiona el cierre de ventana por aspa (❌).

        Args:
            event (QCloseEvent): Evento de cierre.
        """
        self.timer.stop()
        self.senal_volver_recuperar.emit()
        event.accept()

    def validar_codigo(self):
        """
        Valida el campo de entrada del código: debe tener 6 dígitos.
        Habilita o deshabilita el botón 'Verificar' según corresponda.
        """
        texto = self.ventana.input_codigo.text()
        self.ventana.btn_verificar.setEnabled(
            len(texto) == 6 and texto.isdigit())

    def verificar(self):
        """
        Verifica si el código ingresado es válido y no ha expirado.

        Si es correcto, avanza a la ventana de restablecer contraseña.
        Si es incorrecto, muestra un mensaje de error.
        """
        codigo = self.ventana.input_codigo.text().strip()
        if not codigo:
            QMessageBox.warning(self.ventana, "Campo requerido",
                                "Por favor ingresa el código.")
            return

        if verificar_codigo_recuperacion(self.email, codigo):
            QMessageBox.information(
                self.ventana, "Código válido", "✅ Código verificado correctamente.")
            self.cerrar()

            # Mostrar la ventana de restablecer contraseña
            from controladores.restablecer_controlador import RestablecerControlador
            self.restablecer = RestablecerControlador(self.email)
            self.restablecer.senal_volver_login.connect(self.volver_al_login)

            self.restablecer.mostrar()

        else:
            QMessageBox.critical(self.ventana, "Código inválido",
                                 "❌ El código ingresado no es válido o ha expirado.")

    def actualizar_tiempo(self):
        """
        Actualiza la cuenta atrás visible. Si llega a 0, muestra mensaje de expiración.
        """
        self.tiempo_restante = self.tiempo_restante.addSecs(-1)
        minutos = self.tiempo_restante.minute()
        segundos = self.tiempo_restante.second()

        self.ventana.label_tiempo.setText(
            f"<span style='color:black;'>El código expira en: </span>"
            f"<span style='color:orange; font-weight:bold;'>{minutos}:{segundos:02d}</span>"
        )

        if self.tiempo_restante == QTime(0, 0, 0):
            self.timer.stop()
            self.ventana.label_tiempo.setText(
                "<span style='color:red; font-weight:bold;'>⛔ Código expirado</span>")

    def volver_al_login(self):
        """
        Se ejecuta tras restablecer la contraseña, emitiendo la señal para volver al login.
        """
        self.senal_codigo_valido.emit(self.email)
