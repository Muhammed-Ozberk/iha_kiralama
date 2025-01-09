from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartTypeViewSet, PartViewSet
from .views import PartListByAircraftModelView

# Router oluşturuyoruz
router = DefaultRouter()
router.register(r"part_types", PartTypeViewSet)
router.register(r"parts", PartViewSet)

urlpatterns = [
    path("", include(router.urls)),  # API için yönlendirme
    path('parts/by_aircraft_model/<int:aircraft_model_id>/', PartListByAircraftModelView.as_view(), name='part-list-by-aircraft-model')
]