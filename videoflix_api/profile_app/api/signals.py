# profile_app/api/signals.py
from authentication_app.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from profile_app.models import Profile


@receiver(post_save, sender=CustomUser)
def create_profile_from_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            address=instance.address,
            phone=instance.phone,
            email=instance.email
        )

@receiver(post_save, sender=Profile)
def update_user_from_profile(sender, instance, **kwargs):
    user = instance.user  
    user.first_name = instance.first_name  
    user.last_name = instance.last_name    
    user.email = instance.email            
    user.address = instance.address       
    user.phone = instance.phone          
    user.username = instance.username      
    user.save()