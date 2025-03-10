from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.admin import (
    SliderNumericFilter,
)

from authen_sso.admin import sso_admin_site
from coin.models import Gift
from user_core.core_admin import CoreAdmin


class GiftAdmin(CoreAdmin):
    list_display = ('display_image', 'name', 'coin', 'price', )
    search_fields = ('name',)
    list_filter = (
        ('coin', SliderNumericFilter),
        ('price', SliderNumericFilter),
    )

    def display_image(self, obj):
        if obj.get_image():
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.get_image())
        return _("No Image")
    display_image.short_description = _("Image")

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = _('Active')


sso_admin_site.register(Gift, GiftAdmin)
