#cameras/models.py
from django.db import models
from django.contrib.auth.models import User

class Ministry(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название министерства")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Министерство"
        verbose_name_plural = "Министерства"
        indexes = [
            models.Index(fields=['name']),  # Индекс для поиска по имени
        ]

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название региона")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        indexes = [
            models.Index(fields=['name']),  # Индекс для поиска по имени
        ]

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название района")
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name="Регион"
    )

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        constraints = [
            models.UniqueConstraint(fields=['name', 'region'], name='unique_district_name_region')
        ]
        indexes = [
            models.Index(fields=['name', 'region']),  # Индекс для фильтрации
        ]

    def __str__(self):
        return f"{self.name} ({self.region.name})"

class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название здания")
    address = models.TextField(verbose_name="Адрес")
    ministry = models.ForeignKey(
        Ministry,
        on_delete=models.SET_NULL,
        null=True,
        related_name="buildings",
        verbose_name="Министерство"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        related_name="buildings",
        verbose_name="Регион"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="buildings",
        verbose_name="Район"
    )
    contacts = models.TextField(blank=True, verbose_name="Контакты")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['region', 'district']),
        ]

    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название камеры")
    hls_path = models.CharField(max_length=50, verbose_name="HLS путь", help_text="Например, camera_1")
    rtsp_stream = models.CharField(max_length=255, verbose_name="RTSP поток", blank=True, null=True, help_text="RTSP URL камеры, например, rtsp://username:password@ip_address/stream")
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, blank=True, related_name="cameras", verbose_name="Здание"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['building', 'is_active']),
        ]

    def __str__(self):
        return self.name

class UserBuildingPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="building_permissions", verbose_name="Пользователь")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="user_permissions", verbose_name="Здание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Разрешение на здание"
        verbose_name_plural = "Разрешения на здания"
        unique_together = ['user', 'building']
        indexes = [
            models.Index(fields=['user', 'building']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.building.name}"

class UserCameraPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="camera_permissions", verbose_name="Пользователь")
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="user_permissions", verbose_name="Камера")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Разрешение на камеру"
        verbose_name_plural = "Разрешения на камеры"
        unique_together = ['user', 'camera']
        indexes = [
            models.Index(fields=['user', 'camera']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.camera.name}"