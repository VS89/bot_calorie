import logging

from app.constants import TextBotMessage, PrefixCallbackData
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram.tg_request_models import SendMessageModel, EditMessageModel, AnswerCallbackQueryModel
from app.models.telegram.tg_response_models import MessageModel, CallbackQueryModel
from app.utils.utils import CalorieCount


class HandlerCommandActivityCoef:

    def __init__(self, tg_api_client: TelegramApi):
        self._client: TelegramApi = tg_api_client

    async def send_activity_coef_message(self, chat_id: int, is_new_user: bool = False) -> MessageModel:
        """
        Отправка сообщения для команды /help
        """
        text = TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER if is_new_user else TextBotMessage.ACTIVITY_COEF_MSG
        return await self._client.send_message(data=SendMessageModel(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(text='1', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_1'),
                InlineKeyboardButtonModel(text='2', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_2'),
                InlineKeyboardButtonModel(text='3', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_3'),
                InlineKeyboardButtonModel(text='4', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_4'),
                InlineKeyboardButtonModel(text='5', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_5'),
            ])
        ))

    async def handler_callback_data(self, callback_query: CallbackQueryModel, users_db: UsersDB):
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
        is_send_success_registration_msg = False
        activity_coef = int(callback_query.data.split('_')[-1])
        logging.info(f'Тут обработка коэфа == {activity_coef}')
        user = await users_db.get_user_by_user_id(user_id=callback_query.from_user.user_id)
        if user.activity_coef is None:
            is_send_success_registration_msg = True
        # todo этот кусочек с апдейтом можно вынести в отдельную функцию и возможно переименовать handler command ....
        #  просто в handler и к какой тематике он относиться, чтобы там содержались нужные для этого функции
        await users_db.update_activity_coef(user_id=callback_query.from_user.user_id, activity_coef=activity_coef)
        calorie_count = CalorieCount(weight=user.weight,
                                     activity_coef=activity_coef).get_calorie_count()
        await users_db.update_calorie_count(user_id=user.user_id, calorie_count=calorie_count)
        # todo отвечать на колбек надо, чтобы не горела кнопка все время
        await self._client.answer_callback_query(data=AnswerCallbackQueryModel(
            callback_query_id=callback_query.callback_query_id
        ))
        if is_send_success_registration_msg:
            await self._client.send_message(data=SendMessageModel(
                chat_id=callback_query.from_user.user_id,
                text=TextBotMessage.SUCCESS_REGISTRATION_MSG
            ))
