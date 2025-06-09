#stream/redirect.py
from django.shortcuts import redirect

def redirect_to_buildings(request):
    """Редирект на страницу building_list"""
    return redirect('building_list', permanent=False)