import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function NuevaContraseña() {
    const [password, setPassword] = useState('');
    const [confirmar, setConfirmar] = useState('');
    const [mensaje, setMensaje] = useState('');
    const navigate = useNavigate();
    const email = localStorage.getItem('email');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMensaje('');

        if (password !== confirmar) {
            setMensaje('Las contraseñas no coinciden.');
            return;
        }

        try {
            const response = await fetch('http://localhost:1983/api/auth/nueva-contrasena', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, nuevaContrasena: password })
            });

            const data = await response.json();

            if (response.ok) {
                // Limpiar localStorage y redirigir
                localStorage.removeItem('email');
                navigate('/login');
            } else {
                setMensaje(data.message || 'Error al cambiar la contraseña.');
            }
        } catch (error) {
            console.error("Error al cambiar la contraseña:", error);
            setMensaje("Hubo un error. Inténtalo más tarde.");
        }
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2 className="text-center mb-4">Nueva Contraseña</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Nueva contraseña</label>
                        <input
                            type="password"
                            className="form-control"
                            placeholder="********"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Confirmar contraseña</label>
                        <input
                            type="password"
                            className="form-control"
                            placeholder="********"
                            value={confirmar}
                            onChange={(e) => setConfirmar(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Cambiar Contraseña</button>
                </form>
                {mensaje && <p className="text-danger mt-3 text-center">{mensaje}</p>}
            </div>
        </div>
    );
}
