import api from "./api";

export const iniciarSesion = async (email, password) => {
    try {
        const respuesta = await api.post("/auth/login", { email, password });

        if (respuesta.data.exito) {
            // Guardar el token en localStorage
            localStorage.setItem("token", respuesta.data.token);
        }

        return respuesta.data;
    } catch (error) {
        return { exito: false, mensaje: "Error en la autenticación", error: error.response?.data || error.message };
    }
};
