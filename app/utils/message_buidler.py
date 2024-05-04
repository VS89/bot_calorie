from typing import Any

from app.constants import TextBotMessage, PrefixCallbackData, LimitValues
from app.keyboards import InlineKeyboardButtonModel, InlineKeyboardsModel
from app.models.daily_statistics_model import DailyStatisticsModel
from app.models.telegram.tg_request_models import SendMessageModel


class MessageBuilder:

    def __init__(self, user_id: int, callback_data: Any = None, text: str | None = None):
        self._user_id = user_id
        self._callback_data = callback_data
        self._text = text

    def _confirm_message(self, text_msg: str, prefix_callback_data: str) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=text_msg,
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(
                    text=TextBotMessage.YES,
                    callback_data=f'{prefix_callback_data}_{TextBotMessage.YES}_{self._callback_data}'),
                InlineKeyboardButtonModel(
                    text=TextBotMessage.NO,
                    callback_data=f'{prefix_callback_data}_{TextBotMessage.NO}')
            ])
        )

    @property
    def confirm_activity_coef_msg(self) -> SendMessageModel:
        return self._confirm_message(
            text_msg=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(self._callback_data),
            prefix_callback_data=PrefixCallbackData.ACTIVITY_COEF)

    @property
    def select_activity_coef_msg(self) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=self._text,
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(text='1', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_1'),
                InlineKeyboardButtonModel(text='2', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_2'),
                InlineKeyboardButtonModel(text='3', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_3'),
                InlineKeyboardButtonModel(text='4', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_4'),
                InlineKeyboardButtonModel(text='5', callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_5'),
            ])
        )

    @property
    def success_registration_msg(self) -> SendMessageModel:
        return SendMessageModel(chat_id=self._user_id, text=TextBotMessage.SUCCESS_REGISTRATION_MSG)

    @property
    def save_new_weight(self) -> SendMessageModel:
        return SendMessageModel(chat_id=self._user_id, text=TextBotMessage.SAVE_NEW_WEIGHT.format(self._text))

    @property
    def confirm_resave_new_weight(self) -> SendMessageModel:
        return self._confirm_message(text_msg=self._text,
                                     prefix_callback_data=PrefixCallbackData.WEIGHT)

    @property
    def select_period_statistics(self) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=TextBotMessage.SELECT_PERIOD_STATISTICS,
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(
                    text=LimitValues.STATISTIC_10_DAY,
                    callback_data=f'{PrefixCallbackData.STATISTICS}_{LimitValues.STATISTIC_10_DAY}'),
                InlineKeyboardButtonModel(
                    text=LimitValues.STATISTIC_30_DAY,
                    callback_data=f'{PrefixCallbackData.STATISTICS}_{LimitValues.STATISTIC_30_DAY}'),
            ])
        )

    def calorie_balance_message(self, kcal_balance: int) -> SendMessageModel:
        if kcal_balance < LimitValues.CALORIE_BALANCE_LIMIT_D:
            text_msg = TextBotMessage.KCAL_BALANCE_LESS_MINUS_50
        elif LimitValues.CALORIE_BALANCE_LIMIT_D <= kcal_balance < LimitValues.CALORIE_BALANCE_LIMIT_C:
            text_msg = TextBotMessage.KCAL_BALANCE_MORE_MINUS_50_LESS_100
        elif LimitValues.CALORIE_BALANCE_LIMIT_C <= kcal_balance < LimitValues.CALORIE_BALANCE_LIMIT_B:
            text_msg = TextBotMessage.KCAL_BALANCE_MORE_100_LESS_490
        elif LimitValues.CALORIE_BALANCE_LIMIT_B <= kcal_balance < LimitValues.CALORIE_BALANCE_LIMIT_A:
            text_msg = TextBotMessage.KCAL_BALANCE_MORE_490_LESS_550
        else:
            text_msg = TextBotMessage.KCAL_BALANCE_MORE_550.format(kcal_balance)
        return SendMessageModel(
            chat_id=self._user_id,
            text=text_msg
        )

    def statistics_message_by_period(self, statistics_msg_model: list[DailyStatisticsModel]) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=f"{TextBotMessage.STATISTICS_MSG}\n{'\n'.join([i.get_msg for i in statistics_msg_model])}"
        )
