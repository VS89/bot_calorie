import logging

from app.constants import TextBotMessage
from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.models.telegram.tg_request_models import SendMessageModel
from app.schemas.postgresql_schemas import MessagesSchemas
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
        parse_text = ParseText(text)
        match last_message.text:
            case TextBotMessage.SECOND_START_MSG_FOR_NEW_USER:
                value_kg = parse_text.parse_kg()
                if value_kg:
                    logging.info(f'Для пользователя {self._chat_id} получили значение {value_kg=}')
                    await self._users_db.update_weight(user_id=self._chat_id, weight=value_kg)
                    await self._messages_db.delete_message_by_message_id(last_message.message_id)
                    activity_coef_msg = await HandlerCommandActivityCoef(
                        tg_api_client=self._client).send_activity_coef_message(chat_id=self._chat_id, is_new_user=True)
                    await self._messages_db.insert_message(
                        data=MessagesSchemas(
                            user_id=last_message.user_id,
                            message_id=activity_coef_msg.message_id,
                            text=activity_coef_msg.text,
                            activity_coef_flag=True
                        ))
                else:
                    await self._client.send_message(
                        data=SendMessageModel(chat_id=self._chat_id, text=TextBotMessage.SECOND_START_MSG_FOR_NEW_USER)
                    )
            case TextBotMessage.ACTIVITY_COEF_FIRST_MSG_FOR_NEW_USER:
                if text.isnumeric() and (1 <= (value := int(text)) <= 5):
                    logging.info(f"Валидное значение коэффициента {value=}")
                    await self._users_db.update_activity_coef(user_id=self._chat_id, activity_coef=value)
                    user = await self._users_db.get_user_by_user_id(user_id=self._chat_id)
                    calorie_count = CalorieCount(weight=user.weight,
                                                 activity_coef=user.activity_coef).get_calorie_count()
                    await self._users_db.update_calorie_count(user_id=user.user_id,
                                                              calorie_count=calorie_count)
                else:
                    await HandlerCommandActivityCoef(
                        tg_api_client=self._client).send_activity_coef_message(chat_id=self._chat_id)
            case _:
                logging.error(f'Из таблицы сообщений получили текст: "{last_message.text}", '
                              f'НО никак не обработали его')
