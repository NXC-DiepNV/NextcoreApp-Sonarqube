from .constants import Permission, TransactionStatus


def can_change_resource(request, obj, app_label):
    # Super admin can access anytime
    if request.user.is_superuser:
        return True

    # Rest user can not access if status is FAIL and SUCCESS
    if obj and obj.status in [TransactionStatus.STATUS_FAIL, TransactionStatus.STATUS_SUCCESS]:
        return False

    # Admin can change all resource
    if request.user.has_perm(f"{app_label}.{Permission.CAN_CHANGE_TRANSACTION_STATUS}"):
        return True

    # User can change own resource
    if obj and request.user.has_perm(f"{app_label}.{Permission.CAN_CHANGE_OWN_TRANSACTION}") and obj.from_user == request.user:
        return True

    return False
