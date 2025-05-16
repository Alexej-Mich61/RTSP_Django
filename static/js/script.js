//static/js/script.js
console.log('script.js loaded'); // Диагностика загрузки

$(document).ready(function() {
    console.log('jQuery ready'); // Диагностика jQuery

    // Фильтрация районов
    $('#id_region').change(function() {
        console.log('Region changed'); // Отладка
        var regionId = $(this).val();
        if (regionId) {
            $.get('/cameras/api/districts/' + regionId + '/', function(data) {
                var districtSelect = $('#id_district');
                districtSelect.empty();
                districtSelect.append('<option value="">Выберите район</option>');
                $.each(data, function(index, district) {
                    districtSelect.append('<option value="' + district.id + '">' + district.name + '</option>');
                });
            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading districts:', textStatus, errorThrown); // Отладка ошибок AJAX
            });
        } else {
            $('#id_district').empty().append('<option value="">Выберите район</option>');
        }
    });

    // Полноэкранный режим для камер
    $(document).on('click', '.fullscreen-btn', function(e) {
        e.preventDefault(); // Предотвращаем действие по умолчанию
        console.log('Fullscreen button clicked'); // Отладка
        var cameraId = $(this).data('camera-id');
        console.log('Camera ID:', cameraId); // Отладка
        var streamUrl = '/cameras/cameras/' + cameraId + '/stream/';
        console.log('Stream URL:', streamUrl); // Отладка
        $('#fullscreenStream').attr('src', streamUrl);
        try {
            $('#fullscreenModal').modal('show');
            console.log('Modal should be shown'); // Отладка
        } catch (e) {
            console.error('Error opening modal:', e); // Диагностика ошибок Bootstrap
        }
    });

    // Очистка потока при закрытии модального окна
    $('#fullscreenModal').on('hidden.bs.modal', function() {
        console.log('Modal closed'); // Отладка
        $('#fullscreenStream').attr('src', '');
    });
});