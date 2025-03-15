from authentication_app.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from profile_app.models import Profile


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
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
    else:
        profile = instance.profile
        profile.username = instance.username
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.address = instance.address
        profile.phone = instance.phone
        profile.email = instance.email
        profile.save()
