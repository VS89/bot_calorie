from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class EntitiesType(Enum):

    BOT_COMMAND = 'bot_command'


class FromMessageModel(BaseModel):
    """
    Информация от кого пришло сообщение
    """
    model_config = ConfigDict(extra='allow')

    first_name: str = Field(...)
    user_id: int = Field(..., alias='id')
    is_bot: bool = Field(...)
    last_name: str | None = Field(None)
    username: str | None = Field(None)
    language_code: str | None = Field(None)
    is_premium: bool | None = Field(None)


class ChatMessageModel(BaseModel):
    """
    Информация о чате из которого пришло сообщение
    """
    model_config = ConfigDict(extra='allow')

    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str | None = Field(None)
    user_id: int = Field(..., alias='id')
    type: str = Field(...)


class EntitiesModel(BaseModel):
    """
    Модель для команд
    """

    model_config = ConfigDict(validate_default=True, use_enum_values=True)

    offset: int = Field(...)
    length: int = Field(...)
    type: EntitiesType = Field(...)


class MessageModel(BaseModel):
    """
    Модель сообщения
    """

    model_config = ConfigDict(extra='allow')

    message_id: int = Field(...)
    from_msg: FromMessageModel = Field(..., alias='from')
    chat: ChatMessageModel = Field(...)
    date: int = Field(...)
    text: str | None = Field(None)
    reply_markup: dict | None = Field(None)
    entities: list[EntitiesModel] | None = Field(None)


class CallbackQueryModel(BaseModel):
    """
    Модель ответа при нажатии на кнопку
    """
    model_config = ConfigDict(extra='allow')

    callback_query_id: str = Field(..., alias='id')
    from_user: FromMessageModel = Field(..., alias='from')
    message: MessageModel = Field(...)
    chat_instance: str = Field(...)
    data: str = Field(...)


class TelegramResponse(BaseModel):

    update_id: int = Field(...)
    message: MessageModel | None = Field(None)
    callback_query: CallbackQueryModel | None = Field(None)
