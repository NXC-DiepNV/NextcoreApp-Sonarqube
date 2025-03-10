
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.db import models

from unfold.contrib.filters.admin import MultipleChoicesDropdownFilter, RangeDateFilter, MultipleRelatedDropdownFilter
from unfold.contrib.forms.widgets import WysiwygWidget
from decouple import config

from authen_sso.admin import sso_admin_site
from coin.constants import EventType, TransactionStatus
from coin.forms import TransactionForm
from coin.models import Transaction
from coin.permissions import can_change_resource
from user_core.core_admin import CoreAdmin
from user_core.models import CustomUser as User


class TransactionAdmin(CoreAdmin):
    form = TransactionForm
    list_display = (
        'type', 'from_user', 'to_user', 'coin', 'gift', 'status', 'created_at')
    list_filter = (
        ('type', MultipleChoicesDropdownFilter),
        ('event', MultipleRelatedDropdownFilter),
        ('created_by', MultipleRelatedDropdownFilter),
        ('gift', MultipleRelatedDropdownFilter),
        ('created_at', RangeDateFilter),
        ('status', MultipleChoicesDropdownFilter),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    search_fields = ('from_user__username', 'to_user__username', 'description')

    actions = ['approved_transactions', 'reject_transactions']

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = _('Active')

    def approved_transactions(self, request, queryset):
        # Update status of selected transactions to Success
        queryset.update(status=TransactionStatus.STATUS_SUCCESS)
        self.message_user(request, _("Approved selected transactions"))

    approved_transactions.short_description = _(
        "Approved selected transactions")

    def reject_transactions(self, request, queryset):
        queryset.update(status=TransactionStatus.STATUS_FAIL)
        self.message_user(request, _("Reject selected transactions"))

    reject_transactions.short_description = _("Reject selected transactions")

    def has_change_permission(self, request, obj=None):
        return can_change_resource(request, obj, self.opts.app_label) or super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return can_change_resource(request, obj, self.opts.app_label) or super().has_delete_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user  # Pass user params to form
        return form

    def save_form(self, request, form, change):
        form.instance.created_by = request.user
        return self.handle_transaction(request, form, change)

    def handle_deposit_transaction(self, request, form, change):
        """
        Handle deposit transaction
        Function use for admin, do not check negative balance
        """
        coin = form.cleaned_data.get('coin')
        user = form.cleaned_data.get('to_user')

        with transaction.atomic():
            # Update transaction detail
            form.instance.to_wallet_before = user.coin_wallet.balance
            form.instance.to_wallet_after = form.instance.to_wallet_before + coin
            # Update user balance
            user.coin_wallet.balance += coin
            user.coin_wallet.save()

            return super().save_form(request, form, change)

    def handle_withdraw_transaction(self, request, form, change):
        """
        Handle deposit transaction
        Function use for admin, do not check negative balance
        """
        coin = form.cleaned_data.get('coin')
        user = form.cleaned_data.get('to_user')

        with transaction.atomic():
            # Update transaction detail
            form.instance.to_wallet_before = user.coin_wallet.balance
            form.instance.to_wallet_after = form.instance.to_wallet_before - coin

            # Update user balance
            user.coin_wallet.balance -= coin
            user.coin_wallet.save()

            return super().save_form(request, form, change)

    def handle_transfer_transaction(self, request, form, change):
        coin = form.cleaned_data.get('coin')
        from_user = form.cleaned_data.get('from_user')
        to_user = form.cleaned_data.get('to_user')
        fee = coin * 0.1
        with transaction.atomic():
            # From user
            form.instance.from_wallet_before = from_user.coin_wallet.balance
            form.instance.from_wallet_after = form.instance.from_wallet_before - coin
            from_user.coin_wallet.balance = form.instance.from_wallet_after
            from_user.coin_wallet.save()

            # To user
            form.instance.to_wallet_before = to_user.coin_wallet.balance
            form.instance.to_wallet_after = form.instance.to_wallet_before + coin - fee
            to_user.coin_wallet.balance = form.instance.to_wallet_after
            to_user.coin_wallet.save()

            # Add fee to admin
            root_user = User.objects.get(username=config('ROOT_USERNAME'))
            form.instance.admin_wallet_before = root_user.coin_wallet.balance
            form.instance.admin_wallet_after = form.instance.admin_wallet_before + fee
            root_user.coin_wallet.balance = form.instance.admin_wallet_after
            root_user.coin_wallet.save()

            # Fee
            form.instance.fee = fee

            return super().save_form(request, form, change)

    def handle_increase_transaction(self, request, form, change):
        coin = form.cleaned_data.get('coin')
        from_user = User.objects.get(username=config('ROOT_USERNAME'))
        to_user = form.cleaned_data.get('to_user')
        with transaction.atomic():

            # From user
            form.instance.from_wallet_before = from_user.coin_wallet.balance
            form.instance.from_wallet_after = form.instance.from_wallet_before - coin
            from_user.coin_wallet.balance = form.instance.from_wallet_after
            from_user.coin_wallet.save()

            # To user
            form.instance.to_wallet_before = to_user.coin_wallet.balance
            form.instance.to_wallet_after = form.instance.to_wallet_before + coin
            to_user.coin_wallet.balance = form.instance.to_wallet_after
            to_user.coin_wallet.save()

            return super().save_form(request, form, change)

    def handle_decrease_transaction(self, request, form, change):
        coin = form.cleaned_data.get('coin')
        from_user = User.objects.get(username=config('ROOT_USERNAME'))
        to_user = form.cleaned_data.get('to_user')
        with transaction.atomic():

            # From user
            form.instance.from_wallet_before = from_user.coin_wallet.balance
            form.instance.from_wallet_after = form.instance.from_wallet_before + coin
            from_user.coin_wallet.balance = form.instance.from_wallet_after
            from_user.coin_wallet.save()

            # To user
            form.instance.to_wallet_before = to_user.coin_wallet.balance
            form.instance.to_wallet_after = form.instance.to_wallet_before - coin
            to_user.coin_wallet.balance = form.instance.to_wallet_after
            to_user.coin_wallet.save()

            return super().save_form(request, form, change)

    def handle_transaction(self, request, form, change):

        # Request whose status is not success then just save form
        if form.cleaned_data.get('status') != TransactionStatus.STATUS_SUCCESS:
            return super().save_form(request, form, change)

        event_type_handlers = {
            EventType.DEPOSIT: self.handle_deposit_transaction,
            EventType.WITHDRAW: self.handle_withdraw_transaction,
            EventType.TRANSFER: self.handle_transfer_transaction,
            EventType.INCREASE: self.handle_increase_transaction,
            EventType.DECREASE: self.handle_decrease_transaction,
        }

        event_type = form.cleaned_data.get('type')
        handler = event_type_handlers.get(event_type)

        if handler:
            return handler(request, form, change)
        else:
            raise ValueError(f"Unknown event type: {event_type}")


sso_admin_site.register(Transaction, TransactionAdmin)
