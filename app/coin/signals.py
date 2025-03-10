from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from .models import Wallet

User = get_user_model()


@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    """
    Function is automatic called after user creation.
    By default, it creates a wallet for the user with balance is 0
    """
    if created and not hasattr(instance, 'wallet'):
        try:
            with transaction.atomic():
                Wallet.objects.create(user=instance, balance=0)
        except Exception as e:
            print(f"{_('Error creating wallet for user ')}{instance.id}: {e}")
            raise


@receiver(post_save, sender=User)
def add_user_to_coin_user_group(sender, instance, created, **kwargs):
    """
    Function is automatic run when create new user
    By default will assign `coin_user` group to new user
    """
    if created and not instance.is_superuser:
        group = Group.objects.get(name='coin_user')
        instance.groups.add(group)
