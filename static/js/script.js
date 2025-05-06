$(document).ready(function() {
    $('#id_region').change(function() {
        var regionId = $(this).val();
        if (regionId) {
            $.get('/cameras/api/districts/' + regionId + '/', function(data) {
                var districtSelect = $('#id_district');
                districtSelect.empty();
                districtSelect.append('<option value="">Выберите район</option>');
                $.each(data, function(index, district) {
                    districtSelect.append('<option value="' + district.id + '">' + district.name + '</option>');
                });
            });
        } else {
            $('#id_district').empty().append('<option value="">Выберите район</option>');
        }
    });
});