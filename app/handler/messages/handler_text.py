import logging

from app.constants import TextBotMessage, MessageConstant
from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.models.telegram.tg_request_models import SendMessageModel
from app.schemas.postgresql_schemas import MessagesSchemas, UsersSchemas
from app.utils.parse_text import ParseText
from app.utils.utils import CalorieCount


class HandlerText:

    def __init__(self, tg_api_client: TelegramApi, chat_id: int, statistics_db: StatisticsDB, messages_db: MessagesDB,
                 users_db: UsersDB):
        self._client: TelegramApi = tg_api_client
        self._chat_id = chat_id
        self._statistics_db = statistics_db
        self._messages_db = messages_db
        self._users_db = users_db

    async def handler_text(self, text: str):
        """
        """
        last_message = await self._messages_db.get_last_message_by_user_id(user_id=self._chat_id)
        logging.info(f'Последнее сообщение в чате пользователя {self._chat_id} было "{last_message.text}" '
                     f'с message_id == {last_message.message_id}')
        # todo подумать насчет этого класса, потому что иногда нам надо будет парсить text, а иногда last_message.text
        parse_text = ParseText(text)
        user = await self._users_db.get_user_by_user_id(user_id=self._chat_id)
        match last_message.text:

            case TextBotMessage.SECOND_START_MSG_FOR_NEW_USER:
                value_kg = parse_text.parse_kg()
                if value_kg:
                    await self._messages_db.delete_message_by_message_id(last_message.message_id)
                    logging.info(f'Для пользователя {self._chat_id} получили значение {value_kg=}')
                    await self._users_db.update_data(data=UsersSchemas(user_id=self._chat_id,
                                                                       weight=value_kg))
                    await HandlerCommandActivityCoef(tg_api_client=self._client).send_activity_coef_message(
                        chat_id=self._chat_id, message_db=self._messages_db, is_new_user=True)
                else:
                    await self._client.send_message(
                        data=SendMessageModel(chat_id=self._chat_id, text=TextBotMessage.SECOND_START_MSG_FOR_NEW_USER)
                    )

            case TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER | TextBotMessage.ACTIVITY_COEF_MSG:

                if text.isnumeric() and (1 <= (value := int(text)) <= 5):
                    await self._messages_db.delete_all_message_user(user_id=user.user_id)
                    logging.info(f"Валидное значение коэффициента {value=}")
                    if user.activity_coef is None:
                        calorie_count = CalorieCount(weight=user.weight,
                                                     activity_coef=value).get_calorie_count()
                        await self._users_db.update_data(data=UsersSchemas(
                            user_id=user.user_id,
                            activity_coef=value,
                            calorie_count=calorie_count
                        ))
                        await self._client.send_message(data=MessageConstant(
                            user_id=user.user_id).success_registration_msg)
                    else:
                        resp = await self._client.send_message(data=MessageConstant(
                            user_id=self._chat_id, callback_data=value,
                            text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(value)
                        ).confirm_activity_coef_msg)

                        await self._messages_db.insert_message(data=MessagesSchemas(
                            user_id=user.user_id,
                            message_id=resp.message_id,
                            text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(value),
                            activity_coef=value
                        ))
                else:
                    await HandlerCommandActivityCoef(
                        tg_api_client=self._client).send_activity_coef_message(chat_id=self._chat_id,
                                                                               message_db=self._messages_db)

            case value if TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG[:-3] in value:
                if TextBotMessage.YES.lower() == text.lower():
                    logging.info("Ты написал Да, после того как получил окно про подтверждение")
                    # todo этот блок и блок в обработке кнопок можно вынести в одну функцию
                    # todo подумать насчет этого класса, потому что иногда нам надо будет парсить text,
                    #  а иногда last_message.text
                    activity_coef = ParseText(last_message.text).parse_digit()
                    calorie_count = CalorieCount(weight=user.weight,
                                                 activity_coef=activity_coef).get_calorie_count()
                    await self._users_db.update_data(data=UsersSchemas(
                        user_id=user.user_id,
                        activity_coef=activity_coef,
                        calorie_count=calorie_count
                    ))
                    await self._client.send_message(data=SendMessageModel(
                        chat_id=user.user_id,
                        text=TextBotMessage.SUCCESS_CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(calorie_count)
                    ))
                    await self._messages_db.delete_all_message_user(user_id=user.user_id)

                elif TextBotMessage.NO.lower() == text.lower():
                    logging.info("Ты написал Нет, после того как получил окно про подтверждение")
                    # todo этот блок и блок в обработке кнопок можно вынести в одну функцию
                    await self._client.send_message(data=SendMessageModel(
                        chat_id=user.user_id,
                        text=TextBotMessage.FAILED_CONFIRM_CHANGE_ACTIVITY_COEF_MSG
                    ))
                    await self._messages_db.delete_all_message_user(user_id=user.user_id)

                else:
                    logging.info(f"Ты написал {text}, после того как получил окно про подтверждение")
                    await self._client.send_message(data=MessageConstant(
                        user_id=self._chat_id, callback_data=last_message.activity_coef,
                        text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(last_message.activity_coef)
                    ).confirm_activity_coef_msg)

            case _:
                logging.error(f'Из таблицы сообщений получили текст: "{last_message.text}", '
                              f'НО никак не обработали его')
