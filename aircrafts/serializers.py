from rest_framework import serializers
from .models import Aircraft, AircraftModel
from parts.models import Part


class AircraftModelSerializer(serializers.ModelSerializer):
    """
    Uçak modelini serileştiren serializer.
    Bu serializer, uçak modelinin ID ve adını döndürür.
    """

    class Meta:
        model = AircraftModel  # AircraftModel modelini kullanır
        fields = ["id", "name"]  # Sadece ID ve ad alanlarını döndürür


class AircraftSerializer(serializers.ModelSerializer):
    """
    Belirli bir uçağı serileştiren serializer. 
    """

    parts = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )  # Uçağa ait parçaların listesi (isteğe bağlı)

    class Meta:
        model = Aircraft   
        fields = ["id", "name", "aircraft_model", "parts"]   


class DetailedAircraftSerializer(serializers.ModelSerializer):
    """
    Detaylı uçak bilgilerini serileştiren serializer.
    Uçak modelinin adı ve parça detayları gibi ek bilgiler içerir.
    """

    aircraft_model_name = serializers.CharField(source="aircraft_model.name", read_only=True)
    part_details = serializers.SerializerMethodField()   

    class Meta:
        model = Aircraft   
        fields = ["id", "name", "aircraft_model_name", "part_details"]   


    def get_part_details(self, obj):
        """
        Uçağın parçalarını ve her parçanın stok miktarını döndüren metod.
        Parça ismi olarak part_type.name kullanılır.
        """
        parts = Part.objects.filter(id__in=obj.parts)  # Uçağa ait parçalar alınır
        return [
            {
                "name": part.part_type.name,  # part.name yerine part.part_type.name kullanıldı
                "quantity_in_stock": part.quantity_in_stock,
            }
            for part in parts  # Tüm parçalar için bu bilgiler döndürülür
        ]
