
from unfold.contrib.filters.admin import SliderNumericFilter
from django.utils.translation import gettext_lazy as _

from authen_sso.admin import sso_admin_site
from coin.models import Wallet
from user_core.core_admin import CoreAdmin


class WalletAdmin(CoreAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
    list_filter = (('balance', SliderNumericFilter),)

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = _('Active')


sso_admin_site.register(Wallet, WalletAdmin)
