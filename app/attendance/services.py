from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

from attendance.constants import MAX_LEAVE, ON_LEAVE, ONE_DAY
from attendance.models import Attendance
from attendance.utils.attendance_utils import AttendanceUtils
from user_core.models import CustomUser


def extract_year_month(date: str) -> tuple[int, int, int]:
    """Convert date to year, month, day"""
    date_str = str(date)
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError:
        raise ValueError("Date conversion fails.")

def get_last_month_leave(user: CustomUser, year: int, month: int) -> tuple[int] | None:
    """Get take_leave_month and leave_taken from the previous month"""
    if month == 1:
        return None  
    
    prev_month = month - 1
    attendance_last_month = Attendance.objects.filter(
        user=user,
        date__year=year,
        date__month=prev_month
    ).first()

    leave_taken = getattr(attendance_last_month, "leave_taken", 0)

    return leave_taken

def handle_leaves_or_overtime_works(data: Dict[str, Any], count_weekdays: int, users: list[str], year: int, month: int) -> bool:
    """Processing leave day calculations"""
    try:
        
        start_time = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")

        result = defaultdict(lambda: {
            "date": start_time, 
            "take_leave_month": 0, 
            "leave_taken": float(MAX_LEAVE), 
            "working_days_month": float(count_weekdays),
            "actual_ot": 0,
            "coefficient_ot": 0
        })

        for user in users:
            result[user]

            user_check = CustomUser.objects.filter(username=user).first()
            leave_taken_last_month = get_last_month_leave(user_check, year, month)
            if leave_taken_last_month :
                result[user]["leave_taken"] = float(leave_taken_last_month)
        
        for entry in data:
            user_id = entry["user_id"]
            date = entry["date"]
            result[user_id]["date"] = start_time
            if "leaves" in entry:
                for leave in entry["leaves"]:
                    take_leave_month_day = float(leave["interval"] / ONE_DAY)
                    result[user_id]["take_leave_month"] += take_leave_month_day
                    leave_name = leave.get("i18n_names", {}).get("en", "")
                    if leave_name != ON_LEAVE:
                        result[user_id]["working_days_month"] -= take_leave_month_day
                        result[user_id]["leave_taken"] -= float(take_leave_month_day)

            if "overtime_works" in entry:            
                year, month, day = extract_year_month(date)
                check_weekday = AttendanceUtils.check_weekday_str(year, month, day)
                for overtime_work in entry["overtime_works"]:
                    result[user_id]["actual_ot"] += overtime_work['duration']
                    coefficient_ot = AttendanceUtils.ot_coefficient(check_weekday, overtime_work['duration'])
                    result[user_id]["coefficient_ot"] += float(coefficient_ot)  

        for user, values in result.items():
            user_obj = CustomUser.objects.filter(username=user).first()
            if user_obj:
                Attendance.objects.update_or_create(
                    user=user_obj,
                    date=values["date"],
                    defaults={
                        "take_leave_month": values["take_leave_month"],
                        "leave_taken": values["leave_taken"],
                        "working_days_month": values['working_days_month'],
                        "maximum_leave": float(MAX_LEAVE),
                        "actual_ot": values["actual_ot"],
                        "coefficient_ot": values["coefficient_ot"],
                    },
                )

        return True        
    except Exception:
        return False            
