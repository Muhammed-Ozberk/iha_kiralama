from django.forms import ValidationError
from rest_framework import viewsets
from .models import AircraftModel, Aircraft
from parts.models import Part, PartType
from .serializers import (
    AircraftModelSerializer,
    AircraftSerializer,
    DetailedAircraftSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db import transaction


class AircraftModelViewSet(viewsets.ModelViewSet):
    """
    Uçak modellerini yöneten viewset. 
    Bu viewset uçak modelleriyle ilgili CRUD işlemlerini gerçekleştirir.
    """

    queryset = AircraftModel.objects.all()  # Tüm uçak modellerini alır
    serializer_class = AircraftModelSerializer  # Kullanılacak serializer sınıfı


class AircraftViewSet(viewsets.ModelViewSet):
    """
    Uçakları yöneten viewset.
    Uçaklarla ilgili CRUD işlemleri ve detaylı listeleme işlemlerini sağlar.
    """

    queryset = Aircraft.objects.all()  # Tüm uçakları alır
    serializer_class = AircraftSerializer  # Uçak serializer'ı kullanılır

    def list(self, request, *args, **kwargs):
        """
        Uçakları listelemek için kullanılan view.
        - Sayfalama (pagination) desteği ekler.
        - Filtreleme (search) işlemi yapar.
        - Sıralama (sorting) işlemi yapar.
        """

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get("length", 10))  # Sayfalama için page size belirlenir
        paginator.page = int(request.GET.get("start", 0)) // paginator.page_size + 1   

        # Filtreleme işlemi
        search_value = request.GET.get("search[value]", "").strip()   
        queryset = self.get_queryset()
        if search_value:
            # Ad ve model adı üzerinde arama yapılır
            queryset = queryset.filter(
                Q(name__icontains=search_value) |   
                Q(aircraft_model__name__icontains=search_value)   
            )

        # Sıralama işlemi
        order_column = request.GET.get("order[0][column]", 0)
        order_dir = request.GET.get("order[0][dir]", "asc")
        columns = ["id", "name", "aircraft_model__name"]  # Sıralama için kullanılacak alanlar
        if order_column and order_column.isdigit():
            order_field = columns[int(order_column)]  # Sıralanacak alan seçilir
            if order_dir == "desc":
                order_field = f"-{order_field}"  # Azalan sıralama 
            queryset = queryset.order_by(order_field)

        # Sayfalama ve serialize işlemi yapılır
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = DetailedAircraftSerializer(paginated_queryset, many=True)

        response = {
            "draw": int(request.GET.get("draw", 1)),
            "recordsTotal": self.queryset.count(),  # Toplam kayıt sayısı
            "recordsFiltered": queryset.count(),  # Filtrelenmiş kayıt sayısı
            "data": serializer.data,  # Serileştirilmiş uçak verisi
        }
        return Response(response)

    def create(self, request, *args, **kwargs):
        """
        Yeni bir uçak eklemek için kullanılan view. 
        Uçakla birlikte ilgili parçaların stokları da kontrol edilip güncellenir.
        """

        aircraft_data = request.data
        aircraft_model = aircraft_data.get('aircraft_model')

        # Stok kontrolü ve güncelleme işlemini gerçekleştirecek bir fonksiyon ekleyelim
        parts_data = aircraft_data.get("parts", [])

        # Parçaların model uyumunu kontrol et
        if not self.check_parts_model_consistency(parts_data, aircraft_model):
            return Response(
                {
                    "error": "Parts are not consistent with the aircraft model."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if not self.check_and_update_part_stocks(parts_data):
            return Response(
                {"error": "Not enough stock for parts."},  # Parçaların stoklarının yetersiz olduğu durumda hata döner
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializer ile verilerin geçerliliği kontrol edilir
        try:
            self.get_serializer(data=aircraft_data).is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Geçerli ise uçak verisi kaydedilir
        with transaction.atomic():  # Tüm işlemleri bir transaction içinde yapmak için
            aircraft = super().create(request, *args, **kwargs)

            # Parçaların stoklarını güncelle
            self.update_part_stocks(parts_data)

        return Response(aircraft.data, status=status.HTTP_201_CREATED)

    def check_parts_model_consistency(self, parts_data, aircraft_model):
        """
        Parçaların ait olduğu model ile uçak modelinin uyumlu olup olmadığını kontrol eder.
        """
        try:
            aircraft_model_instance = AircraftModel.objects.get(
                id=aircraft_model
            )  # Uçak modelini al
        except AircraftModel.DoesNotExist:
            return False  # Uçak modeli geçerli değilse

        # Parçaların her birinin ait olduğu model ile uçak modelini kontrol et
        for part_id in parts_data:
            try:
                part = Part.objects.get(id=part_id)  # Parçayı al
                if (
                    part.aircraft_model != aircraft_model_instance
                ):  # Parça modeli ile uçak modelini karşılaştır
                    return False
            except Part.DoesNotExist:
                return False  # Parça bulunamazsa

        return True

    def check_and_update_part_stocks(self, parts_data):
        """
        Parçaların stoklarını kontrol eder ve eğer kanat parçası en az 2 adet yoksa
        False döner.
        """

        # Kanat parçası kontrolü ve diğer parçalar için stok kontrolü
        part_types = {part_type.name: part_type for part_type in PartType.objects.all()}
        for part_id in parts_data:
            try:
                part = Part.objects.get(id=part_id)  # Parçayı bul
                if part.part_type.name == "Kanat" and part.quantity_in_stock < 2:
                    return False  # Kanat parçası 2 adet değilse
                if part.quantity_in_stock <= 0:
                    return False  # Diğer parçalar stokta yoksa
            except Part.DoesNotExist:
                return False  # Parça bulunamazsa

        return True

    def update_part_stocks(self, parts_data):
        """
        Parçaların stoklarını günceller.
        Kanat parçasından 2 adet düşürülür, diğer parçaların stoğundan 1 adet düşürülür.
        """
        for part_id in parts_data:
            try:
                part = Part.objects.get(id=part_id)  # Parçayı bul
                if part.part_type.name == "Kanat" and part.quantity_in_stock >= 2:
                    part.quantity_in_stock = part.quantity_in_stock - 2
                elif part.quantity_in_stock > 0:
                    part.quantity_in_stock = part.quantity_in_stock - 1
                part.save()  # Parça stoğu kaydedilir
            except Part.DoesNotExist:
                pass  # Parça bulunamazsa, stok güncellemesi yapılmaz
