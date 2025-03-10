import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .exception_core import ExceptionCore

WEEKEND_DAY_COUNT = 1
FIRST_DAY = 1
SATURDAY = 5
SUNDAY = 6  
class DateTimeCore:
    @staticmethod
    def get_date_text(year: int, month: int, day: int, format_text: str = '%Y/%m%d') -> str:
        try:
            custom_date = datetime(year, month, day)
            return DateTimeCore.format_date(custom_date, format_text)
        except Exception as e:
            return ExceptionCore.raise_custom_exception(repr(e))

    @staticmethod
    def format_date(custom_date: datetime, format_text: str = '%Y/%m/%d') -> str:
        return custom_date.strftime(format_text)

    @staticmethod
    def convert_str_to_date(text: str, format_text: str = '%Y/%m/%d') -> datetime:
        try:
            return datetime.strptime(text, format_text)
        except Exception as e:
            return ExceptionCore.raise_custom_exception(repr(e))

    @staticmethod
    def add_month(year: int, month: int, month_add: int) -> datetime:
        given_date = datetime(year, month, 1)
        target_date = given_date + relativedelta(months=month_add)
        return target_date
    
    @staticmethod
    def count_weekends(year: int, month: int) -> int:
        """Calculate the total number of Saturdays and Sundays in the month."""
        
        total_days_in_month = calendar.monthrange(year, month)[1]

        all_days = range(FIRST_DAY, total_days_in_month + 1)

        weekend_days = [day for day in all_days 
                        if calendar.weekday(year, month, day) in {SATURDAY, SUNDAY}]

        total_weekends = sum(WEEKEND_DAY_COUNT for _ in weekend_days)

        return total_weekends
    
    @staticmethod
    def count_weekdays(year: int, month: int) -> int:
        """Calculate the total number of days in the month minus the number of weekends."""
        total_days = calendar.monthrange(year, month)[1]
        return total_days - DateTimeCore.count_weekends(year, month)
