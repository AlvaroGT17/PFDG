import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function VerificarCodigo() {
    const [codigo, setCodigo] = useState('');
    const [mensaje, setMensaje] = useState('');
    const navigate = useNavigate();
    const email = localStorage.getItem('email'); // Obtener el email guardado

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://localhost:5000/api/verificar-otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, codigo })
            });

            const data = await response.json();
            if (response.ok) {
                navigate('/nueva-contraseña'); // Redirigir a la pantalla de nueva contraseña
            } else {
                setMensaje(data.error);
            }
        } catch (error) {
            console.error("Error en la verificación del código:", error);
            setMensaje("Código incorrecto. Inténtalo de nuevo.");
        }
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2 className="text-center mb-4">Verificar Código</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Código OTP</label>
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
                {mensaje && <p className="text-danger mt-3">{mensaje}</p>}
            </div>
        </div>
    );
}
