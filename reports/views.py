#reports/views.py
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from cameras.models import Building, Camera, UserCameraPermission

logger = logging.getLogger(__name__)

def is_administrator(user):
    return user.is_authenticated and user.groups.filter(name='Administrators').exists()

@login_required
@user_passes_test(is_administrator, login_url='/users/login/')
def reports(request):
    logger.info(f"Получен запрос на /reports/: метод={request.method}, данные={request.POST}")
    if request.method == "POST" and 'generate_report' in request.POST:
        logger.info("Срабатывает генерация отчёта")
        try:
            # Получаем всех пользователей группы Users
            users_group = Group.objects.get(name='Users')
            users = users_group.user_set.all()
            logger.debug(f"Пользователи группы Users: {users.count()}")

            # Собираем данные о зданиях и камерах
            buildings = Building.objects.all().prefetch_related('cameras', 'cameras__user_permissions')
            logger.debug(f"Здания: {buildings.count()}")
            report_data = []
            for building in buildings:
                building_info = {
                    'name': building.name,
                    'cameras': []
                }
                for camera in building.cameras.all():
                    camera_info = {
                        'name': camera.name,
                        'hls_path': camera.hls_path,
                        'rtsp_stream': camera.rtsp_stream or 'Не указан',
                        'allowed_users': [
                            permission.user.username
                            for permission in camera.user_permissions.all()
                            if permission.user in users
                        ]
                    }
                    building_info['cameras'].append(camera_info)
                report_data.append(building_info)
            logger.info(f"Отчёт сгенерирован: {len(report_data)} зданий")

            return render(request, 'reports/reports.html', {'report_data': report_data, 'show_report': True})
        except Exception as e:
            logger.error(f"Ошибка при генерации отчёта: {str(e)}")
            return render(request, 'reports/reports.html', {'show_report': False, 'error': str(e)})
    logger.debug("Отображаем форму для генерации отчёта")
    return render(request, 'reports/reports.html', {'show_report': False})