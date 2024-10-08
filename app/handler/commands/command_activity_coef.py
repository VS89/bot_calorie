from app.utils.configuration_logger import logger

from app.constants import TextBotMessage
from app.db.messages_db import MessagesDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel, AnswerCallbackQueryModel, EditMessageModel
from app.models.telegram.tg_response_models import MessageModel, CallbackQueryModel
from app.schemas.postgresql_schemas import UsersSchemas, MessagesSchemas
from app.utils.message_buidler import MessageBuilder
from app.utils.utils import BalanceCalorie


class HandlerCommandActivityCoef:

    def __init__(self, tg_api_client: TelegramApi, message_db: MessagesDB, users_db: UsersDB):
        self._client: TelegramApi = tg_api_client
        self._message_db = message_db
        self._users_db = users_db

    async def send_activity_coef_message(self, chat_id: int, is_new_user: bool = False) -> MessageModel:
        """
        Отправка сообщения для команды /activity_coef
        """
        text = TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER if is_new_user else TextBotMessage.ACTIVITY_COEF_MSG
        resp = await self._client.send_message(data=MessageBuilder(user_id=chat_id,
                                                                   text=text).select_activity_coef_msg)
        await self._message_db.insert_message(data=MessagesSchemas(
            user_id=chat_id,
            message_id=resp.message_id,
            text=resp.text
        ))
        return resp

    async def handler_callback_data(self, callback_query: CallbackQueryModel):
        """
        Обработка нажатия кнопок для коэфа активности
        """
        await self._client.answer_callback_query(data=AnswerCallbackQueryModel(
            callback_query_id=callback_query.callback_query_id
        ))
        callback_data = callback_query.data.split('_')[-1]
        logger.info(f'Обработка callback_data == {callback_data}')
        user = await self._users_db.get_user_by_user_id(user_id=callback_query.from_user.user_id)
        if callback_data.isnumeric():
            balance_calorie = BalanceCalorie(weight=user.weight,
                                             activity_coef=int(callback_data)).get_balance_calorie_count
            if user.activity_coef is None or TextBotMessage.YES in callback_query.data:
                await self._users_db.update_data(data=UsersSchemas(
                    user_id=user.user_id,
                    activity_coef=int(callback_data),
                    balance_calorie=balance_calorie
                ))
                await self._client.send_message(data=SendMessageModel(
                    chat_id=user.user_id,
                    text=TextBotMessage.SUCCESS_REGISTRATION_MSG if user.activity_coef is None
                    else TextBotMessage.SUCCESS_CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(balance_calorie)
                ))
                await self._message_db.delete_all_message_user(user_id=user.user_id)
            else:
                resp = await self._client.send_message(data=MessageBuilder(
                    user_id=user.user_id, callback_data=callback_data).confirm_activity_coef_msg)

                await self._message_db.insert_message(data=MessagesSchemas(
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
            await self._message_db.delete_all_message_user(user_id=user.user_id)
        await self._client.edit_message(data=EditMessageModel(
            chat_id=user.user_id,
            message_id=callback_query.message.message_id,
            text=callback_query.message.text
        ))
