from rest_framework import serializers
from .models import PartType, Part
from aircrafts.serializers import AircraftModelSerializer
from aircrafts.models import AircraftModel

class PartTypeSerializer(serializers.ModelSerializer):
    """
    Parça tipini serileştiren serializer.
    """

    class Meta:
        model = PartType
        fields = ["id", "name"]   

class PartSerializer(serializers.ModelSerializer):
    """
    Parçayı serileştiren serializer.
    """

    # Sadece okunabilir bilgi için kullanıyoruz
    part_type_detail = PartTypeSerializer(source="part_type", read_only=True)
    aircraft_model_detail = AircraftModelSerializer(source="aircraft_model", read_only=True)

    # Yazılabilir alanlar için PrimaryKeyRelatedField kullanıyoruz
    part_type = serializers.PrimaryKeyRelatedField(queryset=PartType.objects.all())
    aircraft_model = serializers.PrimaryKeyRelatedField(queryset=AircraftModel.objects.all())

    class Meta:
        model = Part
        fields = [
            "id",
            "part_type",  # ID olarak gönderim için
            "part_type_detail",  # Detaylı bilgi için
            "aircraft_model",  # ID olarak gönderim için
            "aircraft_model_detail",  # Detaylı bilgi için
            "quantity_in_stock",
        ]

