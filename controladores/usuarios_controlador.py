from PySide6.QtWidgets import QMessageBox
from vistas.ventana_usuarios import VentanaUsuarios
from modelos.usuarios_consultas import obtener_roles, crear_usuario, existe_usuario_por_nombre, existe_usuario_por_email
import re


class UsuariosControlador:
    def __init__(self, ventana_anterior):
        self.ventana = VentanaUsuarios()
        self.ventana_anterior = ventana_anterior

        self.ventana.boton_volver.clicked.connect(self.volver)
        self.ventana.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.ventana.boton_crear.clicked.connect(self.crear_usuario)

        self.cargar_roles()
        self.ventana.show()

    def cargar_roles(self):
        roles = obtener_roles()
        self.ventana.combo_rol.clear()
        self.ventana.combo_rol.addItem("Seleccione un rol", None)
        for id_rol, nombre in roles:
            self.ventana.combo_rol.addItem(nombre, id_rol)

    def limpiar_campos(self):
        self.ventana.input_nombre.clear()
        self.ventana.input_apellido.clear()
        self.ventana.input_email.clear()
        self.ventana.input_password.clear()
        self.ventana.input_repetir.clear()
        self.ventana.combo_rol.setCurrentIndex(0)

    def volver(self):
        self.ventana.cierre_autorizado = True
        self.ventana.close()
        self.ventana_anterior.show()

    def crear_usuario(self):
        nombre = self.ventana.input_nombre.text().strip()
        apellido = self.ventana.input_apellido.text().strip()
        email = self.ventana.input_email.text().strip()
        password = self.ventana.input_password.text()
        repetir = self.ventana.input_repetir.text()
        rol_id = self.ventana.combo_rol.currentData()

        if not nombre or not apellido or not email or not password or not repetir:
            self.mostrar_error("Todos los campos son obligatorios.")
            return

        if rol_id is None:
            self.mostrar_error("Debe seleccionar un rol válido.")
            return

        if not self.validar_email(email):
            self.mostrar_error("El correo electrónico no es válido.")
            return

        if password != repetir:
            self.mostrar_error("Las contraseñas no coinciden.")
            return

        if existe_usuario_por_nombre(nombre):
            self.mostrar_error(
                "Ya existe un usuario con ese nombre. Por favor, elige otro.")
            return

        if existe_usuario_por_email(email):
            self.mostrar_error(
                "Ya existe un usuario con ese correo electrónico.")
            return

        exito = crear_usuario(nombre, apellido, email, password, rol_id)
        if exito:
            self.mostrar_info("Usuario creado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("Ocurrió un error al crear el usuario.")

    def validar_email(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self.ventana, "Error", mensaje)

    def mostrar_info(self, mensaje):
        QMessageBox.information(self.ventana, "Información", mensaje)


class UsuariosControlador:
    """
    Controlador de la ventana para crear nuevos usuarios en el sistema.

    Permite ingresar nombre, apellido, correo, contraseña, rol y valida toda la
    información antes de llamar al modelo para insertar un nuevo registro.
    """

    def __init__(self, ventana_anterior):
        """
        Inicializa la ventana, conecta los eventos y carga los roles disponibles.

        Args:
            ventana_anterior: Referencia a la ventana desde la que se abre esta.
        """
        self.ventana = VentanaUsuarios()
        self.ventana_anterior = ventana_anterior

        self.ventana.boton_volver.clicked.connect(self.volver)
        self.ventana.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.ventana.boton_crear.clicked.connect(self.crear_usuario)

        self.cargar_roles()
        self.ventana.show()

    def cargar_roles(self):
        """
        Carga los roles desde la base de datos y los añade al combo de selección.
        """
        roles = obtener_roles()
        self.ventana.combo_rol.clear()
        self.ventana.combo_rol.addItem("Seleccione un rol", None)
        for id_rol, nombre in roles:
            self.ventana.combo_rol.addItem(nombre, id_rol)

    def limpiar_campos(self):
        """
        Limpia todos los campos del formulario de creación de usuario.
        """
        self.ventana.input_nombre.clear()
        self.ventana.input_apellido.clear()
        self.ventana.input_email.clear()
        self.ventana.input_password.clear()
        self.ventana.input_repetir.clear()
        self.ventana.combo_rol.setCurrentIndex(0)

    def volver(self):
        """
        Cierra esta ventana y vuelve a la anterior.
        """
        self.ventana.cierre_autorizado = True
        self.ventana.close()
        self.ventana_anterior.show()

    def crear_usuario(self):
        """
        Valida los campos introducidos por el usuario y, si todo es correcto,
        crea un nuevo usuario en la base de datos.

        Muestra mensajes de error si falta algún campo, si el email no es válido,
        si las contraseñas no coinciden o si el usuario ya existe.
        """
        nombre = self.ventana.input_nombre.text().strip()
        apellido = self.ventana.input_apellido.text().strip()
        email = self.ventana.input_email.text().strip()
        password = self.ventana.input_password.text()
        repetir = self.ventana.input_repetir.text()
        rol_id = self.ventana.combo_rol.currentData()

        if not nombre or not apellido or not email or not password or not repetir:
            self.mostrar_error("Todos los campos son obligatorios.")
            return

        if rol_id is None:
            self.mostrar_error("Debe seleccionar un rol válido.")
            return

        if not self.validar_email(email):
            self.mostrar_error("El correo electrónico no es válido.")
            return

        if password != repetir:
            self.mostrar_error("Las contraseñas no coinciden.")
            return

        if existe_usuario_por_nombre(nombre):
            self.mostrar_error(
                "Ya existe un usuario con ese nombre. Por favor, elige otro.")
            return

        if existe_usuario_por_email(email):
            self.mostrar_error(
                "Ya existe un usuario con ese correo electrónico.")
            return

        exito = crear_usuario(nombre, apellido, email, password, rol_id)
        if exito:
            self.mostrar_info("Usuario creado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("Ocurrió un error al crear el usuario.")

    def validar_email(self, email):
        """
        Valida el formato del correo electrónico con una expresión regular.

        Args:
            email (str): Dirección de correo a validar.

        Returns:
            bool: True si el email tiene un formato válido, False en caso contrario.
        """
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def mostrar_error(self, mensaje):
        """
        Muestra un cuadro de diálogo con un mensaje de error.

        Args:
            mensaje (str): Texto del mensaje a mostrar.
        """
        QMessageBox.critical(self.ventana, "Error", mensaje)

    def mostrar_info(self, mensaje):
        """
        Muestra un cuadro de diálogo con un mensaje informativo.

        Args:
            mensaje (str): Texto del mensaje a mostrar.
        """
        QMessageBox.information(self.ventana, "Información", mensaje)
