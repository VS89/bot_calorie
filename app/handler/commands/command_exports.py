import csv
import logging
import os
import time

from app.constants import TextBotMessage
from app.db.statistics_db import StatisticsDB
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_statistics import HandlerStatistics
from app.models.telegram.tg_request_models import SendMessageModel, SendDocumentModel
from app.utils.utils import FileName


class HandlerExport:
    """
    Обработка экспорта статистики
    """

    def __init__(self, tg_api_client: TelegramApi, statistics_db: StatisticsDB):
        self._tg_api_client = tg_api_client
        self._statistics_db = statistics_db

    async def handler_export_command(self, user_id: int):
        """
        Создание и отправка csv файла со всей статистикой
        Отправляем файл в сообщении, в котором будет статистика за все время ведения бота
- Дата - в формате ДД.ММ.ГГГГ
- Потреблено кКал
- Израсходовано кКал
- Баланс
- Вес
- Коэффициент активности
        """
        all_user_statistics = await self._statistics_db.get_all_statistics_by_user_id(user_id=user_id)
        if all_user_statistics:
            logging.info(f'Отправляем файл со статистикой для пользователя: {user_id}')
            user_daily_statistics = HandlerStatistics.get_daily_statistics(all_user_statistics)
            user_daily_statistic_convert_to_list_dict = [i.model_dump() for i in user_daily_statistics]
            file_name = FileName(user_id=user_id).get_name_for_export_statistics()
            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                # todo разобраться как сделать поля как в тз
                # columns = ['Дата', 'Потреблено кКал', 'Израсходовано кКал', 'Баланс', 'Вес', 'Коэффициент активности']
                columns = ['date', 'sum_kc_positive', 'sum_kc_negative', 'daily_balance_calorie',
                           'avg_weight', 'avg_activity_coef']
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                writer.writerows(user_daily_statistic_convert_to_list_dict)
            for i in range(15):
                if os.stat(file_name):
                    await self._tg_api_client.send_document(data=SendDocumentModel(
                        chat_id=user_id,
                        document_path=file_name,
                        document_name=file_name.split('/')[-1],
                        caption='Твоя полная статистка'
                    ))
                    return
                time.sleep(1)
            logging.error(f"В течение 15 секунд не дождались создание файла с полной статистикой "
                          f"для пользователя: {user_id}")
        await self._tg_api_client.send_message(data=SendMessageModel(
            chat_id=user_id,
            text=TextBotMessage.STATISTICS_NOT_FOUND
        ))
