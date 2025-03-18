//tailwind.config.js: Indica a Tailwind CSS qué archivos debe analizar para generar los estilos necesarios.

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,jsx}",
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}
