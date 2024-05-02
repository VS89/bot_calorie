from datetime import datetime

from pydantic import BaseModel, Field

from app.utils.utils import CurrentDate


class MessagesSchemas(BaseModel):
    """
    Модель для таблицы messages
    """

    user_id: int = Field(...)
    message_id: int = Field(...)
    text: str | None = Field(None)
    activity_coef: int | None = Field(None)
    update_weight: float | None = Field(None)
    statistics_flag: bool | None = Field(False)


class StatisticsSchemas(BaseModel):
    """
    Модель для таблицы statistics
    """

    user_id: int = Field(...)
    save_date: datetime = Field(default_factory=CurrentDate.get_now, description='Дата с указанием тайм зоны')
    weight: float | None = Field(None)
    kcal: int | None = Field(None)
    activity_coef: int | None = Field(None)


class UsersSchemas(BaseModel):
    """
    Модель для таблицы users
    """

    user_id: int = Field(...)
    date_update_data: datetime = Field(default_factory=CurrentDate.get_now,
                                       description='Дата, когда последний раз были обновлены данные')
    weight: float | None = Field(None)
    activity_coef: int | None = Field(None)
    balance_calorie: int | None = Field(None, description='Норма калорий в день')

    @property
    def get_set_string_for_update_data(self) -> str:
        result = []
        for k, v in self.model_dump(exclude_none=True).items():
            if k == 'date_update_data':
                result.append(f"{k}='{v}'")
            else:
                result.append(f'{k}={v}')
        return ', '.join(result)
