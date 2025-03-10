
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView
from utils.datetime_core import DateTimeCore

from unfold.contrib.filters.admin import (
    RangeDateFilter,
    MultipleRelatedDropdownFilter
)
from unfold.decorators import action
from unfold.views import UnfoldModelAdminViewMixin

from attendance.forms import LarkSyncForm
from attendance.models import Attendance
from attendance.services import handle_leaves_or_overtime_works
from attendance.utils.attendance_utils import AttendanceUtils
from authen_sso.admin import sso_admin_site
from user_core.core_admin import CoreAdmin
from user_core.models import CustomUser


class AttendanceBasedViewSync(UnfoldModelAdminViewMixin, ListView):
    model = Attendance
    title = _('Lark synchronized data')
    permission_required = () 
    template_name = "admin/lark_sync_form.html"
    form_class = LarkSyncForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['app_label'] = self.model._meta.app_label
        context["form"] = LarkSyncForm()
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

            if not user:
                user = list(CustomUser.objects.exclude(username="admin").values_list("username", flat=True))

            data = AttendanceUtils.get_attendance_user_approvals(user, month, year)
            
            count_weekdays = DateTimeCore.count_weekdays(year, month)
            if working_day > 0:
                count_weekdays = working_day
            insert = handle_leaves_or_overtime_works(data, count_weekdays, user, year, month)

            if insert:
                messages.success(self.request, "Data synced successfully!")
                return HttpResponseRedirect(reverse("admin:attendance_attendance_changelist"))

            messages.error(self.request, _('An error occurred while synchronizing!'))
            return HttpResponseRedirect(reverse("admin:attendance_attendance_changelist"))
        
    def form_invalid(self, form):
        
        messages.error(self.request, _('An error occurred while synchronizing!'))
        return self.render_to_response(self.get_context_data(form=form))

class AttendanceAdmin(CoreAdmin):
    list_display = ('user', 'get_date_display', 'take_leave_month','leave_taken', 'maximum_leave', 'working_days_month', 'actual_ot', 'coefficient_ot')
    search_fields = ('user__username', 'date')
    list_filter = [('user', MultipleRelatedDropdownFilter), ('date', RangeDateFilter)]

    def get_date_display(self, obj):
        if not obj.date:
            return "-"

        return obj.date.strftime('%m/%Y')
    
    get_date_display.admin_order_field = 'date'
    get_date_display.short_description = 'Date'

    actions_list = [
        "lark_synchronized_data",
    ]

    @action(description=_("Lark synchronized data"))
    def lark_synchronized_data(self, request):
        return HttpResponseRedirect(reverse('admin:sync_lark'))

    def get_urls(self):
        return super().get_urls() + [
            path(
                "sync",
                AttendanceBasedViewSync.as_view(model_admin=self),
                name="sync_lark"
            ),
        ]
    
sso_admin_site.register(Attendance, AttendanceAdmin)
