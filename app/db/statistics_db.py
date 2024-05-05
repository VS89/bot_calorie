from aiopg import Cursor

from app.schemas.postgresql_schemas import StatisticsSchemas


class StatisticsDB:
    """
    Класс для работы с базой данных postgresql и таблицей statistics
    """
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def get_all_statistics_by_user_id(self, user_id: int) -> list[StatisticsSchemas] | None:
        """
        Получения всей статистики для пользователя
        """
        await self._cursor.execute(f"SELECT row_to_json(t) FROM "
                                   f"(SELECT * FROM statistics WHERE user_id = {user_id} ORDER BY save_date) t;")
        result = await self._cursor.fetchall()
        return [StatisticsSchemas(**i[0]) for i in result] if result else None

    async def get_statistics_by_days(self, count_days: int | str, user_id: int) -> list[StatisticsSchemas] | None:
        """
        Получаем статистику за количество дней == count_days
        :param count_days:
        :return:
        """
        await self._cursor.execute(f"SELECT row_to_json(t) FROM (SELECT * FROM statistics "
                                   f"WHERE save_date >= CURRENT_DATE - INTERVAL '{count_days} days' "
                                   f"AND user_id = {user_id} ORDER BY save_date) t;")
        result = await self._cursor.fetchall()
        return [StatisticsSchemas(**i[0]) for i in result] if result else None

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
        """
        await self._cursor.execute(
            "INSERT INTO statistics(weight, kcal, activity_coef, save_date, user_id, balance_calorie) "
            "VALUES (%s, %s, %s, %s, %s, %s);", (data.weight, data.kcal, data.activity_coef, data.save_date,
                                                 data.user_id, data.balance_calorie))

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
        """
        Получение последней строки из статистики по user_id
        """
        await self._cursor.execute(
            f"SELECT row_to_json(t) FROM ( SELECT * FROM public.statistics WHERE save_date::date = current_date "
            f"AND user_id = {user_id} ORDER BY save_date DESC LIMIT 1) t;"
        )
        result = await self._cursor.fetchone()
        return StatisticsSchemas(**result[0]) if result else None
