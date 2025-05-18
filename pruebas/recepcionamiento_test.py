# pruebas/recepcionamiento_test.py
"""
Script visual para lanzar la ventana de recepción de vehículos con datos de prueba.

Este archivo permite ejecutar `VentanaRecepcionamiento` de forma independiente
para realizar pruebas visuales, comprobar estilos, disposición de campos y 
funcionalidades básicas, sin necesidad de levantar la aplicación completa.

Puede utilizarse también como función auxiliar en tests unitarios.

Uso recomendado:
    python -m pruebas.recepcionamiento_test
"""

import sys
import os
from datetime import date
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QPixmap, QPen
from PySide6.QtCore import Qt, QPoint
from vistas.ventana_recepcionamiento import VentanaRecepcionamiento
from controladores.recepcionamiento_controlador import RecepcionamientoControlador


def simular_firma(path):
    """
    Genera una imagen PNG de firma de prueba y la guarda en el path especificado.

    Args:
        path (str): Ruta de archivo donde se guardará la imagen simulada.
    """
    pixmap = QPixmap(400, 100)
    pixmap.fill(Qt.white)

    painter = QPainter(pixmap)
    pen = QPen(Qt.black, 2)
    painter.setPen(pen)
    painter.drawText(QPoint(150, 60), "Firma de prueba")
    painter.end()

    pixmap.save(path, "PNG")


def iniciar_ventana_recepcionamiento():
    """
    Prepara una instancia de la ventana de recepción de vehículos con datos pre-cargados
    para pruebas visuales o funcionales.

    Returns:
        VentanaRecepcionamiento: Ventana completamente configurada con datos simulados.
    """
    ventana = VentanaRecepcionamiento()

    datos_prueba = {
        "tipos": [{"nombre": "Turismo", "categoria": "Terrestre"}],
        "categorias": ["Terrestre", "Acuático"],
        "combustibles": ["Gasolina", "Diésel", "Eléctrico", "Híbrido"],
        "motivos": [{"id": 1, "nombre": "Mantenimiento"}, {"id": 2, "nombre": "Avería"}],
        "urgencias": [{"id": 1, "descripcion": "Alta"}, {"id": 2, "descripcion": "Media"}, {"id": 3, "descripcion": "Baja"}],
        "usuario_id": 6,
        "estado_id": 1,
    }

    controlador = RecepcionamientoControlador(ventana, datos_prueba)

    firma_path = os.path.join(os.getcwd(), "firma_temporal.png")
    simular_firma(firma_path)

    # Datos cliente y vehículo
    ventana.input_nombre.setText("Carlos Gómez Hernández")
    ventana.input_dni.setText("23456789B")
    ventana.input_telefono.setText("622345678")
    ventana.input_email.setText("carlos.gomez@example.com")
    ventana.input_direccion.setText("Avda. de la Paz 45")

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

    # Otros campos
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

    return ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = iniciar_ventana_recepcionamiento()
    ventana.show()
    sys.exit(app.exec())
