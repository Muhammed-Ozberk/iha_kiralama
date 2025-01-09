from rest_framework.permissions import BasePermission
from .utils import can_produce_part
from .models import PartType

class CanProducePartPermission(BasePermission):
    """
    Kullanıcının belirli bir parçayı üretme iznini kontrol eden izin sınıfı.
    """

    def has_permission(self, request, view):
        # Yalnızca 'POST' işlemi için kontrol yapılır
        if request.method == "POST":
            part_type_id = request.data.get("part_type")  
            if part_type_id:
                try:
                    part_type = PartType.objects.get(id=part_type_id)  
                    return can_produce_part(request.user, part_type)  # Kullanıcının bu parça tipini üretme yetkisini kontrol edilir
                except PartType.DoesNotExist: 
                    return False 
        return True
