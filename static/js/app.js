const toggle = document.querySelector(".toggle");
const menuDashboard = document.querySelector(".menu-dashboard");
const iconoMenu = toggle.querySelector("i");
const enlacesMenu = document.querySelectorAll(".enlace");

toggle.addEventListener("click", () => {
    menuDashboard.classList.toggle("open");

    if (iconoMenu.classList.contains("bx-menu")) {
        iconoMenu.classList.replace("bx-menu", "bx-x");
    } else {
        iconoMenu.classList.replace("bx-x", "bx-menu");
    }
});

enlacesMenu.forEach(enlace => {
    enlace.addEventListener("click", () => {
        menuDashboard.classList.add("open");
        iconoMenu.classList.replace("bx-menu", "bx-x");
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const btnUsuario = document.getElementById('btn-usuario');
    const perfil = document.getElementById('perfil');

    btnUsuario.addEventListener('click', () => {
        if (perfil.style.display === 'none' || perfil.style.display === '') {
            perfil.style.display = 'flex';
        } else {
            perfil.style.display = 'none';
        }
    });

    // Cerrar si se hace clic fuera del cuadro
    perfil.addEventListener('click', (e) => {
        if (e.target === perfil) {
            perfil.style.display = 'none';
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const btnUsuario = document.getElementById("btn-usuario");
    const btnArchivos = document.getElementById("btn-archivos");
    const btnDocumentacion = document.getElementById("btn-documentacion"); // 👈 NUEVO
    const perfil = document.getElementById("perfil");
    const archivos = document.getElementById("archivos");
    const documentacion = document.getElementById("documentacion"); // 👈 NUEVO

    btnUsuario.addEventListener("click", () => {
        perfil.style.display = "flex";
        archivos.style.display = "none";
        documentacion.style.display = "none";
    });

    btnArchivos.addEventListener("click", () => {
        archivos.style.display = "flex";
        perfil.style.display = "none";
        documentacion.style.display = "none";
    });

    // 👇 NUEVO: Mostrar sección de documentación
    btnDocumentacion.addEventListener("click", () => {
        documentacion.style.display = "flex";
        perfil.style.display = "none";
        archivos.style.display = "none";
    });
});

// Ejecutar un programa .py y mostrar salida en el "terminal"
function ejecutarPrograma(nombreArchivo) {
    fetch(`/run/${nombreArchivo}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('salida').textContent = data.salida;
        })
        .catch(error => {
            document.getElementById('salida').textContent = 'Error al ejecutar el programa: ' + error;
        });
}

// Ejecutar programas Python sin recargar la página
document.addEventListener("DOMContentLoaded", () => {
    const botones = document.querySelectorAll(".btn-ejecutar");
    const salida = document.getElementById("salida");

    botones.forEach(boton => {
        boton.addEventListener("click", async () => {
            const archivo = boton.dataset.archivo;
            salida.textContent = "Ejecutando " + archivo + "...\n";

            try {
                const respuesta = await fetch(`/run/${archivo}`, { method: "POST" });
                const data = await respuesta.json();
                salida.textContent = data.salida;
            } catch (error) {
                salida.textContent = "Error al ejecutar el programa: " + error;
            }
        });
    });
});
