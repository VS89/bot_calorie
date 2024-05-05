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


class AnswerCallbackQueryModel(BaseModel):
    """
    Модель для ответа на нажатие inline-кнопки
    """

    callback_query_id: str = Field(...)
    text: str | None = Field(None)
    show_alert: bool = Field(False)
    url: str | None = Field(None)
    cache_time: int | None = Field(0)


class SendPhotoModel(BaseModel):
    """
    Модель для отправки фото
    """

    chat_id: int | str = Field(...)
    photo_path: str = Field(...)
    photo_name: str | None = Field(default='output.png')
    caption: str | None = Field(default='')

    @property
    def files_dict(self) -> dict:
        return {
            'chat_id': (None, str(self.chat_id)),
            'photo': (self.photo_name, open(self.photo_path, 'rb'), 'image/png'),
            'caption': (None, self.caption)
        }


class SendDocumentModel(BaseModel):
    """
    Модель для отправки файла
    """
    chat_id: int | str = Field(...)
    document_path: str = Field(...)
    document_extension: str = Field(default='text/csv')
    document_name: str | None = Field(default='document')
    caption: str | None = Field(default='')

    @property
    def files_dict(self):
        return {
            'chat_id': (None, str(self.chat_id)),
            'document': (self.document_name, open(self.document_path, 'rb'), self.document_extension),
            'caption': (None, self.caption)
        }



