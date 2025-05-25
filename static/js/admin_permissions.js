//static/js/admin_permissions.js
document.addEventListener('DOMContentLoaded', function() {
    // Функция для получения CSRF-токена из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const buildingField = document.querySelector('#id_building');
    const camerasField = document.querySelector('#id_cameras');

    if (buildingField && camerasField) {
        buildingField.addEventListener('change', function() {
            const buildingId = this.value;
            if (buildingId) {
                fetch(`/cameras/get_cameras/${buildingId}/`, {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken') // Добавляем CSRF-токен для совместимости с POST в будущем
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        camerasField.innerHTML = '';
                        data.cameras.forEach(camera => {
                            const option = document.createElement('option');
                            option.value = camera.id;
                            option.text = camera.name;
                            camerasField.appendChild(option);
                        });
                        camerasField.setAttribute('multiple', 'multiple');
                    })
                    .catch(error => console.error('Error fetching cameras:', error));
            } else {
                camerasField.innerHTML = '';
            }
        });
    }
});