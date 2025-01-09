from django.contrib import admin
from .models import PartType, Part

@admin.register(PartType)
class PartTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # Admin panelinde gösterilecek alanlar
    search_fields = ("name",)  

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "part_type", "aircraft_model", "quantity_in_stock")  # Admin panelinde gösterilecek alanlar
    search_fields = ("part_type",)   
