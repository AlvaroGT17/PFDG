document.addEventListener("DOMContentLoaded", () => {
    const botones = document.querySelectorAll(".toggle-boton");

    botones.forEach(boton => {
        boton.addEventListener("click", () => {
            const item = boton.closest(".item-con-submenu");
            const sublista = item.querySelector(".submodulos");
            const titulo = boton.dataset.titulo;

            const estaVisible = item.classList.contains("open");

            // Cierra todos
            document.querySelectorAll(".item-con-submenu").forEach(otroItem => {
                otroItem.classList.remove("open");
                otroItem.querySelector(".submodulos").style.maxHeight = null;
                otroItem.querySelector(".toggle-boton").textContent = "▶ " + otroItem.querySelector(".toggle-boton").dataset.titulo;
            });

            // Si no estaba abierto, abrir este
            if (!estaVisible) {
                item.classList.add("open");
                sublista.style.maxHeight = sublista.scrollHeight + "px";
                boton.textContent = "▼ " + titulo;
            }
        });
    });
});
