"""
Módulo de pruebas unitarias para la interfaz `VentanaClientes`.

Estas pruebas se centran en verificar la correcta creación de la ventana,
su estructura visual básica, los campos de búsqueda y la presencia de
botones funcionales, sin conectar con la lógica del controlador ni con
la base de datos.

Autor: Cresnik
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

from PySide6.QtWidgets import QToolButton, QLineEdit, QLabel
from vistas.ventana_clientes import VentanaClientes


def iniciar_ventana_clientes():
    """
    Inicializa la ventana de gestión de clientes para pruebas aisladas.
    """
    return VentanaClientes()


def test_clientes_campos_busqueda(qtbot):
    """
    Verifica que los tres campos de búsqueda estén correctamente creados
    y accesibles desde el objeto principal.
    """
    ventana = iniciar_ventana_clientes()
    qtbot.addWidget(ventana)
    ventana.show()

    campos = ventana.findChildren(QLineEdit)
    assert ventana.input_buscar_nombre in campos
    assert ventana.input_buscar_dni in campos
    assert ventana.input_buscar_telefono in campos


def test_clientes_botones_principales(qtbot):
    """
    Verifica que la ventana contiene los botones principales:
    Registrar, Modificar, Limpiar, Eliminar, Volver.
    """
    ventana = iniciar_ventana_clientes()
    qtbot.addWidget(ventana)
    ventana.show()

    botones = ventana.findChildren(QToolButton)
    textos = [b.text().lower() for b in botones]

    assert any("registrar" in texto for texto in textos)
    assert any("modificar" in texto for texto in textos)
    assert any("limpiar" in texto for texto in textos)
    assert any("eliminar" in texto for texto in textos)
    assert any("volver" in texto for texto in textos)


def test_clientes_ventana_muestra(qtbot):
    """
    Verifica que la ventana de clientes puede mostrarse correctamente.
    """
    ventana = iniciar_ventana_clientes()
    qtbot.addWidget(ventana)
    ventana.show()

    assert ventana.isVisible()


def test_clientes_actualiza_titulo_con_nombre(qtbot):
    """
    Verifica que el título de la ventana se actualiza dinámicamente
    cuando se escribe en el campo de nombre.
    """
    ventana = iniciar_ventana_clientes()
    qtbot.addWidget(ventana)
    ventana.show()

    campo_nombre = ventana.input_nombre
    titulo = ventana.titulo

    campo_nombre.setText("Cresnik")
    qtbot.wait(100)

    assert "CRESNIK" in titulo.text()
    assert "Registrar cliente" in titulo.text()


def test_clientes_estilo_aplicado(qtbot):
    """
    Verifica que se aplica la hoja de estilos al cargar la ventana.
    No valida contenido visual, solo que `setStyleSheet` se haya ejecutado.
    """
    ventana = iniciar_ventana_clientes()
    qtbot.addWidget(ventana)
    ventana.show()

    estilo_aplicado = ventana.styleSheet()
    assert isinstance(estilo_aplicado, str)
    assert len(estilo_aplicado.strip()) > 0
