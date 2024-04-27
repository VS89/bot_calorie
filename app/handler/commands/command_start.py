import datetime

from pytz import timezone

from app.constants import TextBotMessage
from app.db.messages_db import MessagesDB

from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel
from app.schemas.postgresql_schemas import MessagesSchemas, UsersSchemas


class HandlerCommandStart:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int, messages_db: MessagesDB,
                 users_db: UsersDB):
        self._client: TelegramApi = tg_api_client
        self._chat_id = chat_id
        self._messages_db = messages_db
        self._users_db = users_db

    async def _send_start_message(self):
        """
        Отправка сообщения для команды /start
        """
        await self._client.send_message(data=SendMessageModel(
            chat_id=self._chat_id,
            text=TextBotMessage.START_MSG
        ))

    async def _send_second_message_after_first_start(self):
        """
        Отправляем второе сообщение при регистрации нового пользователя
        Если пользователя нет в нашей базе, то:
            - Добавляем его в базу
            - Отправляем второе приветственное сообщение
            - Сохраняем в базу сообщение, которое только что отправили
        """
        user = await self._users_db.get_user_by_user_id(self._chat_id)
        if user is None:
            await self._users_db.insert_user(data=UsersSchemas(
                user_id=self._chat_id,
                date_update_data=datetime.datetime.now(tz=timezone('Europe/Moscow'))
            ))
            resp = await self._client.send_message(data=SendMessageModel(
                chat_id=self._chat_id,
                text=TextBotMessage.SECOND_START_MSG_FOR_NEW_USER
            ))
            await self._messages_db.insert_message(data=MessagesSchemas(
                user_id=self._chat_id,
                message_id=resp.message_id,
                text=resp.text
            ))

    async def handler_start_command(self):
        await self._send_start_message()
        await self._send_second_message_after_first_start()

