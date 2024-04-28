from aiopg import Cursor

from app.schemas.postgresql_schemas import MessagesSchemas


class MessagesDB:
    """
    Класс для работы с базой данных postgresql и таблицей messages
    """

    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    async def get_all_messages(self):
        """
        Тестовая функция, все ок работает
        :return:
        """
        await self._cursor.execute("select * from messages;")
        res = await self._cursor.fetchall()

    async def insert_message(self, data: MessagesSchemas):
        """
        Сохраняем сообщение в таблицу
        """
        await self._cursor.execute(
            "INSERT INTO messages(user_id, activity_coef, confirmation_action_flag, statistics_flag, "
            "text, message_id) VALUES (%s, %s, %s, %s, %s, %s);",
            (data.user_id, data.activity_coef, data.confirmation_action_flag, data.statistics_flag,
             data.text, data.message_id))

    async def get_last_message_by_user_id(self, user_id: int) -> MessagesSchemas | None:
        """
        Получаем последнее сохраненное сообщение по user_id
        """
        await self._cursor.execute(f"SELECT row_to_json(t) message FROM (SELECT * FROM messages "
                                   f"WHERE user_id = {user_id} ORDER BY message_id DESC) t;")
        result = await self._cursor.fetchone()
        return MessagesSchemas(**result[0]) if result else None

    async def delete_message_by_message_id(self, message_id: int):
        """
        Удаляем сообщение по message_id
        """
        await self._cursor.execute(f"DELETE FROM messages WHERE message_id = {message_id};")

    async def delete_all_message_user(self, user_id: int):
        """
        Удаляем все сообщения от пользователя
        """
        await self._cursor.execute(f"DELETE FROM messages WHERE user_id = {user_id};")
