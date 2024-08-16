console.log("filters.js loaded successfully");

$(document).ready(function() {
    // Toggle sidebar on button click
    $('#toggle-sidebar').on('click', function() {
        var sidebar = $('.sidebar');
        sidebar.toggleClass('d-none');
    });

    // Initialize price slider
    var slider = document.getElementById('price-slider');
    if (slider) {
        noUiSlider.create(slider, {
            start: [0, maxPrice],
            connect: true,
            range: {
                'min': 0,
                'max': maxPrice
            }
        });

        var priceMinDisplay = document.getElementById('price-min-display');
        var priceMaxDisplay = document.getElementById('price-max-display');

        slider.noUiSlider.on('update', function(values) {
            var minPrice = parseFloat(values[0]).toFixed(2);
            var maxPrice = parseFloat(values[1]).toFixed(2);

            document.getElementById('price_min').value = minPrice;
            document.getElementById('price_max').value = maxPrice;

            priceMinDisplay.textContent = minPrice;
            priceMaxDisplay.textContent = maxPrice;
        });
    } else {
        console.error("Slider element not found");
    }

    // Handle filter form submission via AJAX
    $('#filter-form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: productListUrl,
            type: "GET",
            data: $(this).serialize(),
            success: function(data) {
                $('.product-list').html($(data).find('.product-list').html());
            }
        });
    });
});
