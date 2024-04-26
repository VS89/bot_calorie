import aiopg

from app.db.messages_db import MessagesDB
from app.db.statistics_db import StatisticsDB


class PGConnectionManager:
    def __init__(self):
        self._dsn = f'dbname=test_db user=valentins password=$yUi6g5uJoPbeN*GgEZr host=127.0.0.1'
        self._pool = None
        self._connection = None
        self._cursor = None
        self._statistics_db: StatisticsDB | None = None
        self._messages_db: MessagesDB | None = None

    async def _get_pool(self):
        if self._pool is None or self._pool.closed:
            self._pool = await aiopg.create_pool(self._dsn)
        return self._pool

    async def _get_connection(self):
        await self._get_pool()
        if not self._connection or self._connection.closed:
            self._connection = await self._pool.acquire()
        return self._connection

    async def get_cursor(self):
        await self._get_connection()
        if not self._cursor or self._cursor.closed:
            self._cursor = await self._connection.cursor()
            self._statistics_db = StatisticsDB(self._cursor)
            self._messages_db = MessagesDB(self._cursor)
        return self._cursor

    async def close(self):
        if self._cursor is not None:
            self._cursor.close()
        if self._connection is not None:
            self._connection.close()
        if self._pool is not None:
            self._pool.close()

    @property
    def statistics_db(self) -> StatisticsDB:
        return self._statistics_db

    @property
    def messages_db(self) -> MessagesDB:
        return self._messages_db
