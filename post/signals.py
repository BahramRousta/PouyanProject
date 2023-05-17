from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post


@receiver([post_save, post_delete], sender=Post)
def post_cache_version(sender, instance, **kwargs):

    username = instance.author.user.username
    cache_key = f'user_posts_{username}'
    cache.delete(cache_key)