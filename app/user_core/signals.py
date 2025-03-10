from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_member_group(sender, instance, created, **kwargs):
    """
    Function is automatic run when create new user
    By default will assign `user member` group to new user
    """
    if created and not instance.is_superuser:
        group = Group.objects.get(name='user_member')
        instance.groups.add(group)
