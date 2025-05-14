# pruebas/test_presentacion.py
from vistas.ventana_presentacion import VentanaPresentacion


def test_presentacion_se_muestra(qtbot):
    ventana = VentanaPresentacion()
    qtbot.addWidget(ventana)

    # 🔧 Mostrar explícitamente
    ventana.show()
    qtbot.waitExposed(ventana)  # Esperar a que se exponga

    # ✅ Verificar que se está mostrando correctamente
    assert ventana.isVisible()
    assert ventana.width() > 0
    assert ventana.height() > 0
