import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Configuración clara y exacta del servidor con puerto personalizado
export default defineConfig({
  plugins: [react()],
  server: {
    port: 1702  // <-- Puerto personalizado exactamente como pediste
  }
});
