#cameras/models.py
from django.db import models


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
    # Удалено: objects = None
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
    contacts = models.TextField(blank=True, verbose_name="Контакты")  # Убрано null=True
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"
        indexes = [
            models.Index(fields=['name']),  # Индекс для поиска по имени
            models.Index(fields=['region', 'district']),  # Индекс для фильтрации
        ]

    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название камеры")
    hls_path = models.CharField(max_length=50, verbose_name="HLS путь", help_text="Например, camera_1")
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