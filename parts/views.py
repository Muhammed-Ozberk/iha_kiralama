from rest_framework import viewsets
from .models import PartType, Part
from .serializers import PartTypeSerializer, PartSerializer
from .permissions import CanProducePartPermission
from .utils import can_produce_part_type
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status

# Sayfalama işlemi için kullanılan sınıf.
class PartPagination(PageNumberPagination):
    page_size = 10   
    page_size_query_param = "page_size"  
    max_page_size = 100   

# Parça tiplerini yöneten viewset.
class PartTypeViewSet(viewsets.ModelViewSet):
    """
    PartType nesneleri yönetir.
    Sadece kullanıcının üretmeye yetkili olduğu parça tiplerini döndürür.
    """

    queryset = PartType.objects.all()  # Tüm parça tiplerini alınır
    serializer_class = PartTypeSerializer   

    def get_queryset(self):
        """
        Kullanıcının üretmeye yetkili olduğu parça tiplerini döndüürür.
        `can_produce_part_type` fonksiyonu kullanılarak kullanıcıya ait izinli parça tipleri belirlenir.
        """
        user = self.request.user   
        allowed_part_types = can_produce_part_type(user)  # Kullanıcının izinli olduğu parça tiplerini alınır

        # İzinli parça tiplerinin ID'lerini alınır
        part_type_ids = allowed_part_types.get("part_type_ids", [])
        return PartType.objects.filter(id__in=part_type_ids)  # Filtrelenmiş parça tiplerini döndürür

# Parçaları yöneten viewset.
class PartViewSet(viewsets.ModelViewSet):
    """
    Part nesnelerini yönetir.
    Kullanıcının sadece üretmeye yetkili olduğu parçaları döndürür.
    """

    queryset = Part.objects.all()   
    serializer_class = PartSerializer  # Serileştirici sınıfı
    permission_classes = [CanProducePartPermission]  # Kullanıcı izinlerini kontrol eden sınıf
    pagination_class = PartPagination  # Sayfalama sınıfı

    def get_queryset(self):
        """
        Kullanıcının sadece üretmeye yetkili olduğu parça tiplerine ait parçalar döndürülür.
        Kullanıcının izinli olduğu parça tipleri `can_produce_part_type` fonksiyonu ile belirlenir.
        """
        user = self.request.user   
        allowed_part_types = can_produce_part_type(user)   
        part_type_ids = allowed_part_types.get("part_type_ids", [])  # İzinli parça tiplerinin ID'leri alınır

        # Eğer izinli parça tipleri varsa, bu parçalara göre filtreleme yapılır
        if part_type_ids:
            return Part.objects.filter(part_type__id__in=part_type_ids)  # İzinli parça tiplerine ait parçaları döndürülür
        else:
            return Part.objects.none()  # Eğer izinli parça yoksa, boş queryset döner

    def list(self, request, *args, **kwargs):
        """
        DataTables ile uyumlu bir JSON yanıt döndürür.
        Eğer sayfa bilgisi gelmezse tüm listeyi döner. Sayfa ve sayfa boyutu parametreleri varsa,
        sayfalama işlemi yapılır.
        """
        search = request.GET.get("search[value]", None)   
        page = request.GET.get("page", None)   
        page_size = request.GET.get("page_size", None)   

        queryset = self.get_queryset()

        # Arama filtresi uygulanır
        if search:
            queryset = queryset.filter(name__icontains=search)   

        records_total = queryset.count()  # Toplam kayıt sayısını alınır

        # Eğer sayfa bilgisi yoksa, tüm listeyi döndürülür
        if page is None or page_size is None:
            serializer = self.get_serializer(queryset, many=True)
            response = {
                "draw": int(request.GET.get("draw", 1)),
                "recordsTotal": records_total,
                "recordsFiltered": records_total,  # Filtrelenmiş kayıt sayısı
                "data": serializer.data,
            }
            return Response(response)

        # Sayfa ve sayfa boyutu bilgisi varsa, sayfalama işlemi yapılır
        page = int(page)   
        page_size = int(page_size)   
        start = (page - 1) * page_size  
        end = start + page_size   
        queryset = queryset[start:end]   

        serializer = self.get_serializer(queryset, many=True)

        response = {
            "draw": int(request.GET.get("draw", 1)),
            "recordsTotal": records_total,
            "recordsFiltered": records_total,  
            "data": serializer.data,  
        }
        return Response(response)

    def create(self, request, *args, **kwargs):
        """
        Aynı parça tipi ve uçak modeli varsa sadece stok güncellemesi yapar.
        """
        part_type = request.data.get("part_type")
        aircraft_model = request.data.get("aircraft_model")
        quantity = int(request.data.get("quantity_in_stock", 0))

        # Aynı parça tipi ve uçak modeline sahip bir kayıt varsa onu güncelle
        existing_part = Part.objects.filter(
            part_type_id=part_type, aircraft_model_id=aircraft_model
        ).first()

        if existing_part:
            existing_part.quantity_in_stock += quantity
            existing_part.save()

            # Güncellenen kaydı döndür
            serializer = self.get_serializer(existing_part)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Eğer aynı parça tipi ve uçak modeli yoksa yeni bir kayıt oluştur
        return super().create(request, *args, **kwargs)


# Belirli bir aircraft_model_id'ye göre parçaları listeleyen API view
class PartListByAircraftModelView(APIView):
    """
    Belirli bir aircraft_model_id'ye göre parça listesini döndürür.
    """

    def get(self, request, aircraft_model_id, *args, **kwargs):
        try:
            # aircraft_model_id'ye göre parçaları filtrelenir
            parts = Part.objects.filter(aircraft_model_id=aircraft_model_id)
            serializer = PartSerializer(parts, many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Part.DoesNotExist: 
            return Response({"detail": "Parts not found for this aircraft model."}, status=status.HTTP_404_NOT_FOUND)
