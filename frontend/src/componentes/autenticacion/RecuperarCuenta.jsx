import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../../styles/recuperarCuenta.css";


export default function RecuperarCuenta() {
    const [email, setEmail] = useState('');
    const [mensaje, setMensaje] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://localhost:1983/api/auth/recuperar-cuenta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('email', email);
                navigate('/verificar-codigo');
            } else {
                setMensaje(data.error);
            }
        } catch (error) {
            console.error("Error en la solicitud de recuperación:", error);
            setMensaje("Error al enviar el código. Inténtalo de nuevo.");
        }
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2 className="arial-bold-italic text-rey text-center">
                    Recuperar <span className="text-boxes">cuenta</span>
                </h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Introduce el correo electrónicoasociado a tu cuenta:</label>
                        <input
                            type="email"
                            className="form-control"
                            placeholder="Introduce tu correo"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Enviar Código</button>
                </form>
                {mensaje && <p className="text-danger mt-3">{mensaje}</p>}
            </div>
        </div>
    );
}
