import bcrypt


def encriptar_contrasena(contrasena_plana: str) -> str:
    hashed = bcrypt.hashpw(contrasena_plana.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hash.encode("utf-8"))


if __name__ == "__main__":
    print("🧪 Prueba de encriptación y verificación de contraseña con bcrypt")

    contrasena = input("🔐 Introduce una contraseña a cifrar: ")
    hash_generado = encriptar_contrasena(contrasena)

    print(f"\n📝 Hash generado:\n{hash_generado}\n")

    intento = input("👤 Introduce la contraseña nuevamente para verificar: ")

    if verificar_contrasena(intento, hash_generado):
        print("✅ Contraseña correcta")
    else:
        print("❌ Contraseña incorrecta")
