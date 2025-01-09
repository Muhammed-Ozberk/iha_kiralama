from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import PartType

@receiver(post_save, sender=PartType)
def create_parttype_permissions(sender, instance, created, **kwargs):
    """
    Yeni bir PartType oluşturulduğunda otomatik olarak izin ekler.
    """
    if created:  # Sadece yeni bir PartType oluşturulduğunda çalışır 
        content_type = ContentType.objects.get_for_model(PartType)
        
        # Yeni bir 'produce_' izin kodu oluşturulur ve iziz eklenir
        Permission.objects.get_or_create(
            codename=f"produce_{instance.name.lower()}",  
            name=f"Can produce {instance.name}",  
            content_type=content_type,  
        )
