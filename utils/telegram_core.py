
from http import HTTPStatus
from typing import Tuple

import requests

from .exception_core import ExceptionCore


class TelegramCore():

    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.__url_send_message = f'https://api.telegram.org/bot{
            token}/sendMessage'

    def send_message(self, message: str, parse_mode: str = 'Markdown') -> Tuple[bool, str]:
        params = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode  # Markdown | HTML
        }
        response = requests.get(self.__url_send_message, params=params)

        if response.status_code == HTTPStatus.OK:
            return True, response.json()['result']

        return ExceptionCore.raise_custom_exception(response.text)
