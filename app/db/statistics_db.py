import psycopg2


class StatisticsDB:
    """
    Класс для работы с базой данных postgresql и таблицей statistics
    """

    def __init__(self):
        # todo эти данные спрятать потом
        self.__connect = psycopg2.connect(dbname='test_db', user='valentins', password='$yUi6g5uJoPbeN*GgEZr',
                                          host='127.0.0.1')
        self.__cursor = self.__connect.cursor()

    def __del__(self):
        self.__cursor.close()
        self.__connect.close()

    def get_all_data_from_statistics(self):
        self.__cursor.execute("SELECT * FROM statistics")
        res = self.__cursor.fetchall()
        for row in res:
            print(row)


# if __name__ == '__main__':
#     s = StatisticsDB()
#     s.get_all_data_from_statistics()