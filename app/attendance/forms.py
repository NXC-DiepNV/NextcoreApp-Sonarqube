from decouple import config
from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from unfold.widgets import UnfoldAdminIntegerFieldWidget, UnfoldAdminSelectWidget, UnfoldAdminSelectMultipleWidget

from attendance.constants import MONTH_CHOICES
from user_core.models import CustomUser

class LarkSyncForm(forms.Form):

    user = forms.MultipleChoiceField(
        label=_("User"),
        required=False,
        widget=UnfoldAdminSelectMultipleWidget(
                attrs={
                    "data-theme": "admin-autocomplete",
                    "class": "unfold-admin-autocomplete admin-autocomplete",
                }
            )
    )
    
    month = forms.ChoiceField(
        label=_("Month"),
        required=True,
        widget=UnfoldAdminSelectWidget,
    )

    year = forms.IntegerField(
        label=_("Year"),
        required=True,
        widget=UnfoldAdminIntegerFieldWidget,
    )

    working_day = forms.IntegerField(required=False, label=_("Number of working days of the month"), widget=UnfoldAdminIntegerFieldWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_choices = [(user.username, user.username) for user in CustomUser.objects.exclude(username=config('ROOT_USERNAME'))]
        self.fields['user'].choices = user_choices

        month_choices = MONTH_CHOICES
        self.fields['month'].choices = [("", _("-- Choose month --"))] + month_choices

        self.fields['year'].initial = datetime.now().year

    class Media:
        js = (
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
            "admin/js/jquery.init.js",
            "unfold/js/select2.init.js",
        )
        css = {
            "screen": (
                "admin/css/vendor/select2/select2.css",
                "admin/css/autocomplete.css",
            ),
        }
