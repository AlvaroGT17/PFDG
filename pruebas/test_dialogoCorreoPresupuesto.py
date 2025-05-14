from PySide6.QtWidgets import QLineEdit
from pruebas.dialogoCorreoPresupuesto_test import iniciar_dialogo_correo_presupuesto


def test_dialogo_correo_se_muestra(qtbot):
    dialogo = iniciar_dialogo_correo_presupuesto()
    qtbot.addWidget(dialogo)
    dialogo.show()

    assert dialogo.isVisible()


def test_dialogo_correo_campo_editable(qtbot):
    dialogo = iniciar_dialogo_correo_presupuesto()
    qtbot.addWidget(dialogo)
    dialogo.show()

    campo = dialogo.findChild(QLineEdit)
    assert campo is not None

    texto_prueba = "cliente@ejemplo.com"
    campo.setText(texto_prueba)
    assert dialogo.obtener_correo() == texto_prueba
