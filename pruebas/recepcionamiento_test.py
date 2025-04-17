from PySide6.QtWidgets import QApplication
from vistas.ventana_recepcionamiento import VentanaRecepcionamiento
from controladores.recepcionamiento_controlador import RecepcionamientoControlador
from PySide6.QtGui import QPainter, QPixmap, QPen
from PySide6.QtCore import Qt, QPoint
import sys
import os
from datetime import date


def simular_firma(path):
    """Genera una firma de prueba simple en la ruta especificada."""
    pixmap = QPixmap(400, 100)
    pixmap.fill(Qt.white)

    painter = QPainter(pixmap)
    pen = QPen(Qt.black, 2)
    painter.setPen(pen)
    painter.drawText(QPoint(150, 60), "Firma de prueba")
    painter.end()

    pixmap.save(path, "PNG")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear la ventana
    ventana = VentanaRecepcionamiento()

    # Datos simulados de prueba
    datos_prueba = {
        "tipos": [{"nombre": "Turismo", "categoria": "Terrestre"}],
        "categorias": ["Terrestre", "Acuático"],
        "combustibles": ["Gasolina", "Diésel", "Eléctrico", "Híbrido"],
        "motivos": [{"id": 1, "nombre": "Mantenimiento"}, {"id": 2, "nombre": "Avería"}],
        "urgencias": [{"id": 1, "descripcion": "Alta"}, {"id": 2, "descripcion": "Media"}, {"id": 3, "descripcion": "Baja"}],
        "usuario_id": 6,
        "estado_id": 1,
    }

    # Cargar controlador con ventana y datos simulados
    controlador = RecepcionamientoControlador(ventana, datos_prueba)

    # Simular firma de prueba
    firma_path = os.path.join(os.getcwd(), "firma_temporal.png")
    simular_firma(firma_path)

    # CLIENTE 5 - Carlos Gómez Hernández
    ventana.input_nombre.setText("Carlos Gómez Hernández")
    ventana.input_dni.setText("23456789B")
    ventana.input_telefono.setText("622345678")
    ventana.input_email.setText("carlos.gomez@example.com")
    ventana.input_direccion.setText("Avda. de la Paz 45")

    # Vehículo vinculado - Matrícula: 4567DEF
    ventana.input_matricula.setCurrentText("4567DEF")
    ventana.input_marca.setText("OPEL")
    ventana.input_modelo.setText("Corsa")
    ventana.input_color.setText("Negro")
    ventana.input_anio.setText("2020")
    ventana.input_kilometros.setText("85000")
    ventana.combo_combustible.setCurrentText("Gasolina")
    ventana.input_vin.setText("W0L0XEP08R4000004")
    ventana.combo_categoria.setCurrentText("Terrestre")
    ventana.combo_tipo.setCurrentText("Turismo")

    ventana.combo_motivo.setCurrentText("Mantenimiento")
    ventana.combo_urgencia.setCurrentText("Alta")
    ventana.fecha_recepcion.setDate(date.today())

    ventana.check_arranca.setChecked(True)
    ventana.check_grua.setChecked(False)
    ventana.check_itv.setChecked(True)
    ventana.check_presupuesto_escrito.setChecked(True)
    ventana.check_seguro.setChecked(True)
    ventana.input_compania.setText("Mutua Rey S.A.")

    ventana.input_ultima_revision.setText("15/02/2024")
    ventana.input_max_autorizado.setText("500")
    ventana.input_valor_estimado.setText("2000")
    ventana.input_estado_exterior.setPlainText("Arañazos en lateral izquierdo")
    ventana.input_estado_interior.setPlainText("Buen estado general")
    ventana.input_observaciones.setPlainText(
        "Se requiere diagnóstico completo")

    ventana.input_correo.setText("cresnik17021983@gmail.com")
    ventana.checkbox_ruta_predeterminada.setChecked(True)
    ventana.checkbox_enviar_correo.setChecked(False)
    ventana.checkbox_imprimir.setChecked(False)

    ventana.show()
    sys.exit(app.exec())


# para abrir este mofdulo, ejecuta el siguiente comando en la terminal:
# python -m pruebas.recepcionamiento_test
