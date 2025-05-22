#cameras/forms.py
from django import forms
from .models import Building, Camera

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
        fields = ['name', 'hls_path', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hls_path': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }