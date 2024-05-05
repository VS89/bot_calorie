import datetime

from pytz import timezone

from app.constants import FormatFile


class CurrentDate:

    @staticmethod
    def get_now() -> datetime:
        return datetime.datetime.now(tz=timezone('Europe/Moscow'))


class BalanceCalorie:

    def __init__(self, weight: float, activity_coef: int):
        self._weight = weight
        self._activity_coef = activity_coef
        self._multiplier_activity_coef = 20

    @property
    def get_balance_calorie_count(self) -> int:
        return int(self._weight * self._multiplier_activity_coef + self._weight * self._activity_coef)


class FileName:

    def __init__(self, user_id: int):
        self._file_path = '../.files'
        self._current_date_for_file_name = CurrentDate.get_now().strftime('%d%m%Y%H%M%S')
        self._user_id = user_id

    def _get_file_path(self, file_name: str, format_file: FormatFile) -> str:
        """
        Получаем путь для сохранения файла
        """
        return f'{self._file_path}/{file_name}_{self._user_id}_{self._current_date_for_file_name}.{format_file}'

    def get_name_for_chart_statistics_weight(self) -> str:
        """
        Получаем имя файла для графика статистики веса
        """
        return self._get_file_path(file_name='daily_statistics', format_file=FormatFile.PNG)

    def get_name_for_export_statistics(self):
        """
        Получаем имя файла для экспорта статистики
        :return:
        """
        return self._get_file_path(file_name='export_statistics', format_file=FormatFile.CSV)
