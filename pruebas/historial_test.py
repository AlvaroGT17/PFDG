from PySide6.QtWidgets import QApplication
import sys
from controladores.historial_controlador import HistorialControlador

app = QApplication(sys.argv)

# Cambia esto según el usuario:
usuario_id = 12
es_admin = False  # o False

controlador = HistorialControlador(usuario_id, es_admin)
controlador.mostrar()

sys.exit(app.exec())

# Para ejecutar este escript ejecuta: ----  python -m pruebas.historial_test ----
