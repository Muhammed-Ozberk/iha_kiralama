# Generated by Django 5.1.4 on 2025-01-09 02:53

from django.db import migrations


def create_team_data(apps, schema_editor):
    # Her bir takım için izinler tanımlanıyor.
    teams = [
        {
            "name": "Kanat Takımı",
            "permissions": [
                # Kanat Takımı'nın sahip olduğu izinler
                "add_parttype",
                "change_parttype",
                "delete_parttype",
                "view_parttype",  # Parça tipi izinleri
                "produce_kanat",  # Kanat üretme izni
                "add_part",
                "change_part",
                "delete_part",
                "view_part",  # Parça ile ilgili izinler
                "add_aircraftmodel",
                "change_aircraftmodel",
                "delete_aircraftmodel",
                "view_aircraftmodel",  # Uçak modeli ile ilgili izinler
            ],
        },
        {
            "name": "Gövde Takımı",
            "permissions": [
                # Gövde Takımı'nın sahip olduğu izinler
                "add_parttype",
                "change_parttype",
                "delete_parttype",
                "view_parttype",  # Parça tipi izinleri
                "produce_gövde",  # Gövde üretme izni
                "add_part",
                "change_part",
                "delete_part",
                "view_part",  # Parça ile ilgili izinler
                "add_aircraftmodel",
                "change_aircraftmodel",
                "delete_aircraftmodel",
                "view_aircraftmodel",  # Uçak modeli ile ilgili izinler
            ],
        },
        {
            "name": "Kuyruk Takımı",
            "permissions": [
                # Kuyruk Takımı'nın sahip olduğu izinler
                "add_parttype",
                "change_parttype",
                "delete_parttype",
                "view_parttype",  # Parça tipi izinleri
                "produce_kuyruk",  # Kuyruk üretme izni
                "add_part",
                "change_part",
                "delete_part",
                "view_part",  # Parça ile ilgili izinler
                "add_aircraftmodel",
                "change_aircraftmodel",
                "delete_aircraftmodel",
                "view_aircraftmodel",  # Uçak modeli ile ilgili izinler
            ],
        },
        {
            "name": "Aviyonik Takımı",
            "permissions": [
                # Aviyonik Takımı'nın sahip olduğu izinler
                "add_parttype",
                "change_parttype",
                "delete_parttype",
                "view_parttype",  # Parça tipi izinleri
                "produce_aviyonik",  # Aviyonik üretme izni
                "add_part",
                "change_part",
                "delete_part",
                "view_part",  # Parça ile ilgili izinler
                "add_aircraftmodel",
                "change_aircraftmodel",
                "delete_aircraftmodel",
                "view_aircraftmodel",  # Uçak modeli ile ilgili izinler
            ],
        },
        {
            "name": "Montaj Takımı",
            "permissions": [
                # Montaj Takımı'nın sahip olduğu izinler
                "view_part",  # Parçaları görüntüleme izni
                "view_parttype",  # Parça tiplerini görüntüleme izni
                "add_aircraft",
                "change_aircraft",
                "delete_aircraft",
                "view_aircraft",  # Uçak ile ilgili izinler
                "add_aircraftmodel",
                "change_aircraftmodel",
                "delete_aircraftmodel",
                "view_aircraftmodel",  # Uçak modeli ile ilgili izinler
            ],
        },
    ]

    # Django'nun Group ve Permission modelleri
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for team_data in teams:
        # Takım adıyla grup oluşturuluyor ya da var olan grup alınıyor
        group, created = Group.objects.get_or_create(name=team_data["name"])

        # İzinler alınıyor ve grup ile ilişkilendiriliyor
        for perm_codename in team_data["permissions"]:
            # İzin, codename ile bulunuyor
            permission = Permission.objects.get(codename=perm_codename)
            # Bulunan izin gruba ekleniyor
            group.permissions.add(permission)

def create_admin_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="admin").exists():
        user = User.objects.create_superuser("admin", "admin123")


class Migration(migrations.Migration):

    dependencies = []

    # Migration işlemleri
    operations = [
        migrations.RunPython(create_team_data),
        migrations.RunPython(create_admin_user),
    ]