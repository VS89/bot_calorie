import re
from app.constants import LimitValues


class ParseText:

    def __init__(self, text: str):
        self._text = text

    def parse_weight(self) -> float | None:
        """
        Парсим значение кг из текста
        """
        pattern = r'(\b\d{2,3}(?:[.,]\d)?)\s*(кг|kg)$'
        match = re.search(pattern, self._text.lower())
        # todo надо добавить обработку исключения
        if match:
            value_kg = float(match.group(1).replace(',', '.'))
            if LimitValues.MIN_VALUE_KG <= value_kg <= LimitValues.MAX_VALUE_KG:
                return value_kg

    def parse_kcal(self) -> int | None:
        """
        Парсим значение ккал из текста
        """
        pattern = r'^([-+])?\s*(\d{1,4})\s*(кк|ккал|kc|kcal)$'
        match = re.search(pattern, self._text.lower())
        # todo надо добавить обработку исключения
        if match:
            if match.group(1) == '-':
                return -int(match.group(2))
            else:
                return int(match.group(2))

    def parse_digit(self) -> int | None:
        """
        Парсим первую цифру в тексте
        """
        pattern = r'[1-5]'
        match = re.search(pattern, self._text)
        if match:
           return int(match.group())
