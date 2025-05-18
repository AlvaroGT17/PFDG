const currentURL = window.location.pathname;
document.querySelectorAll('nav.pdoc li a').forEach(link => {
    if (link.getAttribute('href') && currentURL.endsWith(link.getAttribute('href'))) {
        link.classList.add('activo');
    }
});

