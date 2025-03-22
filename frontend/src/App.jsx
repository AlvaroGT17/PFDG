import { Routes, Route } from "react-router-dom";
import Login from "./componentes/autenticacion/Login";
import Dashboard from "./componentes/Dashboard";
import RecuperarCuenta from "./componentes/autenticacion/RecuperarCuenta";
import VerificarCodigo from "./componentes/autenticacion/VerificarCodigo";
import NuevaContraseña from "./componentes/autenticacion/NuevaContraseña";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/recuperar-cuenta" element={<RecuperarCuenta />} />
      <Route path="/verificar-codigo" element={<VerificarCodigo />} />
      <Route path="/nueva-contraseña" element={<NuevaContraseña />} />
      <Route path="*" element={<Login />} /> {/* Fallback por si la ruta no existe */}
    </Routes>
  );
}
