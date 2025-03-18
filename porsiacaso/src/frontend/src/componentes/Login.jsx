import { useState } from "react";
import { iniciarSesion } from "../servicios/usuariosServicio";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";
import Card from "react-bootstrap/Card";
import Image from "react-bootstrap/Image";
import fondo from "../assets/fondo.jpg"; // Cambia por un fondo con los colores del taller
import logo from "../assets/logo.jpg"; // Logo del taller

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        const respuesta = await iniciarSesion(email, password);
        if (respuesta.exito) {
            localStorage.setItem("token", respuesta.token);
            navigate("/dashboard"); // Redirigir tras el login
        } else {
            setError(respuesta.mensaje);
        }
    };

    return (
        <div
            className="d-flex justify-content-center align-items-center vh-100"
            style={{
                backgroundImage: `url(${fondo})`,
                backgroundSize: "cover",
                backgroundPosition: "center",
                minHeight: "100vh",
            }}
        >
            <Container className="d-flex flex-column align-items-center">
                {/* Logo */}
                <Image src={logo} alt="Logo Taller" className="mb-4" fluid style={{ maxWidth: "200px" }} />

                {/* Tarjeta del Login */}
                <Card className="p-4 shadow-lg" style={{ width: "100%", maxWidth: "400px", background: "rgba(255, 255, 255, 0.9)", borderRadius: "10px" }}>
                    <Card.Body>
                        <h2 className="text-center mb-4">Iniciar Sesión</h2>
                        {error && <Alert variant="danger">{error}</Alert>}
                        <Form onSubmit={handleLogin}>
                            <Form.Group className="mb-3">
                                <Form.Label>Email</Form.Label>
                                <Form.Control
                                    type="email"
                                    placeholder="Ingrese su email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Contraseña</Form.Label>
                                <Form.Control
                                    type="password"
                                    placeholder="Ingrese su contraseña"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Button variant="danger" type="submit" className="w-100">
                                Iniciar Sesión
                            </Button>
                        </Form>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
};

export default Login;
