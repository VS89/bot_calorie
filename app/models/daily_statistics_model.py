from pydantic import BaseModel, Field, field_validator


class DailyStatisticsModel(BaseModel):

    date: str = Field(default=..., description="Дата в формате '%d.%m.%Y'")
    avg_weight: float = Field(default=..., description="Среднее значение веса за день")
    sum_kc_positive: int = Field(default=..., description="Сумма приобретенных кКал")
    sum_kc_negative: int = Field(default=..., description="Сумма потраченных кКал")
    daily_balance_calorie: int = Field(default=..., description="Баланс кКал за день")
    avg_activity_coef: int = Field(default=..., description="Округленное среднее значение коэффициента активности")

    @property
    def get_msg(self) -> str:
        return (f"{self.date}, {self.avg_weight}, {self.sum_kc_positive}, {self.sum_kc_negative}, "
                f"{self.daily_balance_calorie}")
