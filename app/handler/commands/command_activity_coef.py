import logging

from app.constants import TextBotMessage, MessageConstant
from app.db.messages_db import MessagesDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel, AnswerCallbackQueryModel
from app.models.telegram.tg_response_models import MessageModel, CallbackQueryModel
from app.schemas.postgresql_schemas import UsersSchemas, MessagesSchemas
from app.utils.utils import CalorieCount


class HandlerCommandActivityCoef:

    def __init__(self, tg_api_client: TelegramApi):
        self._client: TelegramApi = tg_api_client

    async def send_activity_coef_message(self, chat_id: int, message_db: MessagesDB,
                                         is_new_user: bool = False) -> MessageModel:
        """
        Отправка сообщения для команды /help
        """
        text = TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER if is_new_user else TextBotMessage.ACTIVITY_COEF_MSG
        resp = await self._client.send_message(data=MessageConstant(user_id=chat_id,
                                                                    text=text).select_activity_coef_msg)
        await message_db.insert_message(data=MessagesSchemas(
            user_id=chat_id,
            message_id=resp.message_id,
            text=resp.text
        ))
        return resp

    async def handler_callback_data(self, callback_query: CallbackQueryModel, users_db: UsersDB,
                                    message_db: MessagesDB):
        """
        Обработка нажатия кнопок для коэфа активности
        """
        callback_data = callback_query.data.split('_')[-1]
        logging.info(f'Обработка callback_data == {callback_data}')
        user = await users_db.get_user_by_user_id(user_id=callback_query.from_user.user_id)
        if callback_data.isnumeric():
            calorie_count = CalorieCount(weight=user.weight,
                                         activity_coef=int(callback_data)).get_calorie_count()
            if user.activity_coef is None:
                await users_db.update_data(data=UsersSchemas(
                    user_id=user.user_id,
                    activity_coef=int(callback_data),
                    calorie_count=calorie_count
                ))
                await self._client.send_message(data=SendMessageModel(
                    chat_id=user.user_id,
                    text=TextBotMessage.SUCCESS_REGISTRATION_MSG
                ))
                await message_db.delete_all_message_user(user_id=user.user_id)
            elif TextBotMessage.YES in callback_query.data:
                await users_db.update_data(data=UsersSchemas(
                    user_id=user.user_id,
                    activity_coef=int(callback_data),
                    calorie_count=calorie_count
                ))
                await self._client.send_message(data=SendMessageModel(
                    chat_id=user.user_id,
                    text=TextBotMessage.SUCCESS_CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(calorie_count)
                ))
                await message_db.delete_all_message_user(user_id=user.user_id)
            else:
                # todo поменять это сообщение на отправку answer callback query, чтобы кнопка долго не горела
                resp = await self._client.send_message(data=MessageConstant(
                    user_id=user.user_id, callback_data=callback_data).confirm_activity_coef_msg)

                await message_db.insert_message(data=MessagesSchemas(
                    user_id=user.user_id,
                    message_id=resp.message_id,
                    text=resp.text,
                    activity_coef=int(callback_data)
                ))
        else:
            await self._client.send_message(data=SendMessageModel(
                chat_id=user.user_id,
                text=TextBotMessage.FAILED_CONFIRM_CHANGE_ACTIVITY_COEF_MSG
            ))
            await message_db.delete_all_message_user(user_id=user.user_id)
        await self._client.answer_callback_query(data=AnswerCallbackQueryModel(
            callback_query_id=callback_query.callback_query_id
        ))
