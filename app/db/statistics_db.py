from aiopg import Cursor

from app.schemas.postgresql_schemas import StatisticsSchemas


class StatisticsDB:
    """
    Класс для работы с базой данных postgresql и таблицей statistics
    """
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def get_all_statistics(self):
        """
        Тестовая функция, все ок работает
        :return:
        """
        # cursor = await self.get_cursor()
        await self._cursor.execute("select * from statistics")
        res = await self._cursor.fetchall()
        print(res)
        return res

    async def get_user_by_id(self, user_id: int) -> list[tuple] | None:
        """
        Получаем пользователя по id из таблицы статистики
        """
        await self._cursor.execute(f"SELECT * FROM statistics WHERE user_id = {user_id};")
        result = await self._cursor.fetchone()
        return result if result else None
    # SELECT row_to_json(t) statistics FROM (SELECT * FROM statistics WHERE user_id = 281626882 ORDER BY date DESC LIMIT 1) t;

    # async def get_last_activity_coef_today(self, user_id: int) -> int | None:
    #     """
    #     Получаем значение коэффициента активности за сегодня
    #     """
    #     await self._cursor.execute(f"SELECT activity_coef FROM statistics WHERE user_id = {user_id} "
    #                                f"AND date::date = current_date AND activity_coef IS NOT NULL ORDER BY date DESC;")
    #     result = await self._cursor.fetchone()
    #     return result[0] if result else None


    async def insert_row(self, data: StatisticsSchemas) -> None:
        """
        Добавляем строку
        :param data:
        :return:
        """
        # todo  разобраться можно ли как-то не через %s залить данные
        await self._cursor.execute(
            "INSERT INTO statistics(weight, spent_kcal, used_kcal, activity_coef, date, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s);", (data.weight, data.spent_kcal, data.used_kcal,
                                                 data.activity_coef, data.date, data.user_id))
