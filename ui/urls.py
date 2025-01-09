from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("list-part/", views.list_part, name="list_part"),
    path("create-part/", views.create_part, name="create_part"),
    path("create-air-vehicle/", views.create_air_vehicle, name="create-air-vehicle"),
    path("list-air-vehicle/", views.list_air_vehicle, name="list-air-vehicle"),
]
