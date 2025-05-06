# cameras/models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_rtsp_url(value):
    """Валидатор для RTSP URL."""
    rtsp_pattern = r'^rtsp://[^\s/$.?#].*$'
    if not re.match(rtsp_pattern, value):
        raise ValidationError('Введите корректный RTSP URL, начинающийся с rtsp://')

class Ministry(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название министерства")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Министерство"
        verbose_name_plural = "Министерства"

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название региона")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

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
        unique_together = ['name', 'region']

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
    contacts = models.TextField(blank=True, null=True, verbose_name="Контакты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"

    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название камеры")
    rtsp_url = models.CharField(
        max_length=255,
        validators=[validate_rtsp_url],
        verbose_name="RTSP URL"
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cameras",
        verbose_name="Здание"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"

    def __str__(self):
        return self.name