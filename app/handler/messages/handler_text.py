import logging

from app.constants import TextBotMessage, LimitValues, PrefixCallbackData
from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.handlers_model import HandlersModel
from app.models.telegram.tg_request_models import SendMessageModel, EditMessageModel
from app.schemas.postgresql_schemas import MessagesSchemas, UsersSchemas, StatisticsSchemas
from app.utils.message_buidler import MessageBuilder
from app.utils.parse_text import ParseText
from app.utils.utils import BalanceCalorie


class HandlerText:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int, statistics_db: StatisticsDB, messages_db: MessagesDB,
                 users_db: UsersDB, handlers: HandlersModel):
        self._client: TelegramApi = tg_api_client
        self._chat_id = chat_id
        self._statistics_db = statistics_db
        self._messages_db = messages_db
        self._users_db = users_db
        self._handlers = handlers

    async def _second_step_registration_user(self, value_kg: float | None):
        """
        Второй шаг регистрации пользователя, добавление КГ
        """
        if value_kg:
            await self._messages_db.delete_all_message_user(user_id=self._chat_id)
            logging.info(f'Для пользователя {self._chat_id} получили значение {value_kg=}')
            await self._users_db.update_data(data=UsersSchemas(user_id=self._chat_id,
                                                               weight=value_kg))
            await self._handlers.handler_activity_coef.send_activity_coef_message(chat_id=self._chat_id,
                                                                                  is_new_user=True)
        else:
            await self._client.send_message(
                data=SendMessageModel(chat_id=self._chat_id, text=TextBotMessage.SECOND_START_MSG_FOR_NEW_USER)
            )

    async def _handler_activity_coef(self, user: UsersSchemas, text: str, last_message: MessagesSchemas):
        """
        Обработка добавления коэффициента активности
        """

        if text.isnumeric() and (1 <= (value := int(text)) <= 5):
            await self._messages_db.delete_all_message_user(user_id=user.user_id)
            logging.info(f"Валидное значение коэффициента {value=}")
            if user.activity_coef is None:
                balance_calorie = BalanceCalorie(weight=user.weight,
                                                 activity_coef=value).get_balance_calorie_count
                await self._users_db.update_data(data=UsersSchemas(
                    user_id=user.user_id,
                    activity_coef=value,
                    balance_calorie=balance_calorie
                ))
                await self._client.send_message(data=MessageBuilder(
                    user_id=user.user_id).success_registration_msg)
            else:
                resp_activity_coef_msg = await self._client.send_message(data=MessageBuilder(
                    user_id=self._chat_id, callback_data=value,
                    text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(value)).confirm_activity_coef_msg)

                await self._messages_db.insert_message(data=MessagesSchemas(
                    user_id=user.user_id,
                    message_id=resp_activity_coef_msg.message_id,
                    text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(value),
                    activity_coef=value
                ))
        else:
            await self._handlers.handler_activity_coef.send_activity_coef_message(chat_id=self._chat_id)
        await self._client.edit_message(data=EditMessageModel(
            chat_id=user.user_id,
            message_id=last_message.message_id,
            text=last_message.text
        ))

    async def _confirm_change_activity_coef(self, user: UsersSchemas, text: str, last_message: MessagesSchemas):
        if TextBotMessage.YES.lower() == text.lower():
            logging.info("Ты написал Да, после того как получил окно про подтверждение")
            activity_coef = ParseText(last_message.text).parse_digit()
            balance_calorie = BalanceCalorie(weight=user.weight,
                                             activity_coef=activity_coef).get_balance_calorie_count
            await self._users_db.update_data(data=UsersSchemas(
                user_id=user.user_id,
                activity_coef=activity_coef,
                balance_calorie=balance_calorie
            ))
            await self._client.send_message(data=SendMessageModel(
                chat_id=user.user_id,
                text=TextBotMessage.SUCCESS_CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(balance_calorie)
            ))
            await self._messages_db.delete_all_message_user(user_id=user.user_id)

        elif TextBotMessage.NO.lower() == text.lower():
            logging.info("Ты написал Нет, после того как получил окно про подтверждение")
            await self._client.send_message(data=SendMessageModel(
                chat_id=user.user_id,
                text=TextBotMessage.FAILED_CONFIRM_CHANGE_ACTIVITY_COEF_MSG
            ))
            await self._messages_db.delete_all_message_user(user_id=user.user_id)

        else:
            logging.info(f"Ты написал {text}, после того как получил окно про подтверждение")
            resp_repeat_msg = await self._client.send_message(data=MessageBuilder(
                user_id=self._chat_id, callback_data=last_message.activity_coef,
                text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(last_message.activity_coef)
            ).confirm_activity_coef_msg)
            await self._messages_db.insert_message(data=MessagesSchemas(
                user_id=user.user_id,
                message_id=resp_repeat_msg.message_id,
                text=resp_repeat_msg.text,
                activity_coef=last_message.activity_coef
            ))
        await self._client.edit_message(data=EditMessageModel(
            chat_id=user.user_id,
            message_id=last_message.message_id,
            text=last_message.text
        ))

    async def _added_kc(self, value_kc: int, user: UsersSchemas):
        """
        Добавление килокалорий
        """
        await self._statistics_db.insert_row(data=StatisticsSchemas(
            user_id=user.user_id,
            weight=user.weight,
            activity_coef=user.activity_coef,
            kcal=value_kc,
            balance_calorie=user.balance_calorie
        ))
        kcal_sum = await self._statistics_db.get_sum_kcal_for_current_date(user_id=user.user_id)
        logging.info(f"Для пользователя {user.user_id} текущий баланс ккал == {kcal_sum}")
        kcal_balance = user.balance_calorie - kcal_sum - LimitValues.CALORIE_DEFICIT
        send_msg_model = MessageBuilder(user_id=user.user_id).calorie_balance_message(kcal_balance)
        await self._client.send_message(data=send_msg_model)

    async def handler_text(self, text: str):
        """
        Обработчик текста
        """
        if text is None:
            await self._client.send_message(data=SendMessageModel(
                chat_id=self._chat_id,
                text=TextBotMessage.CAN_HANDLER_ONLY_TEXT
            ))
            return
        parse_text = ParseText(text)
        user = await self._users_db.get_user_by_user_id(user_id=self._chat_id)
        last_message = await self._messages_db.get_last_message_by_user_id(user_id=self._chat_id)
        if last_message is not None:
            logging.info(f'Последнее сообщение в чате пользователя {self._chat_id} было "{last_message.text}" '
                         f'с message_id == {last_message.message_id}')
            match last_message.text:

                case TextBotMessage.SECOND_START_MSG_FOR_NEW_USER:
                    value_weight = parse_text.parse_weight()
                    await self._second_step_registration_user(value_weight)
                    return

                case TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER | TextBotMessage.ACTIVITY_COEF_MSG:
                    await self._handler_activity_coef(user=user, text=text, last_message=last_message)
                    return

                case value if TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG[:-3] in value:
                    await self._confirm_change_activity_coef(user=user, text=text, last_message=last_message)
                    return

                case TextBotMessage.SELECT_PERIOD_STATISTICS:
                    await self._handlers.handler_statistics.handler_text_message_select_period_statistics(
                        user_id=user.user_id,
                        text=text,
                        last_message=last_message
                    )
                    return

                case _:
                    logging.error(f'Из таблицы сообщений получили текст: "{last_message.text}", '
                                  f'НО никак не обработали его')

            if last_message.update_weight:
                await self._handlers.handler_edit_weight.confirm_update_weight_via_text_answer(
                    text_answer=text,
                    user=user,
                    value_weight=last_message.update_weight,
                    message_id=last_message.message_id
                )

        if user is not None:
            if value_kc := parse_text.parse_kcal():
                logging.info(f"Распарсили кол-во ккал == {value_kc}")
                await self._added_kc(value_kc=value_kc, user=user)
                return
            if value_weight := parse_text.parse_weight():
                logging.info(f"Распарсили кол-во kg == {value_weight}")
                count_uniq_weight = await self._statistics_db.get_count_uniq_weight_by_user_id_today(
                    user_id=user.user_id)
                logging.info(f"Для пользователя {user.user_id=}, {count_uniq_weight=}")
                if count_uniq_weight > 1:
                    logging.info(f"у юзера больше одного уникального веса")
                    resp_last_row_statistics = await self._statistics_db.get_last_row_by_user_id(user_id=user.user_id)
                    resp_confirm_edit_weight_msg = await self._client.send_message(data=MessageBuilder(
                        user_id=user.user_id,
                        callback_data=value_weight,
                        text=TextBotMessage.CONFIRM_RESAVE_NEW_WEIGHT.format(
                            resp_last_row_statistics.weight)).confirm_resave_new_weight)

                    await self._messages_db.insert_message(data=MessagesSchemas(
                        user_id=user.user_id,
                        message_id=resp_confirm_edit_weight_msg.message_id,
                        text=resp_confirm_edit_weight_msg.text,
                        update_weight=value_weight
                    ))
                    return
                balance_calorie = BalanceCalorie(weight=value_weight,
                                                 activity_coef=user.activity_coef).get_balance_calorie_count
                await self._users_db.update_data(data=UsersSchemas(
                    user_id=user.user_id,
                    weight=value_weight,
                    balance_calorie=balance_calorie
                ))
                await self._statistics_db.insert_row(data=StatisticsSchemas(
                    user_id=user.user_id,
                    weight=value_weight,
                    activity_coef=user.activity_coef,
                    balance_calorie=balance_calorie
                ))

                await self._client.send_message(
                    data=MessageBuilder(user_id=user.user_id, text=str(balance_calorie)).save_new_weight)
                return
