from parts.models import PartType

def can_produce_part(user, part_type):
    """
    Kullanıcının belirli bir PartType üretme yetkisi olup olmadığını kontrol eder.
    """
    codename = f"parts.produce_{part_type.name.lower()}"
    return user.has_perm(codename)


def can_produce_part_type(user,):
    """
    Kullanıcının belirli bir PartType üretme yetkisi olup olmadığını kontrol eder.
    Ayrıca, kullanıcının izinli olduğu parça tiplerinin isimlerini veya ID'lerini döndüren bir fonksiyon.
    """

    # Kullanıcının sahip olduğu tüm izinleri alıyoruz
    permissions = user.get_all_permissions()

    # 'produce_' ile başlayan izinleri filtreliyoruz
    user_allowed_parts = [
        perm for perm in permissions if perm.startswith("parts.produce_")
    ]

    # Kullanıcının izinli olduğu tüm parça tiplerinin isimlerini döndürmek için
    allowed_part_names = []
    allowed_part_ids = []

    for part_type in PartType.objects.all():
        # Her bir parça tipi için izin olup olmadığını kontrol ediyoruz
        codename = f"produce_{part_type.name.lower()}"
        if f"parts.{codename}" in user_allowed_parts:
            allowed_part_names.append(
                part_type.name
            )  # İzinli parça tipinin ismini ekliyoruz
            allowed_part_ids.append(
                part_type.id 
            )  # İzinli parça tipinin ID'sini ekliyoruz


    # İzinli tüm parça tiplerinin isimlerini veya ID'lerini döndürüyoruz
    return {
        "part_type_ids": allowed_part_ids, 
    }
