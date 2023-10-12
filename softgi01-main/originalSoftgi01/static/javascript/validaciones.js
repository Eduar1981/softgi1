document.getElementById('mostrarContrasena').addEventListener('change', function() {
    var contrasenaInput = document.getElementById('contrasena');
    if (this.checked) {
        contrasenaInput.type = 'text';
    } else {
        contrasenaInput.type = 'password';
    }
});

document.getElementById("mostrarConfirmarContrasena").addEventListener("change", function () {
    var input = document.getElementById("repeatContrasena");
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
});
