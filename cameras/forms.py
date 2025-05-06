#cameras/forms.py
from django import forms
from .models import Building, Camera, Ministry, Region, District
from django.core.exceptions import ValidationError
import re

def validate_rtsp_url(value):
    """Валидатор для RTSP URL."""
    rtsp_pattern = r'^rtsp://[^\s/$.?#].*$'
    if not re.match(rtsp_pattern, value):
        raise ValidationError('Введите корректный RTSP URL, начинающийся с rtsp://')

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'ministry', 'region', 'district', 'contacts']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ministry': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'contacts': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'rtsp_url', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rtsp_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }