# Cameras/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from .models import Building, Camera, Region, District
from .forms import BuildingForm
import cv2
import urllib.request
import numpy as np


# Проверка, что пользователь в группе Administrators
def is_administrator(user):
    return user.is_authenticated and user.groups.filter(name='Administrators').exists()


def building_list(request):
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
    return render(request, 'cameras/building_list.html', {'district_data': district_data})


def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    cameras = Camera.objects.filter(building=building)
    paginator = Paginator(cameras, 4)  # 4 камеры на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cameras/building_detail.html', {'building': building, 'page_obj': page_obj})


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


@user_passes_test(is_administrator, login_url='/users/login/')
def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    building_id = camera.building.id
    camera.delete()
    return redirect('building_detail', pk=building_id)


def stream_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    if not camera.is_active:
        return HttpResponse("Камера неактивна", status=403)

    def generate_frames():
        stream_url = camera.rtsp_url
        try:
            cap = cv2.VideoCapture(stream_url)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            cap.release()
        except Exception as e:
            print(f"Ошибка потока: {e}")

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def get_districts(request, region_id):
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def region_list(request):
    regions = Region.objects.all().values('id', 'name')
    return JsonResponse(list(regions), safe=False)