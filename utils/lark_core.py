import json
from typing import Optional, List, Dict, Any
from http import HTTPStatus

import requests

from .exception_core import ExceptionCore


class LarkCore:

    def __init__(self, app_id: str, app_secret: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.larksuite.com/open-apis"
        self.access_token: Optional[str] = None

    def get_user_info_from_code(self, code: str) -> Optional[str]:
        url = f"{self.base_url}/authen/v1/access_token"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "grant_type": "authorization_code",
            "code": code,
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("data", {})

    def get_access_token(self) -> Optional[str]:
        """Get the access token using the app_id and app_secret."""
        url = f"{self.base_url}/auth/v3/app_access_token/internal/"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == HTTPStatus.OK:
            self.access_token = response.json().get("app_access_token")
            return self.access_token
        else:
            raise ExceptionCore.raise_custom_exception(
                f"Failed to get access token: {response.text}")

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get user information using their user ID."""
        if not self.access_token:
            self.get_access_token()

        url = f"{self.base_url}/user/v1/get/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "user_id": user_id
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")

    def send_message(self, chat_id: str, content: str) -> Dict[str, Any]:
        """Send a message to a chat."""
        if not self.access_token:
            self.get_access_token()

        url = f"{self.base_url}/message/v4/send/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "chat_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise Exception(f"Failed to send message: {response.text}")

    def create_chat(self, chat_name: str, user_ids: List[str]) -> Dict[str, Any]:
        """Create a chat group."""
        if not self.access_token:
            self.get_access_token()

        url = f"{self.base_url}/chat/v3/create/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": chat_name,
            "user_ids": user_ids
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise Exception(f"Failed to create chat: {response.text}")

    def bot_send_message(self, bot_webhook_id, content):
        url = f"{self.base_url}/bot/v2/hook/{bot_webhook_id}"
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise Exception(f"Failed to create chat: {response.text}")

    def get_login_url(self, redirect_uri: str) -> str:
        return f"{self.base_url}/authen/v1/authorize?app_id={self.app_id}&redirect_uri={redirect_uri}&response_type=code"


class ApprovalCore(LarkCore):
    def __init__(self, app_id: str, app_secret: str):
        super().__init__(app_id, app_secret)

    def get_user_attendance_approved_data(self, user_ids: List[str], start_date: str, end_date: str, access_token: str = None) -> Dict[str, Any]:
        url = f"{self.base_url}/attendance/v1/user_approvals/query?employee_type=employee_id"
        data = {
            "user_ids": user_ids,
            "check_date_from": start_date,
            "check_date_to": end_date
        }

        token = access_token if access_token is not None else self.access_token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            headers=headers,
            json=data
        )
        if response.status_code == HTTPStatus.OK:
            return response.json()["data"]["user_approvals"]
        else:
            return ExceptionCore.raise_custom_exception(f"Failed to create chat: {response.text}")

    def get_leaves(self, employee_ids: List[str], approval_datas):
        approval_dict = {item: set() for item in employee_ids}
        interval_dict = {item: 0 for item in employee_ids}
        for approval_data in approval_datas:
            if "leaves" not in approval_data:
                continue
            approval_id = approval_data["leaves"][0]["approval_id"]
            interval = approval_data["leaves"][0]["interval"]
            user_id = approval_data["user_id"]

            if approval_id not in approval_dict[user_id]:
                interval_dict[user_id] += interval / 86400
                approval_dict[user_id].add(approval_id)
        return interval_dict
