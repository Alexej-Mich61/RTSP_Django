# reports/models.py
from django.db import models
from cameras.models import Building

class Report(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=100)
    details = models.TextField()

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"{self.event} ({self.building.name})"