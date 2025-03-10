from decouple import config
from datetime import datetime
from django import forms
import os
from django.utils.translation import gettext_lazy as _
from unfold.widgets import UnfoldAdminIntegerFieldWidget, UnfoldAdminSelectWidget, UnfoldAdminSelectMultipleWidget, UnfoldBooleanWidget, UnfoldAdminFileFieldWidget

from attendance.constants import MONTH_CHOICES
from user_core.models import CustomUser

class BulkCreateSalaryForm(forms.Form):

    user = forms.MultipleChoiceField(
        label=_("User"),
        required=True,
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

    underpaid_overpaid = forms.IntegerField(required=False, label=_("Personal income tax underpaid/overpaid (if any)"), widget=UnfoldAdminIntegerFieldWidget)

    increased_income = forms.IntegerField(required=False, label=_("Increased income"), widget=UnfoldAdminIntegerFieldWidget)

    income_deduction = forms.IntegerField(required=False, label=_("Income deduction"), widget=UnfoldAdminIntegerFieldWidget)

    other = forms.IntegerField(required=False, label=_("Other"), widget=UnfoldAdminIntegerFieldWidget)

    override_salary = forms.BooleanField(required=False, label=_("Override salary"), widget=UnfoldBooleanWidget)

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


class ExportSalaryForm(forms.Form):
    user = forms.MultipleChoiceField(
        label=_("User"),
        required=True,
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

    file = forms.FileField(
        required=False,
        label="Upload Template Excel",
        help_text="Select the sample Excel file (.xlsx hoặc .xls)",
        widget=UnfoldAdminFileFieldWidget
    )

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

