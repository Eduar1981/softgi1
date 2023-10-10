document.addEventListener("DOMContentLoaded", function () {
    const botonBusqueda = document.getElementById("mostrarBusqueda");
    const campoBusqueda = document.getElementById("campoBusqueda");

    botonBusqueda.addEventListener("click", function () {
        if (campoBusqueda.style.display === "none" || campoBusqueda.style.display === "") {
            campoBusqueda.style.display = "block";
        } else {
            campoBusqueda.style.display = "none";
        }
    });
});
