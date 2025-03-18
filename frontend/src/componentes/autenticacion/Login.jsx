import React from 'react';
import logo from '../../assets/logo.jpg';

export default function Login() {

    // Maneja el envío del formulario
    const handleSubmit = (event) => {
        event.preventDefault(); // Evita la recarga de la página
        console.log("Inicio de sesión enviado");
        // Aquí puedes agregar la lógica de autenticación
    };

    return (
        <div className="container d-flex flex-column justify-content-center align-items-center vh-100">
            {/* Logo grande y centrado */}
            <img src={logo} alt="Logo del Taller" className="mb-4" style={{ maxWidth: '300px' }} />

            {/* Tarjeta del formulario */}
            <div className="card p-4 shadow-lg" style={{ width: '24rem' }}>
                <h2 className="text-center mb-4 arial-bold-italic">
                    <span className="text-rey">Iniciar</span> <span className="text-boxes">Sesión</span>
                </h2>
                {/* Formulario con el evento onSubmit */}
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Correo electrónico</label>
                        <input type="email" className="form-control" placeholder="👤 usuario@correo.com" title="Introduce tu correo electrónico registrado" required />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Contraseña</label>
                        <input type="password" className="form-control" placeholder="🔒 ********" title="Introduce tu contraseña segura" required />
                    </div>
                    {/* Botón submit para que el Enter funcione */}
                    <button type="submit" className="btn btn-primary w-100">Entrar</button>
                    <div className="text-center mt-2">
                        <a href="#" className="text-decoration-none">¿Olvidaste tu contraseña?</a>
                    </div>
                </form>
            </div>
        </div>
    );
}
