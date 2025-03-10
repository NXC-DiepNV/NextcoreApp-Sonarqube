from django.db import models
from django.utils.translation import gettext_lazy as _

from user_core.models import BaseModel, CustomUser
from .constants import EventType, TransactionStatus, Permission


class Wallet(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='coin_wallet')
    balance = models.IntegerField(
        default=0, verbose_name=_('coin balance'))

    def __str__(self):
        return f"{self.user.username} - {self.balance}"

    class Meta:
        # Display name in admin site
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')
        permissions = [
            (Permission.CAN_CHANGE_WALLET_BALANCE, _('Can change wallet balance')),
        ]


class Gift(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Gift name'))
    coin = models.IntegerField(verbose_name=_('coin'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Price'))
    purchase_link = models.URLField(
        blank=True, null=True, verbose_name=_('Purchase link'))
    image = models.ImageField(
        upload_to='gifts/', blank=True, null=True, verbose_name=_('Image file'))
    image_url = models.URLField(
        blank=True, null=True, verbose_name=_('Image link'))

    def get_image(self):
        return self.image.url if self.image else self.image_url

    def __str__(self):
        return f"{self.name} - {self.coin}"

    class Meta:
        verbose_name = _('Gift')
        verbose_name_plural = _('Gifts')


class Event(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Event name'))
    type = models.CharField(
        max_length=10, choices=EventType.CHOICES, verbose_name=_('Event type'))
    coin = models.IntegerField(verbose_name=_('coin'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class Transaction(BaseModel):
    type = models.CharField(
        max_length=10, choices=EventType.CHOICES, verbose_name=_('Event type'))
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name=_('Event'), blank=True, null=True)
    gift = models.ForeignKey(
        Gift, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Gift'))
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='from_transactions', blank=True, null=True)
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='to_transactions', blank=True, null=True)
    coin = models.IntegerField(verbose_name=_('coin'))
    from_wallet_before = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance before transaction of sender'))
    from_wallet_after = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance after transaction of sender'))
    to_wallet_before = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance before transaction of receiver'))
    to_wallet_after = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance after transaction of receiver'))
    fee = models.IntegerField(default=0, verbose_name=_('Transaction fee'))
    admin_wallet_before = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance before transaction of admin'))
    admin_wallet_after = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('coin balance after transaction of admin'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('Description'))
    status = models.CharField(
        max_length=10, choices=TransactionStatus.CHOICES, default=TransactionStatus.STATUS_PENDING, verbose_name=_('Status'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'))
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='created_transactions', blank=True, null=True)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        permissions = [
            (Permission.CAN_CHANGE_TRANSACTION_STATUS,
             _('Can change transaction status')),

        ]

    def __str__(self):
        return f"{self.created_at} - {self.status}"
