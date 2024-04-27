from enum import Enum

from pydantic import BaseModel, Field, json, ConfigDict


class AllowedUpdate(Enum):

    MESSAGE = 'message'
    EDITED_MESSAGE = 'edited_message'
    CHANNEL_POST = 'channel_post'
    EDITED_CHANNEL_POST = 'edited_channel_post'
    INLINE_QUERY = 'inline_query'
    CHOSEN_INLINE_RESULT = 'chosen_inline_result'
    CALLBACK_QUERY = 'callback_query'
    SHIPPING_QUERY = 'shipping_query'
    PRE_CHECKOUT_QUERY = 'pre_checkout_query'


class SendMessageModel(BaseModel):
    """
    Модель для метода отправки сообщения tg_api -> sendMessage
    """

    chat_id: int = Field(...)
    text: str = Field(None)
    reply_markup: str = Field(None)


class EditMessageModel(SendMessageModel):
    """
    Модель для метода редактирования сообщения tg_api -> editMessageText
    """

    message_id: int = Field(...)


class GetHistoryModel(BaseModel):

    peer: int = Field(..., description='{"_": "channelID"}, // ID канала или чата, где находятся сообщения')
    offset_id: int = Field(0, description='ID первого сообщения для получения')
    offset_date: int = Field(0, description='Дата первого сообщения для получения')
    limit: int = Field(100, description='Максимальное количество сообщений для получения')
    max_id: int = Field(0, description='ID последнего сообщения, которое уже получено')
    min_id: int = Field(0, description='ID первого сообщения, которое нужно получить')


class GetUpdatesModel(BaseModel):

    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    chat_id: int = Field(...)
    # offset: int = Field(0)
    limit: int = Field(0)
    # timeout: int = Field(0)
    # allowed_updates: list[AllowedUpdate] = Field([AllowedUpdate.MESSAGE])


class AnswerCallbackQueryModel(BaseModel):

    callback_query_id: str = Field(...)
    text: str | None = Field(None)
    show_alert: bool = Field(False)
    url: str | None = Field(None)
    cache_time: int | None = Field(0)


