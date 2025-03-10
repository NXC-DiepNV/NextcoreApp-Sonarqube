from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from user_core.constants import Permission, PositionType


class BaseModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    @classmethod
    def active(cls):
        return cls.objects.filter(deleted_at__isnull=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):

    business_email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_contract = models.DateField(blank=True, null=True)
    position = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=PositionType.CHOICE
    )
    citizen_identity = models.CharField(blank=True, null=True, max_length=15)
    bank_number_id = models.CharField(blank=True, null=True, max_length=255)
    bank_name = models.CharField(blank=True, null=True, max_length=255)
    bank_beneficiary = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        db_table = 'user_core_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

        permissions = [
            (Permission.CAN_CHANGE_OWN_INFO,
             _('Can change own info')),

        ]

    def __str__(self):
        return self.username


class CustomGroup(Group, BaseModel):
    class Meta:
        db_table = 'user_core_group'
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        return self.name
