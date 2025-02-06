document.addEventListener("DOMContentLoaded", function() {
    var inputFile = document.getElementById("foto_perfil");
    var label = document.getElementById("nombre_archivo");

    if (inputFile) {
        inputFile.addEventListener("change", function() {
            if (inputFile.files.length > 0) {
                label.textContent = inputFile.files[0].name;
            } else {
                label.textContent = "Ningún archivo seleccionado";
            }
        });
    }
});
