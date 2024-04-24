import aiopg


class StatisticsDB:
    """
    Класс для работы с базой данных postgresql и таблицей statistics
    """

    def __init__(self):
        # todo эти данные спрятать потом
        self.__dsn = f'dbname=test_db user=valentins password=$yUi6g5uJoPbeN*GgEZr host=127.0.0.1'

    async def __execute(self, query: str):
        """

        :param query:
        :return:
        """
        pool = await aiopg.create_pool(self.__dsn)
        async with pool.acquire() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
        pool.close()
        await pool.wait_closed()
        return result

    async def get_all_statistics(self):
        """
        Тестовая функция, все ок работает
        :return:
        """
        res = await self.__execute(query="select * from statistics")
        print(res)


# async def main():
#     s = StatisticsDB()
#     await s.test_decorate()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
