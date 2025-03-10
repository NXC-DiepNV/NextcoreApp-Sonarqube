from django.test import TestCase
from attendance.models import Attendance
from attendance.services import handle_leaves_or_overtime_works
from user_core.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.management import call_command
User = get_user_model()
class HandleLeavesOrOvertimeWorksTest(TestCase):
    def setUp(self):
        """ run command and create user """
        call_command('user_add_groups')
        call_command('coin_add_groups')

        for i in range(1, 5):
            user = User.objects.create_user(
                email=f'user_test_{i}@nextcore.vn',
                business_email=f'user_test_{i}@nextcore.vn',
                username=f'user_test_{i}',
                password=f'usertest{i}',
                is_staff=True,
                is_superuser=False,
                first_name="user",
                last_name="test",
            )
            user.save()

    def test_one_user_pass(self):
        """ Test one users and type on leave in June """
        data = [
            {
                "date": "20240607",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 86400,
                        "start_time": "2024-06-07 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            },
            {
                "date": "20240620",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 43200,
                        "start_time": "2024-06-20 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1']
        year, month = 2024, 6

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))

        expected_outputs = [
            "user_test_1 | 2024-06-01 | 1.5 | 12.0 | 12 | 22.0 | 0.0 | 0.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)

    def test_two_user_pass(self):
        """ Test two users and type on leave in June """
        data = [
            {
                "date": "20240607",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 86400,
                        "start_time": "2024-06-07 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            },
            {
                "date": "20240620",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 43200,
                        "start_time": "2024-06-20 08:30:00",

                    }
                ],
                "user_id": "user_test_2"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1', 'user_test_2']
        year, month = 2024, 6

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))

        expected_outputs = [
            "user_test_1 | 2024-06-01 | 1.0 | 12.0 | 12 | 22.0 | 0.0 | 0.0",
            "user_test_2 | 2024-06-01 | 0.5 | 12.0 | 12 | 22.0 | 0.0 | 0.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)
        

    def test_user_leave_without_pay_pass(self):
        """ Test leave without pay """
        data = [
            {
                "date": "20240607",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ Không Lương",
                        },
                        "interval": 86400,
                        "start_time": "2024-06-07 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            },
            {
                "date": "20240620",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 43200,
                        "start_time": "2024-06-20 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1']
        year, month = 2024, 6

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))

        expected_outputs = [
            "user_test_1 | 2024-06-01 | 1.5 | 11.0 | 12 | 21.0 | 0.0 | 0.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)


    def test_user_leave_and_overtime_pass(self):
        """ Test leave and overtime work(CN) """
        data = [
            {
                "date": "20241202",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 86400,
                        "start_time": "2024-12-02 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            },
            {
                "date": "20241222",
                "overtime_works": [
                    {
                        "duration": 7, 
                    }
                ],
                "user_id": "user_test_1"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1']
        year, month = 2024, 12

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))

        expected_outputs = [
            "user_test_1 | 2024-12-01 | 1.0 | 12.0 | 12 | 22.0 | 7.0 | 14.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)

    def test_user_leave_and_overtime_saturday_pass(self):
        """ Test leave and overtime work(T7) """
        data = [
            {
                "date": "20241202",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 86400,
                        "start_time": "2024-12-02 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            },
            {
                "date": "20241221",
                "overtime_works": [
                    {
                        "duration": 7, 
                    }
                ],
                "user_id": "user_test_1"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1']
        year, month = 2024, 12

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))

        expected_outputs = [
            "user_test_1 | 2024-12-01 | 1.0 | 12.0 | 12 | 22.0 | 7.0 | 7.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)

    def test_leave_with_a_user_not_in_the_data_pass(self):
        """ Test leave with a user not in the data """
        data = [
            {
                "date": "20241202",
                "leaves": [
                    {
                        "i18n_names": {
                            "en": "Nghỉ phép",
                        },
                        "interval": 86400,
                        "start_time": "2024-12-02 08:30:00",

                    }
                ],
                "user_id": "user_test_1"
            }
        ]

        count_weekdays = 22
        users = ['user_test_1', 'user_test_2']
        year, month = 2024, 12

        handle_leaves_or_overtime_works(data, count_weekdays, users, year, month)
        attendances_count = []
        for username in users:
            user = CustomUser.objects.filter(username=username).first()
            attendances = Attendance.objects.filter(user=user, date__year=year, date__month=month).first()
            if attendances:
                attendances_count.append(attendances)

        self.assertEqual(len(attendances_count), len(users))
        expected_outputs = [
            "user_test_1 | 2024-12-01 | 1.0 | 12.0 | 12 | 22.0 | 0.0 | 0.0",
            "user_test_2 | 2024-12-01 | 0.0 | 12.0 | 12 | 22.0 | 0.0 | 0.0"
        ]
        actual_outputs = self.actual_outputs(attendances_count)

        self.assertEqual(actual_outputs, expected_outputs)

    @staticmethod
    def actual_outputs(attendances_count: list[Attendance]) -> list[str]:
        return [
            f"{att.user.username} | {att.date} | {att.take_leave_month} | {att.leave_taken} | {att.maximum_leave} | {att.working_days_month} | {att.actual_ot} | {att.coefficient_ot}"
            for att in attendances_count
        ]
        