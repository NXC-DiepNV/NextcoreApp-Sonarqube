from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.contrib.filters.admin import MultipleRelatedDropdownFilter
from decouple import config

from authen_sso.admin import sso_admin_site
from user_core.core_admin import CoreAdmin
from user_core.models import CustomGroup, CustomUser
from user_core.permissions import can_change_resource, is_can_view_full


class UserAdmin(BaseUserAdmin, CoreAdmin):
    model = CustomUser
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['username', 'first_name',
                    'last_name', 'phone', 'date_of_birth', 'email', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = (
        ('is_active'),
        ('groups', MultipleRelatedDropdownFilter)
    )

    fieldsets = (
        (
            None, {"fields": ("username", "password")}
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "date_of_birth",
                    "email",
                    "avatar",
                    "position",
                ),
                "classes": ["tab"],
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Non-public info"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "date_of_contract",
                    "business_email",
                    "citizen_identity",
                    "bank_number_id",
                    "bank_name",
                    "bank_beneficiary",
                ),
                "classes": ["tab"],
            }
        ),
    )

    def has_change_permission(self, request, obj=None):
        return can_change_resource(request, obj, app_label=self.opts.app_label) or super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return can_change_resource(request, obj, app_label=self.opts.app_label) or super().has_delete_permission(request, obj)

    def save_model(self, request, obj: CustomUser, form, change):
        if not change:
            obj.is_staff = True
            obj.business_email = f"{obj.username}@{config('EMAIL_DOMAIN')}"
        return super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if not is_can_view_full(request, obj):
            fieldsets = [
                (title, fields) for title, fields in fieldsets
                if title != _("Non-public info")
            ]
        return fieldsets


class GroupAdmin(BaseGroupAdmin, CoreAdmin):
    pass


sso_admin_site.register(CustomUser, UserAdmin)
sso_admin_site.register(CustomGroup, GroupAdmin)
