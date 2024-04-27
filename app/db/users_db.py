from aiopg import Cursor

from app.schemas.postgresql_schemas import UsersSchemas
from app.utils.utils import CurrentDate


class UsersDB:
    """
    Класс для работы с базой данных postgresql и таблицей messages
    """

    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def get_user_by_user_id(self, user_id: int) -> UsersSchemas | None:
        """
        Получаем пользователя по id из таблицы users
        """
        await self._cursor.execute(f"SELECT row_to_json(t) users FROM ( "
                                   f"SELECT * FROM users WHERE user_id = {user_id}) t;")
        result = await self._cursor.fetchone()
        return UsersSchemas(**result[0]) if result else None

    async def insert_user(self, data: UsersSchemas) -> None:
        """
        Добавление строки в таблицу юзеров
        """
        await self._cursor.execute(
            "INSERT INTO public.users(user_id, weight, activity_coef, date_update_data) "
            "VALUES (%s, %s, %s, %s);", (data.user_id, data.weight, data.activity_coef, data.date_update_data))

    async def update_weight(self, user_id: int, weight: float):
        """
        Обновление веса юзера
        """
        await self._cursor.execute(
            f"UPDATE public.users SET weight={weight}, date_update_data = '{CurrentDate.get_now()}' "
            f"WHERE user_id = {user_id};"
        )

    async def update_activity_coef(self, user_id: int, activity_coef: int):
        """
        Обновление коэффициента активности юзера
        """
        await self._cursor.execute(
            f"UPDATE public.users SET activity_coef={activity_coef}, date_update_data = '{CurrentDate.get_now()}' "
            f"WHERE user_id = {user_id};"
        )

    async def update_calorie_count(self, user_id: int, calorie_count: int):
        """
        Обновление нормы калорий
        """
        await self._cursor.execute(
            f"UPDATE public.users SET calorie_count={calorie_count}, date_update_data = '{CurrentDate.get_now()}' "
            f"WHERE user_id = {user_id};"
        )
