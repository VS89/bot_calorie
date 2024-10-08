from app.constants import TextBotMessage
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel


class HandlerCommandHelp:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int):
        self.__client: TelegramApi = tg_api_client
        self.__chat_id = chat_id

    async def send_help_message(self):
        """
        Отправка сообщения для команды /help
        """
        await self.__client.send_message(data=SendMessageModel(
            chat_id=self.__chat_id,
            text=TextBotMessage.HELP_MSG
        ))
