import logging

import httpx

from app.models.telegram.tg_request_models import SendMessageModel, GetHistoryModel, GetUpdatesModel
from app.models.telegram.tg_response_models import MessageModel


class TelegramApi:

    def __init__(self, telegram_api_token):
        self.__client = httpx.AsyncClient()
        self.__base_url = f"https://api.telegram.org/bot{telegram_api_token}"

    async def send_message(self, data: SendMessageModel) -> MessageModel:
        """
        Отправляем сообщение в чат
        """
        resp = await self.__client.post(f"{self.__base_url}/sendMessage", data=data.model_dump())
        resp_json = resp.json()
        # todo добавить обработку ошибки если не смогли отправить сообщение
        if resp_json.get('ok'):
            return MessageModel(**resp_json['result'])
        logging.error(f"Не смогли отправить сообщение в чат: {data.chat_id}")
