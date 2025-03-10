from django.utils.translation import gettext_lazy as _


class PositionType:
    BACKEND_SOFTWARE_ENGINEER = 'backend_software_engineer'
    FRONTEND_SOFTWARE_ENGINEER = 'frontend_software_engineer'
    FULLSTACK_SOFTWARE_ENGINEER = 'fullstack_software_engineer'
    MANUAL_QUALITY_CONTROL = 'manual_quality_control'
    AUTOMATION_QUALITY_CONTROL = 'automation_quality_control'

    CHOICE = [
        (BACKEND_SOFTWARE_ENGINEER, _('Backend Software Engineer')),
        (FRONTEND_SOFTWARE_ENGINEER, _('Frontend Software Engineer')),
        (FULLSTACK_SOFTWARE_ENGINEER, _('Fullstack Software Engineer')),
        (MANUAL_QUALITY_CONTROL, _('Manual Quality Control')),
        (AUTOMATION_QUALITY_CONTROL, _('Automation Quality Control')),
    ]


class Permission:
    CAN_CHANGE_OWN_INFO = 'change_own_info'
