import re
from app.constants import LimitValues


class ParseText:

    def __init__(self):
        pass

    def parse_text(self, text: str) -> float | None:
        """
        кейсы которые надо покрыть

        Для кг:
        Пользователь вводит целое число или 1 знак после запятой и кг/kg. Данные могут быть введены:
	    - Без пробелов - "85кг"
	    - С одним или несколькими пробелами - "85 kg", "85  kg"
	    - В качестве разделителя может быть точка или запятая - "85.1kg", "85,1kg"

	    Для ККАЛ
	    1) Пользователь вводит сообщение, которое содержит только целое число, одно из ключевых слов (кКал, kcal,
	    kc, кк), регистр любой и знак перед числом(опционально)
        2) Если пользователь ничего не ввел перед числом или указал знак "+", то мы считаем, что это набранные кКал
        3) Если пользователь указывает знак "-" перед числом, то мы считаем, что это потраченные кКал
        """
        pattern = r'(\b\d{2,3}(?:[.,]\d)?)\s*(кг|kg)'
        match = re.search(pattern, text.lower())
        # todo надо добавить обработку исключения
        if match:
            value_kg = float(match.group(1).replace(',', '.'))
            if LimitValues.MIN_VALUE_KG <= value_kg <= LimitValues.MAX_VALUE_KG:
                print(value_kg)
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
