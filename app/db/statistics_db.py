import datetime

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

    async def insert_row(self, data: StatisticsSchemas) -> None:
        """
        Добавляем строку
        :param data:
        :return:
        """
        # todo разобраться можно ли как-то не через %s залить данные
        await self._cursor.execute(
            "INSERT INTO statistics(weight, kcal, activity_coef, save_date, user_id) "
            "VALUES (%s, %s, %s, %s, %s);", (data.weight, data.kcal, data.activity_coef, data.save_date,
                                             data.user_id))

    async def get_sum_kcal_for_current_date(self, user_id: int) -> int | None:
        """
        Получение суммы kcal
        """
        await self._cursor.execute(
            f"SELECT SUM(kcal) FROM statistics WHERE save_date::date = current_date AND user_id = {user_id};"
        )
        result = await self._cursor.fetchone()
        return result[0] if result else None

    async def get_count_uniq_weight_by_user_id_today(self, user_id: int) -> int:
        """
        Получение количество уникальных параметров веса пользователя за сегодня
        """
        await self._cursor.execute(
            f"SELECT COUNT(DISTINCT weight) FROM statistics WHERE save_date::date = current_date "
            f"AND user_id = {user_id};"
        )
        result = await self._cursor.fetchone()
        return result[0] if result else None

    async def get_last_row_by_user_id(self, user_id: int) -> StatisticsSchemas | None:
        await self._cursor.execute(
            f"SELECT row_to_json(t) FROM ( SELECT * FROM public.statistics WHERE save_date::date = current_date "
            f"AND user_id = {user_id} ORDER BY save_date DESC LIMIT 1) t;"
        )
        result = await self._cursor.fetchone()
        return StatisticsSchemas(**result[0]) if result else None
