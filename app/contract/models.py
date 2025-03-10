from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

from user_core.models import BaseModel, CustomUser

def default_end_date():
    return date.today() + timedelta(days=180)

class Contract(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='contract_user')
    salary_gross  = models.IntegerField(default=0, verbose_name=_('Gross Salary'))
    salary_basic = models.IntegerField(default=0, verbose_name=_('Basic Salary'))
    allowance_clothing = models.IntegerField(default=415000, verbose_name=_('Clothing Allowance'))
    allowance_lunch = models.IntegerField(default=730000, verbose_name=_('Lunch Allowance'))
    allowance_housing = models.IntegerField(default=0, verbose_name=_('Housing Allowance'))
    allowance_phone = models.IntegerField(default=0, verbose_name=_('Phone Allowance'))
    allowance_fuel = models.IntegerField(default=0, verbose_name=_('Fuel Allowance'))
    allowance_position = models.IntegerField(default=0, verbose_name=_('Position Allowance'))
    allowance_responsibility = models.IntegerField(default=0, verbose_name=_('Responsibility Allowance'))
    bonus_kpi = models.IntegerField(default=0, verbose_name=_('KPI Bonus'))
    deduction_personal = models.IntegerField(default=11000000, verbose_name=_('Personal Deduction'))
    number_dependents = models.IntegerField(default=0, verbose_name=_('Number of Dependents'))
    signing_date = models.DateField(verbose_name=_('Contract Signing Date'))
    start_date = models.DateField(default=date.today, verbose_name=_('Contract Start Date'))
    end_date = models.DateField(default=default_end_date, verbose_name=_('Contract End Date'))
    is_current_contract = models.BooleanField(default=True, verbose_name="Current Contract")

    def save(self, *args, **kwargs):
        if self.is_current_contract:
            Contract.objects.filter(user=self.user, is_current_contract=True).exclude(pk=self.pk).update(is_current_contract=False)
        super().save(*args, **kwargs)

    class Meta:
        app_label = "contract"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contract')
