document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.querySelector(".user-icon");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    userIcon.addEventListener("click", function () {
        dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });

    // Ocultar menú si se hace clic fuera de él
    document.addEventListener("click", function (event) {
        if (!userIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });

    // === Función para abrir y cerrar el modal de publicación ===
    window.openModal = function () {
        document.getElementById("postModal").style.display = "flex";
    };

    window.closeModal = function () {
        document.getElementById("postModal").style.display = "none";
    };

    // === Función para abrir y cerrar el modal del mapa ===
    window.openMap = function () {
        document.getElementById("mapModal").style.display = "flex";

        // Inicializar el mapa solo si no existe
        if (!window.mapInitialized) {
            var map = L.map('map').setView([-12.0464, -77.0428], 12); // Centrado en Lima

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            var marker = L.marker([-12.0464, -77.0428], { draggable: true }).addTo(map);

            marker.on('dragend', function (e) {
                var latlng = marker.getLatLng();
                document.getElementById("location-input").value = latlng.lat + ', ' + latlng.lng;
            });

            window.mapInitialized = true;
        }
    };

    window.closeMapModal = function () {
        document.getElementById("mapModal").style.display = "none";
    };

    window.confirmLocation = function () {
        closeMapModal();
    };

    // === Manejo de hashtags ===
    document.querySelectorAll(".hashtag-label").forEach(label => {
        label.addEventListener("click", function () {
            document.querySelectorAll(".hashtag-label").forEach(h => h.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // === Manejo de previsualización de imágenes ===
    const imageInput = document.getElementById("image-input");
    const imagePreview = document.getElementById("image-preview");

    imageInput.addEventListener("change", function (event) {
        imagePreview.innerHTML = "";  // Limpiar vista previa anterior
        const files = event.target.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const reader = new FileReader();

            reader.onload = function (e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.classList.add("preview-img");
                img.setAttribute("onclick", `openModalLightbox('${e.target.result}')`);
                imagePreview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });

    // Función para abrir el Lightbox de imágenes en publicaciones
    window.openPostLightbox = function(src) {
        document.getElementById("post-lightbox-image").src = src;
        document.getElementById("post-lightbox").style.display = "flex";
    };

    // Función para cerrar el Lightbox
    window.closePostLightbox = function() {
        document.getElementById("post-lightbox").style.display = "none";
    };

});
