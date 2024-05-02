import logging

from app.constants import TextBotMessage
from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.models.telegram.tg_request_models import SendMessageModel, AnswerCallbackQueryModel, EditMessageModel
from app.models.telegram.tg_response_models import CallbackQueryModel
from app.schemas.postgresql_schemas import StatisticsSchemas, UsersSchemas, MessagesSchemas
from app.utils.message_buidler import MessageBuilder
from app.utils.utils import BalanceCalorie


class HandlerEditWeight:

    def __init__(self, tg_api_client: TelegramApi,  users_db: UsersDB, statistics_db: StatisticsDB,
                 messages_db: MessagesDB):
        self._tg_api_client = tg_api_client
        self._users_db = users_db
        self._statistics_db = statistics_db
        self._messages_db = messages_db

    async def _save_weight(self, user: UsersSchemas, new_value_weight: float):
        """
        Сохраняем новое значение веса
        """
        await self._statistics_db.insert_row(data=StatisticsSchemas(
            user_id=user.user_id,
            weight=new_value_weight,
            activity_coef=user.activity_coef
        ))
        balance_calorie = BalanceCalorie(weight=new_value_weight,
                                         activity_coef=user.activity_coef).get_balance_calorie_count
        await self._users_db.update_data(data=UsersSchemas(
            user_id=user.user_id,
            weight=new_value_weight,
            balance_calorie=balance_calorie
        ))
        await self._tg_api_client.send_message(data=SendMessageModel(
            chat_id=user.user_id,
            text=TextBotMessage.SAVE_NEW_WEIGHT.format(balance_calorie)
        ))
        await self._messages_db.delete_all_message_user(user_id=user.user_id)

    async def _dont_save_weight(self, user: UsersSchemas):
        """
        Не сохраняем значение веса
        """
        await self._tg_api_client.send_message(data=SendMessageModel(
            chat_id=user.user_id,
            text=TextBotMessage.SAVE_OLD_WEIGHT.format(user.weight)
        ))
        await self._messages_db.delete_all_message_user(user_id=user.user_id)

    async def confirm_update_weight_via_text_answer(self, text_answer: str, user: UsersSchemas, value_weight: float,
                                                    message_id: int):
        """
        Обработка обновления веса через текстовые ответы
        """
        user_old_weight = user.weight
        logging.info("Зашли в функцию обновления значения кг пользователя")
        if text_answer.lower() == TextBotMessage.YES.lower():
            logging.info(f"Подтвердили что пользователь ввел 'ДА', на самом деле пользователь ввел - {text_answer}")
            await self._save_weight(user=user, new_value_weight=value_weight)

        elif text_answer.lower() == TextBotMessage.NO.lower():
            logging.info(f"Подтвердили что пользователь ввел 'НЕТ', на самом деле пользователь ввел - {text_answer}")
            await self._dont_save_weight(user=user)
        else:
            resp_confirm_edit_weight_msg = await self._tg_api_client.send_message(data=MessageBuilder(
                user_id=user.user_id,
                callback_data=value_weight,
                text=TextBotMessage.CONFIRM_RESAVE_NEW_WEIGHT.format(value_weight)).confirm_resave_new_weight)

            await self._messages_db.insert_message(data=MessagesSchemas(
                user_id=user.user_id,
                message_id=resp_confirm_edit_weight_msg.message_id,
                text=resp_confirm_edit_weight_msg.text,
                update_weight=value_weight
            ))
        await self._tg_api_client.edit_message(data=EditMessageModel(
            chat_id=user.user_id,
            text=TextBotMessage.CONFIRM_RESAVE_NEW_WEIGHT.format(user_old_weight),
            message_id=message_id
        ))

    async def handler_callback_data_edit_weight(self, callback_query: CallbackQueryModel):
        """
        Обработчик подтверждения редактирования КГ пользователя
        """
        user = await self._users_db.get_user_by_user_id(user_id=callback_query.from_user.user_id)
        if TextBotMessage.YES in callback_query.data:
            value_weight = float(callback_query.data.split('_')[-1])
            await self._save_weight(user=user, new_value_weight=value_weight)
        else:
            await self._dont_save_weight(user=user)
        await self._tg_api_client.edit_message(data=EditMessageModel(
            chat_id=user.user_id,
            text=callback_query.message.text,
            message_id=callback_query.message.message_id
        ))
        await self._tg_api_client.answer_callback_query(data=AnswerCallbackQueryModel(
            callback_query_id=callback_query.callback_query_id
        ))
