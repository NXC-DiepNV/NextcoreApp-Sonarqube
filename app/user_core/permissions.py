from user_core.constants import Permission


def is_can_view_full(request, obj):
    if request.user.is_superuser:
        return True
    if request.user == obj:
        return True
    return False


def can_change_resource(request, obj, app_label):
    # Super admin can access anytime
    if request.user.is_superuser:
        return True

    # User can change own resource
    if obj and request.user.has_perm(f"{app_label}.{Permission.CAN_CHANGE_OWN_INFO}") and obj == request.user:
        return True

    return False
