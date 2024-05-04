import os
import time

import matplotlib.pyplot as plt

from app.models.daily_statistics_model import DailyStatisticsModel


def create_chart_png(daily_statistics: list[DailyStatisticsModel]) -> str | None:
    """
    Создаем график с разрешением .png и возвращаем байты для отправки картинки
    """
    x = [i.date for i in daily_statistics]
    y = [float(f"{i.avg_weight:.1f}") for i in daily_statistics]
    lower_range_y = int(min(y) - 1)
    upper_range_y = int(max(y) + 1)
    plt.figure(figsize=(10, 10))
    plt.plot(x, y)
    plt.ylim(lower_range_y, upper_range_y)
    plt.xlim(-1, len(daily_statistics))
    plt.xlabel("Дата в формате ДД.ММ.ГГГГ")
    plt.ylabel("Вес(кг)")
    plt.xticks(rotation=90)
    plt.savefig('output.png')
    # todo научится генерить названия и сохранять в .files, подробней описал в obsidian
    for i in range(15):
        if os.stat('/Users/valentins/Desktop/pet_projects/bot_kalori/app/output.png'):
            return '/Users/valentins/Desktop/pet_projects/bot_kalori/app/output.png'
        time.sleep(1)
    return
