from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.admin import (
    MultipleChoicesDropdownFilter,
)

from authen_sso.admin import sso_admin_site
from coin.models import Event
from user_core.core_admin import CoreAdmin


class EventAdmin(CoreAdmin):
    list_display = ('name', 'type', 'coin')
    search_fields = ('name', 'type')
    list_filter = (
        ('type', MultipleChoicesDropdownFilter),
    )

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = _('Active')


sso_admin_site.register(Event, EventAdmin)
