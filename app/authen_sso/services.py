from decouple import config

from .constants import LARK_LOGIN_CALLBACK_URI
from utils.lark_core import LarkCore

# Init when service is imported (avoid multiple init in methods)
lark_core = LarkCore(config('LARK_APP_ID'), config('LARK_APP_SECRET'))


def lark_get_lark_login_url():
    """
    Get URL login in Lark
    """
    return lark_core.get_login_url(
        config('BASE_URL') + LARK_LOGIN_CALLBACK_URI,
    )


def exchange_code_for_user_info(code):
    """
    Get user info from code
    """
    return lark_core.get_user_info_from_code(code)
