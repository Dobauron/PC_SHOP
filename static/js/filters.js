console.log("filters.js loaded successfully");

$(document).ready(function() {
    var slider = document.getElementById('price-slider');
    if (!slider) {
        console.error("Slider element not found");
        return;
    }

    noUiSlider.create(slider, {
        start: [0, maxPrice],
        connect: true,
        range: {
            'min': 0,
            'max': maxPrice
        }
    });

    slider.noUiSlider.on('update', function(values) {
        document.getElementById('price_min').value = values[0];
        document.getElementById('price_max').value = values[1];
    });

    $('#filter-form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: productListUrl,  // Używamy poprawnie zdefiniowanej zmiennej
            type: "GET",
            data: $(this).serialize(),
            success: function(data) {
                $('.product-list').html($(data).find('.product-list').html());
            }
        });
    });
});
