import React, { useState } from 'react';
import axios from 'axios';
import logo from '../../assets/logo.jpg';
import '../../index.css';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post('http://localhost:1983/api/auth/login', { email, password });

            // Guardar token en localStorage
            localStorage.setItem('token', response.data.token);

            // Mostrar mensaje de éxito (Puedes redirigir a otra página)
            alert('¡Inicio de sesión exitoso!');
        } catch (err) {
            setError(err.response?.data?.message || 'Error al iniciar sesión');
        }
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            <img src={logo} alt="Logo del Taller" className="mb-4" style={{ maxWidth: '300px' }} />

            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2 className="text-center mb-4 arial-bold-italic">
                    <span className="text-rey">Iniciar</span> <span className="text-boxes">Sesión</span>
                </h2>

                {error && <div className="alert alert-danger text-center">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Correo electrónico</label>
                        <input
                            type="email"
                            className="form-control"
                            placeholder="👤 usuario@correo.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Contraseña</label>
                        <input
                            type="password"
                            className="form-control"
                            placeholder="🔒 ********"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" className="btn btn-primary">Entrar</button>
                    <div className="text-center mt-2">
                        <a href="#" className="text-decoration-none">¿Olvidaste tu contraseña?</a>
                    </div>
                </form>
            </div>
        </div>
    );
}
