import pytest

from app.constants import LimitValues
from app.utils.parse_text import ParseText


class TestParseText:

    @pytest.mark.parametrize('text, exp_value', [
        ('Мой вес 72кг', 72.0),
        ('Мой вес 39кг', None),
        ('Мой вес 251кг', None),
        ('Мой вес 111 кг', 111.0),
        ('Мой вес 44    кг', 44.0),
        ('Мой вес 77KG', 77.0),
        ('Мой вес 82.0кг', 82.0),
        ('Мой вес 82,7 кг', 82.7),
        ('Мой вес 99;1кг', None),
        ('Мой вес 111,1      кг', 111.1),
        ('Мой вес 123 asdqwe кг', None),
        ('кг', None),
        (f'Мой вес {LimitValues.MAX_VALUE_KG}кг', LimitValues.MAX_VALUE_KG),
        (f'Мой вес {LimitValues.MIN_VALUE_KG}кг', LimitValues.MIN_VALUE_KG)
    ])
    def test_parse_kg(self, text, exp_value):
        """
        Проверяем, что работает регулярное выражение: (\b\d{2,3}(?:[.,]\d)?)\s*(кг|kg), которое ищет и возвращает
        значения(float) в кг, если не находит, то None
        """
        value = ParseText(text).parse_kg()
        assert value == exp_value, (f"Ошибка, ожидали что для текста '{text}' распарсится значение == {exp_value}, "
                                    f"получили {value}")

    @pytest.mark.parametrize('text, exp_value', [
        ('-1кк', -1),
        ('+1ккал', 1),
        ('1 kc', 1),
        ('1  kcal', 1),
        ('1111 кк', 1111),
        ('1111  ккал', 1111),
        ('- 1111kc', -1111),
        ('+  1111kcal', 1111)
    ])
    def test_parse_kcal(self, text, exp_value):
        """
        Проверяем, что работает регулярное выражение: ^([-+])?\s*(\d{1,4})\s*(кк|ккал|kc|kcal),
        которое ищет и возвращает значения(int) в ккал, если не находит, то None
        """
        value = ParseText(text).parse_kcal()
        assert value == exp_value, (f"Ошибка, ожидали что для текста '{text}' распарсится значение == {exp_value}, "
                                    f"получили {value}")

