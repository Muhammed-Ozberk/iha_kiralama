from django.db import models

class PartType(models.Model):
    """
    Parçanın tipi (ör. Kanat, Gövde, Kuyruk)
    """

    name = models.CharField(max_length=255, unique=True)   

    def __str__(self):
        return self.name   

class Part(models.Model):
    """
    Belirli bir parçayı tanımlayan model.
    Parçanın tipi ve ait olduğu uçak modeli ile ilişkilendirilmiştir.
    """

    part_type = models.ForeignKey(
        PartType, on_delete=models.CASCADE, related_name="parts"   
    )
    aircraft_model = models.ForeignKey(
        "aircrafts.AircraftModel",  # Lazy reference kullanımı
        on_delete=models.CASCADE,
        related_name="parts",  # İlişkili uçak modelleri
    )
    quantity_in_stock = models.IntegerField(default=0)  # Stoktaki miktar

    def __str__(self):
        return f"({self.part_type}) - {self.aircraft_model}"  