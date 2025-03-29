import re
from PySide6.QtCore import QObject, Signal, QTimer, QTime
from PySide6.QtWidgets import QMessageBox
from vistas.ventana_verificar import VentanaVerificar
from modelos.login_consultas import verificar_codigo_recuperacion


class VerificarControlador(QObject):
    senal_codigo_valido = Signal(str)
    senal_volver_recuperar = Signal()

    def __init__(self, email):
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
        self.ventana.show()

    def cerrar(self):
        self.timer.stop()
        self.ventana.close()

    def volver(self):
        self.cerrar()
        self.senal_volver_recuperar.emit()

    def handle_cierre_ventana(self, event):
        self.timer.stop()
        self.senal_volver_recuperar.emit()
        event.accept()

    def validar_codigo(self):
        texto = self.ventana.input_codigo.text()
        self.ventana.btn_verificar.setEnabled(
            len(texto) == 6 and texto.isdigit())

    def verificar(self):
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
        self.tiempo_restante = self.tiempo_restante.addSecs(-1)
        minutos = self.tiempo_restante.minute()
        segundos = self.tiempo_restante.second()

        self.ventana.label_tiempo.setText(
            f"<span style='color:black;'>El código expira en: </span><span style='color:orange; font-weight:bold;'>{minutos}:{segundos:02d}</span>"
        )

        if self.tiempo_restante == QTime(0, 0, 0):
            self.timer.stop()
            self.ventana.label_tiempo.setText(
                "<span style='color:red; font-weight:bold;'>⛔ Código expirado</span>")

    def volver_al_login(self):
        self.senal_codigo_valido.emit(self.email)
