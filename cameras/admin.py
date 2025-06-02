#cameras/admin.py
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Ministry, Region, District, Building, Camera, UserBuildingPermission, UserCameraPermission

class UserBuildingPermissionForm(forms.ModelForm):
    cameras = forms.ModelMultipleChoiceField(
        queryset=Camera.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Камеры"
    )

    class Meta:
        model = UserBuildingPermission
        fields = ['user', 'building', 'cameras']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.building:
            self.fields['cameras'].queryset = Camera.objects.filter(building=self.instance.building)
            self.initial['cameras'] = Camera.objects.filter(
                user_permissions__user=self.instance.user,
                building=self.instance.building
            )
        elif 'building' in self.data:
            try:
                building_id = int(self.data.get('building'))
                self.fields['cameras'].queryset = Camera.objects.filter(building_id=building_id)
            except (ValueError, TypeError):
                self.fields['cameras'].queryset = Camera.objects.none()
        else:
            self.fields['cameras'].queryset = Camera.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        building = cleaned_data.get('building')
        cameras = cleaned_data.get('cameras')
        if building and cameras:
            invalid_cameras = cameras.exclude(building=building)
            if invalid_cameras.exists():
                raise forms.ValidationError("Выбранные камеры должны принадлежать указанному зданию.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if self.cleaned_data['cameras']:
            UserCameraPermission.objects.filter(
                user=instance.user,
                camera__building=instance.building
            ).delete()
            for camera in self.cleaned_data['cameras']:
                UserCameraPermission.objects.create(
                    user=instance.user,
                    camera=camera
                )
        return instance

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    search_fields = ['name']

class CameraInline(admin.TabularInline):
    model = Camera
    extra = 1
    fields = ['name', 'hls_path', 'is_active']

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'ministry', 'region', 'district', 'created_at']
    list_filter = ['ministry', 'region', 'district']
    search_fields = ['name', 'address', 'contacts']
    inlines = [CameraInline]

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'hls_path', 'is_active', 'created_at']
    list_filter = ['building', 'is_active']
    search_fields = ['name', 'hls_path']

@admin.register(UserBuildingPermission)
class UserBuildingCameraPermissionAdmin(admin.ModelAdmin):
    form = UserBuildingPermissionForm
    list_display = ['user', 'building', 'created_at']
    list_filter = ['user', 'building']
    search_fields = ['user__username', 'building__name']

    def delete_model(self, request, obj):
        UserCameraPermission.objects.filter(user=obj.user, camera__building=obj.building).delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            UserCameraPermission.objects.filter(user=obj.user, camera__building=obj.building).delete()
        queryset.delete()

# Отменяем стандартную регистрацию User
admin.site.unregister(User)

# Регистрируем кастомную админку для User
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_active']

    # Указываем поля для формы редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Указываем поля для формы добавления
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )