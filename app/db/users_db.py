from aiopg import Cursor

from app.schemas.postgresql_schemas import UsersSchemas


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
            "INSERT INTO users (user_id, weight, activity_coef, date_update_data) "
            "VALUES (%s, %s, %s, %s);", (data.user_id, data.weight, data.activity_coef, data.date_update_data))

    async def update_data(self, data: UsersSchemas):
        """
        Обновление данных в таблице
        """
        await self._cursor.execute(
            f"UPDATE public.users SET {data.get_set_string_for_update_data} WHERE user_id = {data.user_id};"
        )
