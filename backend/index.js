import express from 'express';
import cors from 'cors';
import authRoutes from './routes/authRoutes.js';

const app = express();

// Configuración
app.use(express.json());
app.use(cors());

// Rutas
app.use('/api/auth', authRoutes);

// Servidor
const PORT = process.env.PORT || 1983;
app.listen(PORT, () => {
    console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});
