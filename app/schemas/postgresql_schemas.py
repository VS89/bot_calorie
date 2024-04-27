from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class MessagesSchemas(BaseModel):
    """
    Модель для таблицы messages
    """

    user_id: int = Field(...)
    message_id: int = Field(...)
    text: str | None = Field(None)
    activity_coef_flag: bool | None = Field(False)
    confirmation_action_flag: bool | None = Field(False)
    statistics_flag: bool | None = Field(False)


class StatisticsSchemas(BaseModel):
    """
    Модель для таблицы statistics
    """

    user_id: int = Field(...)
    date: datetime = Field(..., description='Дата с указанием тайм зоны')
    weight: float | None = Field(None)
    spent_kcal: int | None = Field(None)
    used_kcal: int | None = Field(None)
    activity_coef: int | None = Field(None)


class UsersSchemas(BaseModel):
    """
    Модель для таблицы users
    """
    user_id: int = Field(...)
    date_update_data: datetime = Field(..., description='Дата, когда последний раз были обновлены данные')
    weight: float | None = Field(None)
    activity_coef: int | None = Field(None)
    calorie_count: int | None = Field(None, description='Норма калорий в день')
