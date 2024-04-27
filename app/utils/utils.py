import datetime

from pytz import timezone


class CurrentDate:

    @staticmethod
    def get_now() -> datetime:
        return datetime.datetime.now(tz=timezone('Europe/Moscow'))


class CalorieCount:

    def __init__(self, weight: float, activity_coef: int):
        self._weight = weight
        self._activity_coef = activity_coef
        self._multiplier_activity_coef = 20

    def get_calorie_count(self) -> int:
        return int(self._weight * self._multiplier_activity_coef + self._weight * self._activity_coef)
