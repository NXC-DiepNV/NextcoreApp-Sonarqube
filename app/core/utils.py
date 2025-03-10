from django.utils.html import format_html

def format_number(obj, field):
    value = getattr(obj, field, 0)
    return format_html(f"{value:,}") if value else "0"

def format_date(obj, field):
    value = getattr(obj, field, '')
    return value.strftime('%m/%Y')