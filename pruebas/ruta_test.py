from utilidades.rutas import obtener_ruta_absoluta

try:
    print("🔍 Probando cargar CSS de verificación...")
    ruta = obtener_ruta_absoluta("css/verificar_codigo.css")
    print(f"✅ Ruta encontrada:\n{ruta}")
except Exception as e:
    print(f"❌ ERROR: {e}")
