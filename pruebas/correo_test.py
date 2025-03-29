from utilidades.correo import enviar_correo

# CORRECTO
nombre = "CRESNIK"
correo = "cresnik17021983@gmail.com"
codigo = "123456"

print("📤 Enviando correo de prueba...")
try:
    enviar_correo(correo, nombre, codigo)
    print("✅ Correo enviado correctamente.")
except Exception as e:
    print("❌ Falló el envío:", e)
