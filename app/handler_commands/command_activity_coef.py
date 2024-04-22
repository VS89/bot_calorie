from app.constants import TextBotMessage
from app.external_api.telegram_api import TelegramApi
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel


class HandlerCommandActivityCoef:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int):
        self.__client: TelegramApi = tg_api_client
        self.__chat_id = chat_id

    async def send_activity_coef_message(self):
        """
        Отправка сообщения для команды /help
        """
        await self.__client.send_message(data={
            'chat_id': self.__chat_id,
            'text': '\n'.join(TextBotMessage.ACTIVITY_COEF_START_MSG),
            "reply_markup": InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(text='1', callback_data='1'),
                InlineKeyboardButtonModel(text='2', callback_data='callback text 2'),
                InlineKeyboardButtonModel(text='3', callback_data='2'),
                InlineKeyboardButtonModel(text='4', callback_data='3'),
                InlineKeyboardButtonModel(text='5', callback_data='4'),
            ])
        })
