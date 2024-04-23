import logging

from app.constants import TextBotMessage, PrefixCallbackData
from app.external_api.telegram_api import TelegramApi
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram.tg_request_models import SendMessageModel


class HandlerCommandActivityCoef:

    def __init__(self, tg_api_client: TelegramApi):
        self.__client: TelegramApi = tg_api_client

    async def send_activity_coef_message(self, chat_id: int):
        """
        Отправка сообщения для команды /help
        """
        await self.__client.send_message(data=SendMessageModel(
            chat_id=chat_id,
            text='\n'.join(TextBotMessage.ACTIVITY_COEF_START_MSG),
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(text='1', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_1'),
                InlineKeyboardButtonModel(text='2', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_2'),
                InlineKeyboardButtonModel(text='3', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_3'),
                InlineKeyboardButtonModel(text='4', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_4'),
                InlineKeyboardButtonModel(text='5', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_5'),
            ])
        ))

    async def handler_callback_data(self, callback_data: str):
        """
        Если у пользователя был ранее введенный коэффициент, то выводим следующее сообщение
        ```
        Ты точно хочешь изменить свой коэффициент активности на X
        ```
        где Х - это значение выбранное пользователем. Под сообщением будет inline-клавиатура
        с двумя кнопками "Да" и "Нет", так же пользователь может текстом ввести Да/Нет(регистр букв не важен).

        4) Если пользователь нажимает/вводит "Нет", отправляем сообщение
        ```
        Хорошо, оставим все как было
        ```
        5) Если пользователь нажимает/вводит "Да", отправляем сообщение
        ```
        Твой новый коэффициент активности успешно сохранен
        И теперь твоя норма кКал составляет Х, но не забудь про дефицит -500 кКал
        ```
        где Х - это количество кКал, которое будет рассчитано как последний указанный пользователем
        вес умноженный на текущий коэффициент активности
        6) После того как мы сохранили новый коэффициент активности мы заново пересчитываем допустимую норму
        кКал в день с учетом дефицита -500кКал, чтобы при вводе потребляемых и расходуемых кКал у
        нас выводилась актуальная для пользователя информация
        """
        coef = callback_data.split('_')[-1]
        logging.info(f'Тут обработка коэфа == {coef}')


