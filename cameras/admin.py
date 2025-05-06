# cameras/admin.py
from django.contrib import admin
from .models import Ministry, Region, District, Building, Camera

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
    fields = ['name', 'rtsp_url', 'is_active']

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'ministry', 'region', 'district', 'created_at']
    list_filter = ['ministry', 'region', 'district']
    search_fields = ['name', 'address', 'contacts']
    inlines = [CameraInline]

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'rtsp_url', 'is_active', 'created_at']
    list_filter = ['building', 'is_active']
    search_fields = ['name', 'rtsp_url']
