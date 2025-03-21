import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function VerificarCodigo() {
    const [codigo, setCodigo] = useState('');
    const [mensaje, setMensaje] = useState('');
    const navigate = useNavigate();
    const email = localStorage.getItem('email'); // Obtener el email guardado

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
                // Código correcto → redirigir a pantalla para nueva contraseña
                navigate('/nueva-contraseña');
            } else {
                setMensaje(data.message || "Código incorrecto.");
            }
        } catch (error) {
            console.error("Error en la verificación del código:", error);
            setMensaje("Hubo un error al verificar el código.");
        }
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2><span className="text-rey">Verificar</span> <span className="text-boxes">codigo</span></h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Introdudca el código de seguridad</label>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Introduce el código recibido"
                            value={codigo}
                            onChange={(e) => setCodigo(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Validar Código</button>
                </form>
                {mensaje && <p className="text-danger mt-3 text-center">{mensaje}</p>}
            </div>
        </div>
    );
}
