import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
    const [usuario, setUsuario] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        // Obtener el usuario desde localStorage
        const usuarioGuardado = localStorage.getItem('usuario');

        if (usuarioGuardado) {
            setUsuario(JSON.parse(usuarioGuardado));
        } else {
            navigate('/'); // Si no hay usuario, redirigir al login
        }
    }, [navigate]);

    return (
        <div className="container text-center mt-5">
            <h1>Bienvenido, {usuario?.nombre} 👋</h1>
            <p>Tu rol es: <strong>{usuario?.rol}</strong></p>
            <button className="btn btn-danger" onClick={() => {
                localStorage.removeItem('token');
                localStorage.removeItem('usuario');
                navigate('/');
            }}>
                Cerrar sesión
            </button>
        </div>
    );
}
