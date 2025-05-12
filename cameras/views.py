# Cameras/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BuildingForm, CameraForm
from .models import Building, Camera, Region, District, Ministry
from django.http import StreamingHttpResponse, JsonResponse
from django.core.paginator import Paginator
import cv2


def create_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building_list')
    else:
        form = BuildingForm()
    return render(request, 'cameras/building_form.html', {'form': form})


def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'cameras/building_list.html', {'buildings': buildings})


def building_detail(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    cameras = building.cameras.all()
    paginator = Paginator(cameras, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cameras/building_detail.html', {
        'building': building,
        'page_obj': page_obj,
    })


def building_edit(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    cameras = building.cameras.all()

    if request.method == 'POST':
        if 'save_building' in request.POST:
            building_form = BuildingForm(request.POST, instance=building)
            if building_form.is_valid():
                building_form.save()
                return redirect('building_detail', building_id=building_id)
        elif 'add_camera' in request.POST:
            new_camera_form = CameraForm(request.POST)
            if new_camera_form.is_valid():
                camera = new_camera_form.save(commit=False)
                camera.building = building
                camera.save()
                return redirect('building_edit', building_id=building_id)
        elif any(key.startswith('save_camera_') for key in request.POST):
            for camera in cameras:
                if f'save_camera_{camera.id}' in request.POST:
                    camera_form = CameraForm(request.POST, instance=camera)
                    if camera_form.is_valid():
                        camera_form.save()
                    return redirect('building_edit', building_id=building_id)
        elif any(key.startswith('delete_camera_') for key in request.POST):
            for camera in cameras:
                if f'delete_camera_{camera.id}' in request.POST:
                    camera.delete()
                    return redirect('building_edit', building_id=building_id)

    building_form = BuildingForm(instance=building)
    camera_forms = [CameraForm(instance=camera) for camera in cameras]
    new_camera_form = CameraForm()

    return render(request, 'cameras/building_edit.html', {
        'building': building,
        'building_form': building_form,
        'camera_forms': camera_forms,
        'new_camera_form': new_camera_form,
    })


def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    building_id = camera.building.id if camera.building else None
    camera.delete()
    if building_id:
        return redirect('building_detail', building_id=building_id)
    return redirect('building_list')


def stream_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    cap = cv2.VideoCapture(camera.rtsp_url)

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def region_list(request):
    regions = Region.objects.all().values('id', 'name')
    return JsonResponse(list(regions), safe=False)


def district_list(request, region_id=None):
    if region_id:
        districts = District.objects.filter(region_id=region_id).values('id', 'name')
    else:
        districts = District.objects.all().values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def users(request):
    return render(request, 'users/users.html')


def reports(request):
    return render(request, 'reports/reports.html')