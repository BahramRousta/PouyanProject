import logging
from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import Profile

logger = logging.getLogger('account')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info("Profile created: {}".format(instance.username))