from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse
from django.urls import path
from django.contrib import messages
from django.utils.encoding import force_str
from django.core.exceptions import FieldDoesNotExist
from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static

from unfold.decorators import action
from unfold.views import UnfoldModelAdminViewMixin
from import_export.resources import ModelResource
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    MultipleRelatedDropdownFilter
)

from core.utils import format_date, format_number
from salary.constants import ROLE_MEMBER
from salary.forms import BulkCreateSalaryForm, ExportSalaryForm
from salary.models import Salary
from salary.services import SalaryService
from user_core.core_admin import CoreAdmin
from authen_sso.admin import sso_admin_site

class SalaryBasedViewSync(UnfoldModelAdminViewMixin, ListView):
    model = Salary
    title = _('Bulk create salary')
    permission_required = () 
    template_name = "admin/bulk_create_salary_form.html"
    form_class = BulkCreateSalaryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['app_label'] = self.model._meta.app_label
        context["form"] = BulkCreateSalaryForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """Process data when submitting the form"""
        form = self.form_class(request.POST) 

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
            
            month = int(form.cleaned_data.get("month"))
            year = form.cleaned_data.get("year")
            working_day = form.cleaned_data.get("working_day") or 0
            user = form.cleaned_data.get("user")
            override_salary = form.cleaned_data.get("override_salary")
            underpaid_overpaid = form.cleaned_data.get("underpaid_overpaid") or 0
            increased_income = form.cleaned_data.get("increased_income") or 0
            income_deduction = form.cleaned_data.get("income_deduction") or 0
            other = form.cleaned_data.get("other") or 0
        
            create_bulk_salary = SalaryService.create_bulk_salary_service(user, month, year, working_day, override_salary, underpaid_overpaid, 
                                           increased_income, income_deduction, other)
            if create_bulk_salary:
                messages.success(self.request, _("Data bulk create salary successfully!"))
                return HttpResponseRedirect(reverse("admin:salary_salary_changelist"))

            messages.error(self.request, _('An error occurred while creating data!'))
            return self.render_to_response(self.get_context_data(form=form))

        
    def form_invalid(self, form):
        
        messages.error(self.request, _('An error occurred while creating data!'))
        return self.render_to_response(self.get_context_data(form=form))
        
    
