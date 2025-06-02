#cameras/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.conf import settings  # Импортируем настройки
from .models import Building, Camera, Region, District, UserBuildingPermission, UserCameraPermission
from .forms import BuildingForm
from .utils import is_administrator
from django.contrib.auth.decorators import login_required

def stream_camera(request, camera_id):
    """Возвращает HLS URL для камеры."""
    camera = get_object_or_404(Camera, id=camera_id)
    if not camera.is_active:
        return JsonResponse({'error': 'Камера неактивна'}, status=403)
    hls_url = f"{settings.HLS_HOST}/{camera.hls_path}/stream.m3u8"
    return JsonResponse({'hls_url': hls_url})

@login_required
def building_list(request):
    if is_administrator(request.user):
        # Администраторы видят все здания
        districts = District.objects.all()
        district_data = []
        for district in districts:
            buildings = Building.objects.filter(district=district)
            building_count = buildings.count()
            if building_count > 0:
                district_data.append({
                    'district': district,
                    'building_count': building_count,
                    'buildings': [
                        {'building': b, 'camera_count': Camera.objects.filter(building=b).count()}
                        for b in buildings
                    ]
                })
        no_district_buildings = Building.objects.filter(district__isnull=True)
        no_district_count = no_district_buildings.count()
        if no_district_count > 0:
            district_data.append({
                'district': None,
                'building_count': no_district_count,
                'buildings': [
                    {'building': b, 'camera_count': Camera.objects.filter(building=b).count()}
                    for b in no_district_buildings
                ]
            })
    else:
        # Пользователи видят только разрешённые здания
        permitted_building_ids = UserBuildingPermission.objects.filter(user=request.user).values_list('building_id',
                                                                                                      flat=True)
        district_data = []
        districts = District.objects.filter(buildings__id__in=permitted_building_ids).distinct()
        for district in districts:
            buildings = Building.objects.filter(id__in=permitted_building_ids, district=district)
            building_count = buildings.count()
            if building_count > 0:
                district_data.append({
                    'district': district,
                    'building_count': building_count,
                    'buildings': [
                        {'building': b, 'camera_count': Camera.objects.filter(building=b).count()}
                        for b in buildings
                    ]
                })
        no_district_buildings = Building.objects.filter(id__in=permitted_building_ids, district__isnull=True)
        no_district_count = no_district_buildings.count()
        if no_district_count > 0:
            district_data.append({
                'district': None,
                'building_count': no_district_count,
                'buildings': [
                    {'building': b, 'camera_count': Camera.objects.filter(building=b).count()}
                    for b in no_district_buildings
                ]
            })
    return render(request, 'cameras/building_list.html', {
        'district_data': district_data,
        'is_administrator': is_administrator(request.user)
    })

@login_required
def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    # Проверка доступа к зданию для Users
    if not is_administrator(request.user) and not UserBuildingPermission.objects.filter(user=request.user,
                                                                                        building=building).exists():
        return render(request, 'cameras/access_denied.html', status=403)

    if is_administrator(request.user):
        # Администраторы видят все камеры
        cameras = Camera.objects.filter(building=building).order_by('id')
    else:
        # Пользователи видят только разрешённые камеры
        permitted_camera_ids = UserCameraPermission.objects.filter(user=request.user).values_list('camera_id',
                                                                                                  flat=True)
        cameras = Camera.objects.filter(building=building, id__in=permitted_camera_ids).order_by('id')

    paginator = Paginator(cameras, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cameras/building_detail.html', {
        'building': building,
        'page_obj': page_obj,
        'is_administrator': is_administrator(request.user),
        'hls_host': settings.HLS_HOST,  # Передаём HLS_HOST в контекст шаблона
    })

@login_required
@user_passes_test(is_administrator, login_url='/users/login/')
def building_create(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building_list')
    else:
        form = BuildingForm()
    return render(request, 'cameras/building_form.html', {'form': form})

@login_required
@user_passes_test(is_administrator, login_url='/users/login/')
def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('building_detail', pk=building.pk)
    else:
        form = BuildingForm(instance=building)
    return render(request, 'cameras/building_form.html', {'form': form})

@login_required
@user_passes_test(is_administrator, login_url='/users/login/')
def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    building_id = camera.building.id
    camera.delete()
    return redirect('building_detail', pk=building_id)

def get_districts(request, region_id):
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def region_list(request):
    regions = Region.objects.all().values('id', 'name')
    return JsonResponse(list(regions), safe=False)

def get_cameras(request, building_id):
    cameras = Camera.objects.filter(building_id=building_id).values('id', 'name')
    return JsonResponse({'cameras': list(cameras)})