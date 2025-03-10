from django import forms
from core.widgets import UnfoldCommaNumberWidget
from contract.models import Contract
class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'salary_gross': UnfoldCommaNumberWidget(),
            'salary_basic': UnfoldCommaNumberWidget(),
            'allowance_clothing': UnfoldCommaNumberWidget(),
            'allowance_lunch': UnfoldCommaNumberWidget(),
            'allowance_housing': UnfoldCommaNumberWidget(),
            'allowance_phone': UnfoldCommaNumberWidget(),
            'allowance_fuel': UnfoldCommaNumberWidget(),
            'allowance_position': UnfoldCommaNumberWidget(),
            'allowance_responsibility': UnfoldCommaNumberWidget(),
            'bonus_kpi': UnfoldCommaNumberWidget(),
            'deduction_personal': UnfoldCommaNumberWidget(),
        }
