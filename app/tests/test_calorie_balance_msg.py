import pytest

from app.constants import TextBotMessage, LimitValues
from app.utils.message_buidler import MessageBuilder


class TestCalorieBalanceMsg:

    @pytest.mark.parametrize('user_balance_calorie, kcal_sum, exp_text_msg',
                             [(1150, 100, TextBotMessage.KCAL_BALANCE_MORE_550.format(550)),
                              (1151, 100, TextBotMessage.KCAL_BALANCE_MORE_550.format(551)),
                              (1149, 100, TextBotMessage.KCAL_BALANCE_MORE_490_LESS_550),
                              (1090, 100, TextBotMessage.KCAL_BALANCE_MORE_490_LESS_550),
                              (1089, 100, TextBotMessage.KCAL_BALANCE_MORE_100_LESS_490),
                              (700, 100, TextBotMessage.KCAL_BALANCE_MORE_100_LESS_490),
                              (699, 100, TextBotMessage.KCAL_BALANCE_MORE_MINUS_50_LESS_100),
                              (550, 100, TextBotMessage.KCAL_BALANCE_MORE_MINUS_50_LESS_100),
                              (549, 100, TextBotMessage.KCAL_BALANCE_LESS_MINUS_50)])
    def test_calorie_balance_msg(self, user_balance_calorie, kcal_sum, exp_text_msg):
        """
        Проверяем разные тексты для разного баланса ккал
        """
        kcal_balance = user_balance_calorie - kcal_sum - LimitValues.CALORIE_DEFICIT
        calorie_balance_msg = MessageBuilder(user_id=1111).calorie_balance_message(kcal_balance)
        assert calorie_balance_msg.text == exp_text_msg, \
            (f"Ожидали, что при балансе {kcal_balance} получим сообщение с текстом '{exp_text_msg}',"
             f" НО получили '{calorie_balance_msg.text}'")
