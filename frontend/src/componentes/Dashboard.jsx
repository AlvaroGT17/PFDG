import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/dashboard.css";
import ficharIcono from '../assets/iconos/fichar.png';
import reparacionIcono from '../assets/iconos/reparacion.png';
import historialIcon from '../assets/iconos/historial.png';
import clientesIcon from '../assets/iconos/clientes.png';
import vehiculosIcon from '../assets/iconos/vehiculos.png';
import facturacionIcon from '../assets/iconos/facturacion.png';
import reportesIcon from '../assets/iconos/reportes.png';
import usuariosIcon from '../assets/iconos/usuarios.png';
import cerrarSesionIcon from '../assets/iconos/cerrar.png';



export default function Dashboard() {
    const [usuario, setUsuario] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const usuarioGuardado = localStorage.getItem('usuario');
        if (usuarioGuardado) {
            setUsuario(JSON.parse(usuarioGuardado));
        } else {
            window.location.hash = '/login';
            window.location.reload();
        }
    }, [navigate]);

    const cerrarSesion = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');

        // ✅ Forzar recarga completa para evitar estados cacheados
        navigate('/login');

    };


    return (
        <div className="dashboard-container">
            <div className="dashboard-card">
                <h2 className="dashboard-titulo">
                    Bienvenido, <span className="text-boxes">{usuario?.nombre}</span>
                </h2>
                <p className="dashboard-rol">Rol: <strong>{usuario?.rol}</strong></p>

                <div className="dashboard-botones">

                    {/* 🕒 Fichar */}
                    <button className="btn-dashboard">
                        <img src={ficharIcono} alt="Fichar" className="btn-icono" />
                        <span className="btn-texto">Fichar</span>
                    </button>

                    {/* 🔧 Reparaciones */}
                    <button className="btn-dashboard">
                        <img src={reparacionIcono} alt="Reparaciones" className="btn-icono" />
                        <span className="btn-texto">Reparaciones</span>
                    </button>

                    {/* 🧾 Historial */}
                    <button className="btn-dashboard">
                        <img src={historialIcon} alt="Historial" className="btn-icono" />
                        <span className="btn-texto">Historial</span>
                    </button>

                    {/* 👥 Clientes */}
                    <button className="btn-dashboard">
                        <img src={clientesIcon} alt="Clientes" className="btn-icono" />
                        <span className="btn-texto">Clientes</span>
                    </button>

                    {/* 🚗 Vehículos */}
                    <button className="btn-dashboard">
                        <img src={vehiculosIcon} alt="Vehículos" className="btn-icono" />
                        <span className="btn-texto">Vehículos</span>
                    </button>

                    {/* 💸 Facturación */}
                    <button className="btn-dashboard">
                        <img src={facturacionIcon} alt="Facturación" className="btn-icono" />
                        <span className="btn-texto">Facturación</span>
                    </button>

                    {/* 📊 Reportes */}
                    <button className="btn-dashboard">
                        <img src={reportesIcon} alt="Reportes" className="btn-icono" />
                        <span className="btn-texto">Reportes</span>
                    </button>

                    {/* 👤 Usuarios */}
                    <button className="btn-dashboard">
                        <img src={usuariosIcon} alt="Usuarios" className="btn-icono" />
                        <span className="btn-texto">Usuarios</span>
                    </button>

                    {/* 🔐 Cerrar sesión */}
                    <button className="btn-dashboard" onClick={cerrarSesion}>
                        <img src={cerrarSesionIcon} alt="Cerrar sesión" className="btn-icono" />
                        <span className="btn-texto">Cerrar sesión</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
