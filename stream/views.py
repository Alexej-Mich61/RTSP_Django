from django.shortcuts import redirect

def redirect_to_buildings(request):
    return redirect('building_list', permanent=False)