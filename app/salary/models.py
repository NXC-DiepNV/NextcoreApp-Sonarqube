from django.db import models
from django.utils.translation import gettext_lazy as _

from user_core.models import BaseModel, CustomUser

class Salary(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='salary_user')
    date = models.DateField(null=True, blank=True)
    total_income  = models.IntegerField(default=0, verbose_name=_('Total income'))
    daily_wage = models.IntegerField(default=0, verbose_name=_('100% Daily Wage'))
    overtime_taxable = models.IntegerField(default=0, verbose_name=_('Overtime (Taxable)'))
    overtime_non_taxable = models.IntegerField(default=0, verbose_name=_('Overtime (Non-Taxable)'))
    employee_insurance_social = models.IntegerField(default=0, verbose_name=_('Employee Social Insurance'))
    employee_insurance_health = models.IntegerField(default=0, verbose_name=_('Employee Health Insurance'))
    employee_insurance_unemployment = models.IntegerField(default=0, verbose_name=_('Employee Unemployment Insurance'))
    count_employee_insurance = models.IntegerField(default=0, verbose_name=_('Employee Insurance'))
    enterprise_insurance_social = models.IntegerField(default=0, verbose_name=_('Enterprise Social Insurance'))
    enterprise_insurance_health = models.IntegerField(default=0, verbose_name=_('Enterprise Health Insurance'))
    enterprise_insurance_unemployment = models.IntegerField(default=0, verbose_name=_('Enterprise Unemployment Insurance'))
    count_enterprise_insurance = models.IntegerField(default=0, verbose_name=_('Enterprise Insurance'))
    personal_income_tax  = models.IntegerField(default=0, verbose_name=_('Personal Income Tax '))
    taxable_income = models.IntegerField(default=0, verbose_name=_('Taxable Income'))
    dependent = models.IntegerField(default=0, verbose_name=_('Dependent'))
    taxable_earnings = models.IntegerField(default=0, verbose_name=_('Taxable Earnings'))
    tax_underpaid_or_overpaid = models.IntegerField(default=0, verbose_name=_('Personal Income Tax Underpaid/Overpaid (if any)'))
    income_additional = models.IntegerField(default=0, verbose_name=_('Additional Income'))
    income_deduction = models.IntegerField(default=0, verbose_name=_('Income Deduction'))
    other = models.IntegerField(default=0, verbose_name=_('Other'))
    working_day = models.FloatField(default=0, verbose_name=_('Working day'))
    count_other_income = models.IntegerField(default=0, verbose_name=_('Other Income / Deductions'))
    actual_income = models.IntegerField(default=0, verbose_name=_('Actual Income'))
    file_payslip = models.CharField(blank=True, null=True, max_length=255)
    file_payslip_protect = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_migration_salary_user_date",
            )
        ]
        app_label = "salary"
        verbose_name = _('Salary')
        verbose_name_plural = _('Salary')
