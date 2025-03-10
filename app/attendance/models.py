from django.db import models
from django.utils.translation import gettext_lazy as _

from user_core.models import BaseModel, CustomUser

class Attendance(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='attendance_user')
    date = models.DateField(null=True, blank=True)
    take_leave_month = models.FloatField(verbose_name=_('Take leave this month'))
    leave_taken = models.FloatField(verbose_name=_('Number of days off during the year'))
    maximum_leave = models.IntegerField(verbose_name=_('Maximum leave'))
    working_days_month = models.FloatField(verbose_name=_('Number of working days in the month'))
    actual_ot = models.FloatField(verbose_name=_('Actual OT hours'))
    coefficient_ot = models.FloatField(verbose_name=_('Number of OT hours multiplied by coefficient'))
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_migration_attendance_user_date",
            )
        ]
        app_label = "attendance"
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
