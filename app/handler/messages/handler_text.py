import logging

from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel


class HandlerText:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int, statistics_db: StatisticsDB, messages_db: MessagesDB):
        self._client: TelegramApi = tg_api_client
        self._chat_id = chat_id
        self._statistics_db = statistics_db
        self._messages_db = messages_db

    async def handler_text(self, message_id: int):
        """
        """
        last_message = await self._messages_db.get_last_message_by_user_id(user_id=self._chat_id)
        logging.info(f'Последнее сообщение в чате пользователя {self._chat_id} было {last_message.text} '
                     f'с message_id == {last_message.message_id}')
        if message_id > last_message.message_id:
            await self._client.send_message(data=SendMessageModel(chat_id=self._chat_id,
                                                                  text="окей, твое сообщение новое, уговорил"))
