document.addEventListener("DOMContentLoaded", function () {
    const filters = document.querySelectorAll(".filter");
    const loteCards = document.querySelectorAll(".lote-card");

    filters.forEach(filter => {
        filter.addEventListener("change", applyFilters);
    });

    function applyFilters() {
        // Obtener valores seleccionados de los filtros
        const estadoFilters = Array.from(document.querySelectorAll('.filter[data-filter="estado"]:checked')).map(f => f.value.toLowerCase());
        const fundoFilters = Array.from(document.querySelectorAll('.filter[data-filter="fundo"]:checked')).map(f => f.value.toLowerCase());
        const cultivoFilters = Array.from(document.querySelectorAll('.filter[data-filter="cultivo"]:checked')).map(f => f.value.toLowerCase());

        loteCards.forEach(lote => {
            const estado = lote.getAttribute("data-estado")?.toLowerCase() || "";
            const fundo = lote.getAttribute("data-fundo")?.toLowerCase() || "";
            const cultivo = lote.getAttribute("data-cultivo")?.toLowerCase() || "";

            // Verificar si el lote cumple con todos los filtros activos
            const estadoMatch = estadoFilters.length === 0 || estadoFilters.includes(estado);
            const fundoMatch = fundoFilters.length === 0 || fundoFilters.includes(fundo);
            const cultivoMatch = cultivoFilters.length === 0 || cultivoFilters.includes(cultivo);

            // Mostrar solo los lotes que cumplan con TODOS los filtros seleccionados
            lote.style.display = (estadoMatch && fundoMatch && cultivoMatch) ? "flex" : "none";
        });
    }
});


