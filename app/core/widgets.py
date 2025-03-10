from django import forms
from unfold.widgets import INPUT_CLASSES

class UnfoldCommaNumberWidget(forms.TextInput):
    input_type = 'text'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'formatted-number ' + ' ' . join(INPUT_CLASSES)}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value is None or value == '':
            return ''
        try:
            return '{:,}'.format(int(value))
        except (ValueError, TypeError):
            return value

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value:
            return value.replace(',', '')
        return value
    
    class Media:
        js = ('admin/js/format_number.js',)
