"""
Módulo de configuración global para Pytest.

Este archivo define fixtures que se aplican automáticamente a todos los tests
del proyecto. Su objetivo principal es evitar que cuadros de diálogo modales 
(QMessageBox) bloqueen la ejecución de los tests unitarios y requieran 
interacción manual del usuario.

Esto permite que las pruebas se ejecuten de forma automatizada, rápida y fluida,
incluso en entornos CI/CD o sin entorno gráfico visible.


"""

import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QMessageBox, QFileDialog


@pytest.fixture(autouse=True, scope="session")
def desactivar_qmessagebox():
    """
    Fixture global y automático que reemplaza los métodos QMessageBox.information,
    QMessageBox.warning y QMessageBox.critical por objetos simulados (MagicMock).

    Esto evita que se abran ventanas emergentes reales durante la ejecución de los tests,
    lo cual podría interrumpirlos o hacer que se queden bloqueados esperando un clic.

    Este mock es aplicable a todos los tests de la sesión sin necesidad de importarlo
    o aplicarlo manualmente en cada archivo de prueba.
    """
    QMessageBox.information = MagicMock()
    QMessageBox.warning = MagicMock()
    QMessageBox.critical = MagicMock()

    # Desactivar QFileDialog.getSaveFileName para que no abra ventana
    QFileDialog.getSaveFileName = MagicMock(
        return_value=("ruta_ficticia.ext", None))
