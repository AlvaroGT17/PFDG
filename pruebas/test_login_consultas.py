# pruebas/test_login_consultas.py
"""
Pruebas unitarias para el módulo `login_consultas`.

Este conjunto de tests verifica las funciones clave del proceso de autenticación
y recuperación de cuenta del sistema, incluyendo:

- Obtener usuario por nombre o por email.
- Guardar códigos de recuperación.
- Verificar contraseñas con bcrypt.
- Validar códigos de recuperación (con control de expiración).
- Actualizar contraseñas cifradas.

Se utilizan mocks para evitar conexiones reales a la base de datos.

"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import bcrypt
import modelos.login_consultas as login_consultas


# 🔧 Fixture reutilizable que simula una conexión y cursor
@pytest.fixture
def mock_conexion():
    """
    Devuelve una tupla con objetos simulados para conexión y cursor,
    utilizados en la mayoría de los tests que requieren acceso a BD.
    """
    mock_cursor = MagicMock()
    mock_conexion = MagicMock()
    mock_conexion.cursor.return_value = mock_cursor
    return mock_conexion, mock_cursor


def test_obtener_usuario_por_nombre_devuelve_datos(mock_conexion):
    """
    Verifica que `obtener_usuario_por_nombre()` devuelve un diccionario
    con los campos esperados cuando encuentra una coincidencia.
    """
    conexion, cursor = mock_conexion
    cursor.fetchone.return_value = (
        1, "CRESNIK", "RASIEL", "cresnik@example.com", "hash", "ADMINISTRADOR")

    with patch("modelos.login_consultas.obtener_conexion", return_value=conexion):
        usuario = login_consultas.obtener_usuario_por_nombre("Cresnik")

    assert usuario["nombre"] == "CRESNIK"
    assert usuario["rol"] == "ADMINISTRADOR"
    conexion.close.assert_called_once()


def test_obtener_usuario_por_email_devuelve_datos(mock_conexion):
    """
    Verifica que `obtener_usuario_por_email()` devuelve correctamente 
    el ID y nombre del usuario al encontrar coincidencia por correo.
    """
    conexion, cursor = mock_conexion
    cursor.fetchone.return_value = (7, "CRESNIK")

    with patch("modelos.login_consultas.obtener_conexion", return_value=conexion):
        usuario = login_consultas.obtener_usuario_por_email(
            "cresnik@example.com")

    assert usuario["id"] == 7
    assert usuario["nombre"] == "CRESNIK"
    conexion.close.assert_called_once()


def test_guardar_codigo_recuperacion_realiza_update(mock_conexion):
    """
    Verifica que `guardar_codigo_recuperacion()` ejecuta correctamente
    un `UPDATE` en la base de datos y realiza `commit` exitosamente.
    """
    conexion, cursor = mock_conexion

    with patch("modelos.login_consultas.obtener_conexion", return_value=conexion), \
            patch("modelos.login_consultas.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = datetime(2025, 1, 1, 12, 0, 0)

        exito = login_consultas.guardar_codigo_recuperacion(1, "ABC123")

    cursor.execute.assert_called_once()
    conexion.commit.assert_called_once()
    assert exito is True


def test_verificar_contrasena_correcta():
    """
    Comprueba que `verificar_contrasena()` devuelve True si la contraseña
    ingresada coincide con el hash almacenado.
    """
    hash_pw = bcrypt.hashpw(b"1234", bcrypt.gensalt())
    assert login_consultas.verificar_contrasena(
        "1234", hash_pw.decode("utf-8")) is True


def test_verificar_codigo_recuperacion_valido(mock_conexion):
    """
    Verifica que `verificar_codigo_recuperacion()` devuelve True cuando:
    - El código coincide con el almacenado.
    - El código no ha expirado.
    """
    conexion, cursor = mock_conexion
    ahora = datetime.utcnow() + timedelta(minutes=3)
    cursor.fetchone.return_value = ("ABC123", ahora)

    with patch("modelos.login_consultas.obtener_conexion", return_value=conexion):
        valido = login_consultas.verificar_codigo_recuperacion(
            "cresnik@example.com", "ABC123")

    assert valido is True
    conexion.close.assert_called_once()


def test_actualizar_contrasena_realiza_update(mock_conexion):
    """
    Verifica que `actualizar_contrasena()` actualiza correctamente el hash
    de la nueva contraseña en la base de datos, con commit incluido.
    """
    conexion, cursor = mock_conexion

    with patch("modelos.login_consultas.obtener_conexion", return_value=conexion):
        resultado = login_consultas.actualizar_contrasena(
            "cresnik@example.com", "nueva123")

    assert resultado is True
    conexion.commit.assert_called_once()
    conexion.close.assert_called_once()
