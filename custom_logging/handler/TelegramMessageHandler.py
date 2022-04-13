from requests import get
import logging


class TelegramMessageHandler(logging.StreamHandler):

    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot_token = bot_token,
        self.chat_id = chat_id

    def emit(self, record):
        msg = self.format(record)
        response = get(f'https://api.telegram.org/bot{self.bot_token[0]}/sendMessage?chat_id={self.chat_id}&text={msg}')
