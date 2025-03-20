import { Routes, Route } from "react-router-dom";
import Login from "./componentes/autenticacion/Login";
import Dashboard from "./componentes/Dashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}
