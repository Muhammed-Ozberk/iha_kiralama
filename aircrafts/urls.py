from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftModelViewSet, AircraftViewSet

# API için router oluşturulur ve view'larla ilişkilendirilir.
router = DefaultRouter()
router.register(r"aircraft_models", AircraftModelViewSet)  # Uçak modelleri için view seti
router.register(r"aircrafts", AircraftViewSet)  # Uçaklar için view seti

urlpatterns = [
    path("", include(router.urls)),  # Router URL'leri dahil edilir
]
