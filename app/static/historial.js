document.addEventListener("DOMContentLoaded", function () {
    const filters = document.querySelectorAll(".filter");
    const loteCards = document.querySelectorAll(".lote-card");

    if (loteCards.length === 0) {
        console.warn("No se encontraron lotes en la vista historial.");
        return;
    }

    filters.forEach(filter => {
        filter.addEventListener("change", applyFilters);
    });

    function applyFilters() {
        // Obtener valores seleccionados de los filtros
        const fundoFilters = Array.from(document.querySelectorAll('.filter[data-filter="fundo"]:checked')).map(f => f.value.toLowerCase());
        const cultivoFilters = Array.from(document.querySelectorAll('.filter[data-filter="cultivo"]:checked')).map(f => f.value.toLowerCase());

        loteCards.forEach(lote => {
            const fundo = lote.getAttribute("data-fundo")?.toLowerCase() || "";
            const cultivo = lote.getAttribute("data-cultivo")?.toLowerCase() || "";

            // Verificar si el lote cumple con los filtros seleccionados
            const fundoMatch = fundoFilters.length === 0 || fundoFilters.includes(fundo);
            const cultivoMatch = cultivoFilters.length === 0 || cultivoFilters.includes(cultivo);

            // Mostrar solo los lotes que cumplan con los filtros seleccionados
            lote.style.display = (fundoMatch && cultivoMatch) ? "flex" : "none";
        });
    }
});
