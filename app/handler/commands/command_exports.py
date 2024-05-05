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
        """
        all_user_statistics = await self._statistics_db.get_all_statistics_by_user_id(user_id=user_id)
        if all_user_statistics:
            logging.info(f'Отправляем файл со статистикой для пользователя: {user_id}')
            user_daily_statistics = HandlerStatistics.get_daily_statistics(all_user_statistics)
            file_name = FileName(user_id=user_id).get_name_for_export_statistics()
            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                columns = ['Дата', 'Потреблено кКал', 'Израсходовано кКал', 'Баланс', 'Вес', 'Коэффициент активности']
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows([[i.date, i.sum_kc_positive, i.sum_kc_negative, i.daily_balance_calorie,
                                   i.avg_weight, i.avg_activity_coef] for i in user_daily_statistics])

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
