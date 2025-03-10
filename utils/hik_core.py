import uuid
from http import HTTPStatus
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPDigestAuth

from .exception_core import ExceptionCore


class HikCore:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_events(self, start_time=None, end_time=None):
        if not start_time or not end_time:
            utc_now = datetime.utcnow()
            local_time = utc_now + timedelta(hours=7)
            start_time = local_time - timedelta(minutes=1)
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+07:00")
            end_time = local_time.strftime("%Y-%m-%dT%H:%M:%S+07:00")

        response = requests.post(
            url=self.url,
            auth=HTTPDigestAuth(
                username=self.username,
                password=self.password
            ),
            json={
                "AcsEventCond": {
                    "searchID": uuid.uuid4().hex,
                    "searchResultPosition": 0,
                    "maxResults": 100,
                    "major": 0,
                    "minor": 0,
                    "timeReverseOrder": True,
                    "startTime": start_time,
                    "endTime": end_time
                }
            }
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()
        raise ExceptionCore.raise_custom_exception(
            'Has error when call hik vision')
