//static/js/admin_permissions.js
document.addEventListener('DOMContentLoaded', function() {
    const buildingField = document.querySelector('#id_building');
    const camerasField = document.querySelector('#id_cameras');

    if (buildingField && camerasField) {
        buildingField.addEventListener('change', function() {
            const buildingId = this.value;
            if (buildingId) {
                fetch(`/cameras/get_cameras/${buildingId}/`)
                    .then(response => response.json())
                    .then(data => {
                        camerasField.innerHTML = '';
                        data.cameras.forEach(camera => {
                            const option = document.createElement('option');
                            option.value = camera.id;
                            option.text = camera.name;
                            camerasField.appendChild(option);
                        });
                        // Обновляем атрибут multiple
                        camerasField.setAttribute('multiple', 'multiple');
                    })
                    .catch(error => console.error('Error fetching cameras:', error));
            } else {
                camerasField.innerHTML = '';
            }
        });
    }
});