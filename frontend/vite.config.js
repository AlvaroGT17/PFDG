import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'ReyBoxes - Mecánica y mantenimiento',
        short_name: 'ReyBoxes',
        description: 'Sistema de gestión para talleres mecánicos',
        start_url: '/',
        display: 'standalone',
        background_color: '#222831',
        theme_color: '#E30613',
        orientation: 'portrait',
        icons: [
          {
            src: 'icon-192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
  server: {
    port: 1702
  }
});
