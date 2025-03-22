import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import "../../styles/verificarCodigo.css";

export default function VerificarCodigo() {
    const [codigo, setCodigo] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [mostrarReenvio, setMostrarReenvio] = useState(false);
    const [tiempoRestante, setTiempoRestante] = useState(300); // 5 minutos (300 segundos)
    const navigate = useNavigate();
    const email = localStorage.getItem('email');

    // ✅ CUENTA REGRESIVA (5 minutos)
    useEffect(() => {
        if (tiempoRestante > 0) {
            const intervalo = setInterval(() => {
                setTiempoRestante((prev) => prev - 1);
            }, 1000);

            return () => clearInterval(intervalo);
        } else {
            setMostrarReenvio(true); // Mostrar el botón al expirar el tiempo
            setMensaje("El código ha expirado. Solicita uno nuevo.");
        }
    }, [tiempoRestante]);

    // ✅ FUNCIÓN PARA VALIDAR CÓDIGO
    const handleSubmit = async (event) => {
        event.preventDefault();
        setMensaje('');

        try {
            const response = await fetch('http://localhost:1983/api/auth/verificar-codigo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, codigo })
            });

            const data = await response.json();

            if (response.ok) {
                navigate('/nueva-contraseña');
            } else {
                setMensaje(data.message || "Código incorrecto o expirado.");
                setMostrarReenvio(true); // Mostrar botón si el código es incorrecto
            }
        } catch (error) {
            console.error("Error en la verificación del código:", error);
            setMensaje("Código incorrecto o expirado.");
            setMostrarReenvio(true);
        }
    };

    // ✅ FUNCIÓN PARA REENVIAR CÓDIGO
    const reenviarCodigo = async () => {
        try {
            const response = await fetch('http://localhost:1983/api/auth/recuperar-cuenta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok) {
                setMensaje('Nuevo código enviado al correo.');
                setMostrarReenvio(false); // Ocultar botón después de reenviar
                setTiempoRestante(300); // Reiniciar cuenta regresiva
            } else {
                setMensaje(data.message || 'Error al reenviar el código.');
            }
        } catch (error) {
            console.error("Error al reenviar el código:", error);
            setMensaje("Error al reenviar el código.");
        }
    };

    // ✅ FORMATEAR TIEMPO (minutos y segundos)
    const formatTiempo = (segundos) => {
        const minutos = Math.floor(segundos / 60);
        const segRestantes = segundos % 60;
        return `${minutos}:${segRestantes < 10 ? '0' : ''}${segRestantes}`;
    };

    return (
        <div className="verificar-codigo-container">
            <div className="verificar-codigo-card">
                <h2 className="arial-bold-italic text-rey text-center">
                    Verificar <span className="text-boxes">código</span>
                </h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Introduce el código de seguridad</label>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Introduce el código recibido"
                            value={codigo}
                            onChange={(e) => setCodigo(e.target.value)}
                            required
                        />
                    </div>

                    {/* Botones alineados correctamente */}
                    <div className="botones-container">
                        <button type="submit" className="btn btn-danger btn-tercio">
                            Validar Código
                        </button>

                        {/* Mostrar botón de reenvío solo si el código expiró o fue incorrecto */}
                        {mostrarReenvio && (
                            <button type="button" className="btn btn-secondary btn-tercio" onClick={reenviarCodigo}>
                                Reenviar código
                            </button>
                        )}
                    </div>

                    {/* Mostrar cuenta regresiva si el código no ha expirado */}
                    {tiempoRestante > 0 && (
                        <p className="text-center mt-2 text-warning">
                            El código expira en: <strong>{formatTiempo(tiempoRestante)}</strong>
                        </p>
                    )}
                </form>

                {/* Mensaje con letras blancas */}
                {mensaje && (
                    <p className="text-white mt-3 text-center">
                        ✅ {mensaje}
                    </p>
                )}
            </div>
        </div>
    );
}