class ExportSalaryView(UnfoldModelAdminViewMixin, ListView):
    model = Salary
    title = _('Export salary')
    permission_required = () 
    template_name = "admin/export_salary_form.html"
    form_class = ExportSalaryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['app_label'] = self.model._meta.app_label
        context["form"] = ExportSalaryForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """Process data when submitting the form"""
        form = ExportSalaryForm(request.POST, request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
            
            file = form.cleaned_data.get("file")
            month = int(form.cleaned_data.get("month"))
            year = form.cleaned_data.get("year")
            user = form.cleaned_data.get("user")
            
            response = SalaryService.export_salary_service(None, file, user, month, year)
            return response

        
    def form_invalid(self, form):
        
        messages.error(self.request, _('An error occurred while exporting data!'))
        return self.render_to_response(self.get_context_data(form=form))


class SalaryResource(ModelResource):
    class Meta:
        model = Salary
        fields = ('user', 'date', 'total_income', 'daily_wage','overtime_taxable', 
                    'overtime_non_taxable', 'employee_insurance_social', 'employee_insurance_health', 
                    'employee_insurance_unemployment', 'count_employee_insurance', 
                    'enterprise_insurance_social', 'enterprise_insurance_health', 'enterprise_insurance_unemployment', 
                    'count_enterprise_insurance', 'personal_income_tax', 'taxable_income', 
                    'dependent', 'taxable_earnings', 'tax_underpaid_or_overpaid', 'income_additional', 
                    'income_deduction', 'other', 'count_other_income', 'actual_income')
        
    def get_field_name(self, field):
        field_name = field.attribute if hasattr(field, 'attribute') else field
        try:
            field_obj = self._meta.model._meta.get_field(field_name)
            return force_str(field_obj.verbose_name)
        except FieldDoesNotExist:
            return field_name
        except Exception as e:
            return field_name

    def get_export_headers(self, selected_fields=None):
        fields_to_export = selected_fields if selected_fields else self.get_fields()
        return [self.get_field_name(field) for field in fields_to_export]

class SalaryAdmin(CoreAdmin):

    list_display = ('user', 'get_role', 'date_format', 'total', 'daily','overtime_taxable', 
                    'overtime_non_taxable', 'insurance_social_employee', 'insurance_health_employee', 
                    'insurance_unemployment_employee', 'insurance_employee', 
                    'insurance_social_enterprise', 'insurance_health_enterprise', 'insurance_unemployment_enterprise', 
                    'insurance_enterprise', 'income_tax_personal', 'income_taxable', 
                    'dependent', 'earnings_taxable', 'underpaid_or_overpaid', 'additional_income', 
                    'deduction_income', 'other_format', 'income_count_other', 'income_actual', 'view_payslip')
    search_fields = ('user__username',)
    list_filter = [('user', MultipleRelatedDropdownFilter), ('date', RangeDateFilter)]

    actions_list = [
        "bulk_create_salary",
        "export_salary",
    ]

    actions = [
        "export_salary_view",
        "send_mail_payslip"
    ]

    @admin.action(description=_('Export salary'))
    def export_salary_view(self, request, queryset):
        return SalaryService.export_salary_service(queryset)
    
    @admin.action(description=_('Send mail payslip'))
    def send_mail_payslip(self, request, queryset):
        sendmail =  SalaryService.handle_sendmail_payslip(queryset)
        if sendmail:
            messages.success(request, _("Email sent payslip successfully!"))
            return HttpResponseRedirect(reverse("admin:salary_salary_changelist"))
        messages.error(request, _('Email sent payslip error!'))
        return HttpResponseRedirect(reverse("admin:salary_salary_changelist"))

    @action(description=_("Bulk create salary"))
    def bulk_create_salary(self, request):
        return HttpResponseRedirect(reverse('admin:bulk_create_salary'))
    
    @action(description=_("Export salary"))
    def export_salary(self, request):
        return HttpResponseRedirect(reverse('admin:export_salary'))
    
    def get_role(self, obj):
        return ROLE_MEMBER
    get_role.short_description = _('Role')

    def generate_formatted_field(field_name, type = None):
        def formatted_field(self, obj):
            if type is not None:
                return format_date(obj, field_name)
            
            return format_number(obj, field_name)
        
        formatted_field.admin_order_field = field_name
        formatted_field.short_description = Salary._meta.get_field(field_name).verbose_name
        return formatted_field
    
    total = generate_formatted_field('total_income')
    daily = generate_formatted_field('daily_wage')

    insurance_social_employee = generate_formatted_field('employee_insurance_social')
    insurance_health_employee = generate_formatted_field('employee_insurance_health')
    insurance_unemployment_employee = generate_formatted_field('employee_insurance_unemployment')
    insurance_employee = generate_formatted_field('count_employee_insurance')
    insurance_social_enterprise = generate_formatted_field('enterprise_insurance_social')
    insurance_health_enterprise = generate_formatted_field('enterprise_insurance_health')
    insurance_unemployment_enterprise = generate_formatted_field('enterprise_insurance_unemployment')
    insurance_enterprise = generate_formatted_field('count_enterprise_insurance')
    income_tax_personal = generate_formatted_field('personal_income_tax')
    income_taxable = generate_formatted_field('taxable_income')
    earnings_taxable = generate_formatted_field('taxable_earnings')
    underpaid_or_overpaid = generate_formatted_field('tax_underpaid_or_overpaid')
    additional_income = generate_formatted_field('income_additional')
    deduction_income = generate_formatted_field('income_deduction')
    other_format = generate_formatted_field('other')
    income_count_other = generate_formatted_field('count_other_income')
    income_actual = generate_formatted_field('actual_income')
    
    date_format = generate_formatted_field('date', 'date')

    def view_payslip(self, obj):
        if obj.file_payslip:
            relative_path = obj.file_payslip.replace("./app/salary/static/", "")
            file_url = static(relative_path)
            return format_html('<a href="{}" target="_blank">{}</a>', file_url, _("Show payslip"))
        return _("No file")
    
    view_payslip.short_description = _("File Payslip")

    def get_urls(self):
        return super().get_urls() + [
            path(
                "bulk-create-salary",
                SalaryBasedViewSync.as_view(model_admin=self),
                name="bulk_create_salary"
            ),
            path(
                "export-salary",
                ExportSalaryView.as_view(model_admin=self),
                name="export_salary"
            ),
        ]
    

sso_admin_site.register(Salary, SalaryAdmin)
