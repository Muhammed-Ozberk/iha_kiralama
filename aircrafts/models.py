from django.db import models
from django.contrib.postgres.fields import ArrayField


class AircraftModel(models.Model):
    """
    Uçak modelini temsil eder. Örneğin TB2, TB3 veya Akıncı gibi modeller.
    """

    name = models.CharField(max_length=255, unique=True)  # Modelin adı, benzersiz olmalıdır.

    def __str__(self):
        return f"{self.name}"  # Modelin adını döndürür.


class Aircraft(models.Model):
    """
    Belirli bir uçağı temsil eder. Örneğin, THY'nin bir TB2 uçağı.
    """

    name = models.CharField(max_length=255)  # Uçağın adı.
    aircraft_model = models.ForeignKey(
        AircraftModel, on_delete=models.CASCADE, related_name="aircrafts"
    )  # Uçak modeli ile ilişki kurar.
    parts = ArrayField(models.IntegerField(), blank=True, default=list)  # Uçağın parçaları.

    def __str__(self):
        return f"{self.name} ({self.aircraft_model})"  # Uçak adı ve modeliyle birlikte döndürür.
