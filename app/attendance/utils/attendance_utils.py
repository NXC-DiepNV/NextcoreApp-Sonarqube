

import calendar
from datetime import datetime
from decouple import config
from typing import Any, Dict, List

from utils.lark_core import ApprovalCore

class AttendanceUtils:
    
    @staticmethod
    def check_weekday_str(year: int, month: int, day: int) -> int:
        date_obj = datetime(year, month, day).date()
        return date_obj.strftime("%a")
    
    @staticmethod
    def ot_coefficient(rank: str, ot: int) -> float:
        """
            "Mon": "Th2",
            "Tue": "Th3",
            "Wed": "Th4",
            "Thu": "Th5",
            "Fri": "Th6",
            "Sat": "Th7",
            "Sun": "CN",
        """
        if rank == 'Sun':
            return ot * 2
        if rank == 'Sat':
            return ot
        return ot * 1.5
    
    def get_attendance_user_approvals(usernames: List[str], month: int, year: int) -> Dict[str, Any]:
        """
        Get leave of month for usernames
        """
        approval_client = ApprovalCore(app_id=config('LARK_APP_ID'), app_secret=config('LARK_APP_SECRET'))
        access_token = approval_client.get_access_token()
        last_date_of_month = calendar.monthrange(
            year=year,
            month=month
        )[1]  # Get last day of month

        if month < 10:
            month = '0' + str(month)
            
        approvals_data = approval_client.get_user_attendance_approved_data(
            user_ids=usernames,
            start_date=f'{year}{month}01',
            end_date=f'{year}{month}{last_date_of_month}',
            access_token=access_token
        )
        return approvals_data
