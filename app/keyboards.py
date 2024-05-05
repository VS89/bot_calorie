import json
from typing import Any

from math import ceil
from pydantic import BaseModel, Field


class InlineKeyboardButtonModel(BaseModel):
    """
    Inline кнопка для клавиатуры
    """

    text: str | int = Field(...)
    callback_data: str | None = Field(None)

    @property
    def dict_data_exclude_none(self) -> dict:
        return self.model_dump(exclude_none=True)


class InlineKeyboardsModel(BaseModel):
    """
    Inline клавиатура
    """

    rows: int = Field(1)

    def create_keyboard(self, buttons: list[InlineKeyboardButtonModel]) -> json:
        """
        Создание клавиатуры
        :param buttons: список кнопок
        :return: объект json
        """
        part = ceil(len(buttons)/self.rows)
        new_buttons = [i.dict_data_exclude_none for i in buttons]
        return json.dumps({'inline_keyboard': [new_buttons[part * k:part * (k + 1)] for k in range(self.rows)]})
