from app.constants import TextBotMessage
from app.external_api.telegram_api import TelegramApi


class HandlerCommandStart:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int):
        self.__client: TelegramApi = tg_api_client
        self.__chat_id = chat_id

    async def send_start_message(self):
        """
        Отправка сообщения для команды /start
        """
        await self.__client.send_message(data={
            'chat_id': self.__chat_id,
            'text': '\n'.join(TextBotMessage.START_MSG)
        })
