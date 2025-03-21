import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import Login from './componentes/autenticacion/Login.jsx';
import RecuperarCuenta from './componentes/autenticacion/RecuperarCuenta.jsx';
import VerificarCodigo from './componentes/autenticacion/VerificarCodigo.jsx';
import NuevaContraseña from './componentes/autenticacion/NuevaContraseña.jsx';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css'; // Asegurar que el CSS se carga aquí

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/recuperar-cuenta" element={<RecuperarCuenta />} />
        <Route path="/verificar-codigo" element={<VerificarCodigo />} />
        <Route path="/nueva-contraseña" element={<NuevaContraseña />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
