from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @classmethod
    def create_profile(cls, user):
        """Create a profile for a user if it doesn't exist."""
        profile, created = cls.objects.get_or_create(user=user)
        return profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when a user is created/updated."""
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.create_profile(instance)  # Ensure profile exists even for existing users
