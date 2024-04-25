import re
from app.constants import LimitValues


class ParseText:

    def __init__(self):
        pass

    def parse_text(self, text: str) -> float | None:
        """
        кейсы которые надо покрыть

        """
        pattern = r'(\b\d{2,3}(?:[.,]\d)?)\s*(кг|kg)'
        match = re.search(pattern, text.lower())
        # todo надо добавить обработку исключения
        if match:
            value_kg = float(match.group(1).replace(',', '.'))
            if LimitValues.MIN_VALUE_KG <= value_kg <= LimitValues.MAX_VALUE_KG:
                return value_kg

    def parse_kcal(self, text) -> int | None:
        """
        :param text:
        :return:
        """
        pattern = r'^([-+])?\s*(\d{1,4})\s*(кк|ккал|kc|kcal)'
        match = re.search(pattern, text.lower())
        # todo надо добавить обработку исключения
        if match:
            if match.group(1) == '-':
                return -int(match.group(2))
            else:
                return int(match.group(2))
