from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from unfold.contrib.filters.admin import (
    SingleNumericFilter,
    RangeNumericFilter
)

from authen_sso.admin import sso_admin_site
from contract.forms import ContractForm
from contract.models import Contract
from user_core.core_admin import CoreAdmin

class ContractAdmin(CoreAdmin):
    form = ContractForm
    list_display = ('user', 'gross', 'basic','clothing', 
                    'lunch', 'housing', 'phone', 'fuel', 'position', 
                    'responsibility', 'kpi', 'personal', 'number_dependents', 
                    'signing', 'start', 'end', 'is_current_contract')
    search_fields = ('user__username',)
    list_filter = [('salary_gross', RangeNumericFilter), ('number_dependents', SingleNumericFilter)]

    def format_number(self, obj, field):
        value = getattr(obj, field, 0)
        return format_html(f"{value:,}") if value else "0"

    def generate_formatted_field(field_name, type = None):
        def formatted_field(self, obj):
            if type is not None:
                return self.format_date(obj, field_name)
            
            return self.format_number(obj, field_name)
        
        formatted_field.admin_order_field = field_name
        formatted_field.short_description = Contract._meta.get_field(field_name).verbose_name
        return formatted_field
    
    def format_date(self, obj, field):
        value = getattr(obj, field, '')
        return value.strftime('%d/%m/%Y')

    gross = generate_formatted_field('salary_gross')
    basic = generate_formatted_field('salary_basic')
    clothing = generate_formatted_field('allowance_clothing')
    lunch = generate_formatted_field('allowance_lunch')
    housing = generate_formatted_field('allowance_housing')
    phone = generate_formatted_field('allowance_phone')
    fuel = generate_formatted_field('allowance_fuel')
    position = generate_formatted_field('allowance_position')
    responsibility = generate_formatted_field('allowance_responsibility')
    kpi = generate_formatted_field('bonus_kpi')
    personal = generate_formatted_field('deduction_personal')

    signing = generate_formatted_field('signing_date', 'date')
    start = generate_formatted_field('start_date', 'date')
    end = generate_formatted_field('end_date', 'date')


sso_admin_site.register(Contract, ContractAdmin)
