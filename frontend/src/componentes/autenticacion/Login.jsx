/* eslint-disable */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import logo from '../../assets/logo.jpg';
import { motion } from 'framer-motion';
import { useEffect } from 'react';


export default function Login() {
    const [nombre, setNombre] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const nombreMayus = nombre.trim().toUpperCase();
            const response = await axios.post('http://localhost:1983/api/auth/login', {
                nombre: nombreMayus,
                password,
            });

            console.log('Respuesta del backend:', response.data);
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('usuario', JSON.stringify(response.data.usuario));

            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.message || 'Error al iniciar sesión');
        }
    };


    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            {/* ✅ Logo animado desde la derecha */}
            <motion.div
                initial={{ x: 200, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 1 }}
            >
                <img src={logo} alt="Logo del Taller" className="mb-4" style={{ maxWidth: '300px' }} />
            </motion.div>

            {/* ✅ Tarjeta animada desde la izquierda */}
            <motion.div
                className="card p-4 shadow-lg"
                style={{ width: '24rem' }}
                initial={{ x: -200, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 1 }}
            >
                <h2 className="text-center mb-4 arial-bold-italic">
                    <span className="text-rey">Iniciar</span> <span className="text-boxes">Sesión</span>
                </h2>

                {error && <div className="alert alert-danger text-center">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="👤 Inserte su nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value.toUpperCase())}
                        required
                    />

                    <div className="mb-3">
                        <label className="form-label">Contraseña</label>
                        <input
                            type="password"
                            className="form-control"
                            placeholder="🔒 ********"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            autoComplete="new-password"
                        />
                    </div>

                    <button type="submit" className="btn btn-primary">🔑 Entrar</button>
                    <div className="text-center mt-2">
                        <Link to="/recuperar-cuenta" className="text-decoration-none">
                            ¿Olvidaste tu contraseña?
                        </Link>
                    </div>
                </form>
            </motion.div>
        </div>
    );
}
