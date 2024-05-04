import asyncio
import datetime
from random import randint

from pytz import timezone

from app.db.pg_connection_manager import PGConnectionManager
from app.schemas.postgresql_schemas import StatisticsSchemas


async def generate_statistics(count_days: int = 10, user_id: int = 281626882):
    """
    Генерация статистики
    """
    pg = PGConnectionManager()
    await pg.get_cursor()
    if count_days == 10:
        weight = [77.0, 78.1, 79.3, 78.5, 77.6, 77.0, 78.1, 79.3, 78.5, 77.6]
        balance_c = [1694, 1718, 1744, 1705, 1707, 1694, 1718, 1744, 1705, 1707]
        save_date = [datetime.datetime.now(tz=timezone('Europe/Moscow')) - datetime.timedelta(days=i) for i in
                     range(9, -1, -1)]
        range_create = 10
    else:
        weight = [77.0, 78.1, 79.3, 78.5, 77.6, 77.0, 78.1, 79.3, 78.5, 77.6, 77.0, 78.1, 79.3, 78.5, 77.6, 77.0,
                  78.1, 79.3, 78.5, 77.6, 77.0, 78.1, 79.3, 78.5, 77.6, 77.0, 78.1, 79.3, 78.5, 77.6]
        balance_c = [1694, 1718, 1744, 1705, 1707, 1694, 1718, 1744, 1705, 1707, 1694, 1718, 1744, 1705, 1707, 1694,
                     1718, 1744, 1705, 1707, 1694, 1718, 1744, 1705, 1707, 1694, 1718, 1744, 1705, 1707]
        save_date = [datetime.datetime.now(tz=timezone('Europe/Moscow')) - datetime.timedelta(days=i) for i in
                     range(29, -1, -1)]
        range_create = 30
    for i in range(range_create):
        for y in range(10):
            await pg.statistics_db.insert_row(data=StatisticsSchemas(
                user_id=user_id,
                save_date=save_date[i],
                balance_calorie=balance_c[i],
                weight=weight[i],
                activity_coef=2,
                kcal=randint(-1000, 1000)
            ))
    await pg.close()


if __name__ == '__main__':
    asyncio.run(generate_statistics(count_days=30))
