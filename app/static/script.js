// Mostrar/Ocultar contraseña
function togglePassword(id) {
    const input = document.getElementById(id);
    input.type = (input.type === "password") ? "text" : "password";
}

// Mostrar el nombre de la imagen seleccionada
document.getElementById('foto_perfil').addEventListener('change', function(event) {
    const fileName = event.target.files[0] ? event.target.files[0].name : "Cargar Foto";
    document.querySelector('.file-label').innerHTML = fileName + ' <img src="/static/img/Imagen.png" class="upload-icon">';
});