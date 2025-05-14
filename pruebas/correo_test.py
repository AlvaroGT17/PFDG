from utilidades.correo import enviar_correo


def probar_envio_correo():
    """
    Llama a la función enviar_correo con datos simulados.
    Se usa en test_correo.py para pruebas controladas.
    """
    nombre = "CRESNIK"
    correo = "cresnik17021983@gmail.com"
    codigo = "123456"
    enviar_correo(correo, nombre, codigo)
