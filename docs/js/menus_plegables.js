document.addEventListener("DOMContentLoaded", () => {
    const botones = document.querySelectorAll(".toggle-boton");
    const submenus = document.querySelectorAll(".submodulos");

    // Inicialmente ocultar todos los grupos
    document.querySelectorAll(".grupo-modulos").forEach(ul => {
        ul.style.display = "none";
    });

    botones.forEach(boton => {
        const idObjetivo = boton.dataset.target;
        const ulObjetivo = document.getElementById(idObjetivo);

        boton.addEventListener("click", () => {
            const estaVisible = ulObjetivo.style.display === "block";

            // Oculta todos los grupos
            document.querySelectorAll(".grupo-modulos").forEach(ul => {
                ul.style.display = "none";
            });

            // Cierra todos los submenús abiertos
            document.querySelectorAll(".item-con-submenu").forEach(item => {
                item.classList.remove("open");
            });

            // Restaura todos los textos
            botones.forEach(b => {
                const textoBase = b.textContent.slice(2);
                b.textContent = "▶ " + textoBase;
            });

            // Si estaba cerrado, mostrar y actualizar símbolo
            if (!estaVisible) {
                ulObjetivo.style.display = "block";
                boton.textContent = "▼ " + boton.textContent.slice(2);
            }
        });
    });

    // Mostrar submenú al pasar el ratón pero mantenerlo abierto
    document.querySelectorAll(".submenu-toggle").forEach(toggle => {
        const item = toggle.closest(".item-con-submenu");

        toggle.addEventListener("mouseenter", () => {
            // Cierra todos los submenús abiertos
            document.querySelectorAll(".item-con-submenu").forEach(otro => {
                if (otro !== item) {
                    otro.classList.remove("open");
                }
            });

            // Abre este
            item.classList.add("open");
        });
    });
});


