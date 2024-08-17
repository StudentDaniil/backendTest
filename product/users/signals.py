from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Balance

from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
