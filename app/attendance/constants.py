from django.utils.translation import gettext_lazy as _, get_language
import calendar

def get_month_choices():
    lang = get_language()
    if lang == "vi":
        return [(str(i), _("Tháng") + f" {i}") for i in range(1, 13)]
    else:
        return [(str(i), _(calendar.month_name[i])) for i in range(1, 13)]

MONTH_CHOICES = get_month_choices()

MAX_LEAVE = 12

ON_LEAVE = 'Nghỉ phép'

ONE_DAY = 86400
