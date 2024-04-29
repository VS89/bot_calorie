from typing import Any

from app.constants import TextBotMessage, PrefixCallbackData, LimitValues
from app.keyboards import InlineKeyboardButtonModel, InlineKeyboardsModel
from app.models.telegram.tg_request_models import SendMessageModel


class MessageBuilder:

    def __init__(self, user_id: int, callback_data: Any = None, text: str | None = None):
        self._user_id = user_id
        self._callback_data = callback_data
        self._text = text

    @property
    def confirm_activity_coef_msg(self) -> SendMessageModel:
        return SendMessageModel(
            chat_id=self._user_id,
            text=TextBotMessage.CONFIRM_CHANGE_ACTIVITY_COEF_MSG.format(self._callback_data),
            reply_markup=InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                InlineKeyboardButtonModel(
                    text=TextBotMessage.YES,
                    callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_{TextBotMessage.YES}_{self._callback_data}'),
                InlineKeyboardButtonModel(
                    text=TextBotMessage.NO,
                    callback_data=f'{PrefixCallbackData.ACTIVITY_COEF}_{TextBotMessage.NO}')
            ])
        )

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
