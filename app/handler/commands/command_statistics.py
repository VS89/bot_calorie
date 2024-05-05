import logging

from app.constants import TextBotMessage, LimitValues
from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB
from app.db.users_db import UsersDB
from app.external_api.telegram_api import TelegramApi
from app.models.daily_statistics_model import DailyStatisticsModel
from app.models.telegram.tg_request_models import SendMessageModel, EditMessageModel, SendPhotoModel, \
    AnswerCallbackQueryModel
from app.models.telegram.tg_response_models import MessageModel, CallbackQueryModel
from app.schemas.postgresql_schemas import MessagesSchemas, StatisticsSchemas
from app.utils.create_chart import create_chart_png
from app.utils.message_buidler import MessageBuilder


class HandlerStatistics:

    def __init__(self, tg_api_client: TelegramApi, messages_db: MessagesDB, users_db: UsersDB,
                 statistics_db: StatisticsDB):
        self._tg_api_client = tg_api_client
        self._messages_db = messages_db
        self._users_db = users_db
        self._statistics_db = statistics_db

    @staticmethod
    def get_daily_statistics(statistics: list[StatisticsSchemas]) -> list[DailyStatisticsModel]:
        """
        Рассчитываем статистику за каждый день
        """
        date_format = '%d.%m.%Y'
        dict_statistics = {}
        for statistic in statistics:
            date_stat = statistic.save_date.strftime(date_format)
            if dict_statistics.get(date_stat):
                dict_statistics[date_stat].append(statistic)
            else:
                dict_statistics[date_stat] = [statistic]
        daily_statistics: list[DailyStatisticsModel] | list = []
        for date in dict_statistics.keys():
            sum_kc_positive = 0
            sum_kc_negative = 0
            sum_balance_calorie = 0
            sum_weight = 0
            sum_activity_coef = 0
            for value in dict_statistics[date]:
                if value.kcal is not None:
                    if value.kcal > 0:
                        sum_kc_positive += value.kcal
                    else:
                        sum_kc_negative += abs(value.kcal)
                sum_weight += value.weight
                sum_balance_calorie += value.balance_calorie
                sum_activity_coef += value.activity_coef
            len_value_statistics = len(dict_statistics[date])
            avg_weight = round((sum_weight / len_value_statistics), 1)
            avg_balance_calorie = sum_balance_calorie / len_value_statistics
            avg_activity_coef = round(sum_activity_coef / len_value_statistics)
            daily_balance_calorie = int(avg_balance_calorie - sum_kc_positive + sum_kc_negative)
            daily_statistics.append(DailyStatisticsModel(
                date=date,
                avg_weight=avg_weight,
                sum_kc_positive=sum_kc_positive,
                sum_kc_negative=sum_kc_negative,
                daily_balance_calorie=daily_balance_calorie,
                avg_activity_coef=avg_activity_coef
            ))
        return daily_statistics

    async def send_statistics_message(self, user_id: int) -> MessageModel:
        """
        Отправка сообщения после ввода команды /statistics
        """
        resp = await self._tg_api_client.send_message(data=MessageBuilder(user_id=user_id).select_period_statistics)
        await self._messages_db.insert_message(data=MessagesSchemas(
            user_id=user_id,
            message_id=resp.message_id,
            text=resp.text
        ))
        return resp

    async def handler_text_message_select_period_statistics(self, user_id: int, text: str,
                                                            last_message: MessagesSchemas):
        """
        Обработка текстового ответа на сообщение про выбор периода статистики
        """
        if text.isnumeric() and (int(text) == LimitValues.STATISTIC_10_DAY or
                                 int(text) == LimitValues.STATISTIC_30_DAY):
            statistics = await self._statistics_db.get_statistics_by_days(count_days=int(text) - 1, user_id=user_id)
            daily_statistics = self.get_daily_statistics(statistics=statistics)
            chart_path = create_chart_png(daily_statistics=daily_statistics, user_id=user_id)
            await self._tg_api_client.send_message(data=MessageBuilder(
                user_id=user_id).statistics_message_by_period(daily_statistics))
            await self._tg_api_client.send_photo(data=SendPhotoModel(
                chat_id=user_id,
                photo_path=chart_path,
                caption=TextBotMessage.CAPTION_CHART_STATISTIC_WEIGHT.format(text)
            ))
            await self._messages_db.delete_all_message_user(user_id=user_id)
        else:
            await self.send_statistics_message(user_id=user_id)
        await self._tg_api_client.edit_message(data=EditMessageModel(
            chat_id=user_id,
            message_id=last_message.message_id,
            text=last_message.text
        ))

    async def handler_callback_data(self, callback_query: CallbackQueryModel):
        """
        Обработка нажатия кнопок для получения статистики
        """
        await self._tg_api_client.answer_callback_query(data=AnswerCallbackQueryModel(
            callback_query_id=callback_query.callback_query_id
        ))
        callback_data = callback_query.data.split('_')[-1]
        logging.info(f'Обработка callback_data == {callback_data} для статистики')
        user = await self._users_db.get_user_by_user_id(user_id=callback_query.from_user.user_id)
        statistics = await self._statistics_db.get_statistics_by_days(count_days=int(callback_data) - 1,
                                                                      user_id=callback_query.from_user.user_id)
        if statistics:
            logging.info(f"Для пользователя {user.user_id}. Статистика == {statistics}")
            daily_statistics = self.get_daily_statistics(statistics=statistics)
            chart_path = create_chart_png(daily_statistics=daily_statistics, user_id=user.user_id)
            await self._tg_api_client.send_message(data=MessageBuilder(
                user_id=callback_query.from_user.user_id).statistics_message_by_period(daily_statistics))
            await self._tg_api_client.send_photo(data=SendPhotoModel(
                chat_id=callback_query.from_user.user_id,
                photo_path=chart_path,
                caption=TextBotMessage.CAPTION_CHART_STATISTIC_WEIGHT.format(callback_data)
            ))
            await self._tg_api_client.edit_message(data=EditMessageModel(
                chat_id=callback_query.from_user.user_id,
                message_id=callback_query.message.message_id,
                text=callback_query.message.text
            ))
            await self._messages_db.delete_all_message_user(user_id=callback_query.from_user.user_id)
            return
        logging.info(f"Не смогли найти статистику для пользователя {user.user_id}")
        await self._tg_api_client.send_message(data=SendMessageModel(chat_id=user.user_id,
                                                                     text=TextBotMessage.STATISTICS_NOT_FOUND))
