import logging
import os
import time

import matplotlib.pyplot as plt

from app.models.daily_statistics_model import DailyStatisticsModel
from app.utils.utils import FileName


def create_chart_png(daily_statistics: list[DailyStatisticsModel], user_id: int) -> str | None:
    """
    Создаем график с разрешением .png и возвращаем байты для отправки картинки
    """
    x = [i.date for i in daily_statistics]
    y = [float(f'{i.avg_weight:.1f}') for i in daily_statistics]
    lower_range_y = int(min(y) - 1)
    upper_range_y = int(max(y) + 1)
    plt.figure(figsize=(10, 10))
    plt.plot(x, y)
    plt.ylim(lower_range_y, upper_range_y)
    plt.xlim(-1, len(daily_statistics))
    plt.xlabel('Дата в формате ДД.ММ.ГГГГ')
    plt.ylabel('Вес(кг)')
    plt.xticks(rotation=90)
    file_name = FileName(user_id=user_id).get_name_for_chart_statistics_weight()
    plt.savefig(file_name)
    for i in range(15):
        if os.stat(file_name):
            return file_name
        time.sleep(1)
    logging.error(f"В течение 15 секунд не дождались создание файла с графиком динамики веса "
                  f"для пользователя: {user_id}")
