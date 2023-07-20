$(document).ready(function() {
    $('#segment-dropdown').change(function() {
        var selectedSegment = $(this).val();
        var current_path = window.location.pathname;

        $.ajax({
            url: '/get_price_plans',
            type: 'POST',
            data: {
                segment: selectedSegment,
                current_path: current_path
            },
            success: function(response) {
                var pricePlanDropdown = $('#price-plan-dropdown');
                pricePlanDropdown.empty();
                pricePlanDropdown.append($('<option>').text('All').attr('value', 'All'));
                $.each(JSON.parse(response), function(index, option) {
                    pricePlanDropdown.append($('<option>').text(option).attr('value', option));
                });
            }
        });
    });

    $('#price-plan-dropdown').change(function() {
        var selectedSegment = $('#segment-dropdown').val();
        var selectedPricePlan = $(this).val();
        var current_path = window.location.pathname;
        $.ajax({
            url: '/get_discounted_mf',
            type: 'POST',
            data: {
                segment: selectedSegment, 
                price_plan: selectedPricePlan,
                current_path: current_path
            },
            success: function(response) {
                var discountedMFDropdown = $('#discounted-mf-dropdown');
                discountedMFDropdown.empty();
                discountedMFDropdown.append($('<option>').text('All').attr('value', 'All'));
                $.each(JSON.parse(response), function(index, option) {
                    discountedMFDropdown.append($('<option>').text(option).attr('value', option));
                });
            }
        });
    });

    $('#discounted-mf-dropdown').change(function() {
        var selectedSegment = $('#segment-dropdown').val();
        var selectedPricePlan = $('#price-plan-dropdown').val();
        var selectedDiscountedMF = $(this).val();
        
        $.ajax({
            url: '/get_admin_centers',
            type: 'POST',
            data: {
                segment: selectedSegment, 
                price_plan: selectedPricePlan, 
                discounted_mf: selectedDiscountedMF,
                current_path: current_path
            },
            success: function(response) {
                var adminCenterDropdown = $('#admin-center-dropdown');
                adminCenterDropdown.empty();
                adminCenterDropdown.append($('<option>').text('All').attr('value', 'All'));
                $.each(JSON.parse(response), function(index, option) {
                    adminCenterDropdown.append($('<option>').text(option).attr('value', option));
                });
            }
        });
    });

    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
});