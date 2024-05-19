import httpx

from app.models.telegram.tg_request_models import SendMessageModel, EditMessageModel, AnswerCallbackQueryModel, \
    SendPhotoModel, SendDocumentModel
from app.models.telegram.tg_response_models import MessageModel
from app.utils.configuration_logger import logger


class TelegramApi:

    def __init__(self, telegram_api_token):
        self._client = httpx.AsyncClient()
        self._base_url = f"https://api.telegram.org/bot{telegram_api_token}"

    async def send_message(self, data: SendMessageModel) -> MessageModel:
        """
        Отправляем сообщение в чат
        """
        resp = await self._client.post(f"{self._base_url}/sendMessage", data=data.model_dump())
        resp_json = resp.json()
        if resp_json.get('ok'):
            return MessageModel(**resp_json['result'])
        logger.error(f"Не смогли отправить сообщение в чат: {data.chat_id}")

    async def edit_message(self, data: EditMessageModel) -> MessageModel:
        """
        Редактируем сообщение в чате
        """
        resp = await self._client.post(f"{self._base_url}/editMessageText", data=data.model_dump())
        resp_json = resp.json()
        if resp_json.get('ok'):
            return MessageModel(**resp_json['result'])
        logger.error(f"Не смогли отредактировать сообщение {data.message_id} в чате: {data.chat_id}")

    async def answer_callback_query(self, data: AnswerCallbackQueryModel):
        """
        Отвечаем на нажатие inline-кнопки
        """
        resp = await self._client.post(f"{self._base_url}/answerCallbackQuery", data=data.model_dump())
        resp_json = resp.json()
        if resp_json.get('ok'):
            return
        logger.error(f"Не смогли ответить на нажатие кнопки, answer callback query: {resp_json}")
        
    async def send_photo(self, data: SendPhotoModel):
        """
        Отправляем фото
        """
        resp = await self._client.post(f"{self._base_url}/sendPhoto", files=data.files_dict)
        resp_json = resp.json()
        if resp_json.get('ok'):
            return
        logger.error(f'Не смогли отправить фото со статистикой в чат: {data.chat_id}.\n{resp_json}')

    async def send_document(self, data: SendDocumentModel):
        """
        Отправляем документ
        """
        resp = await self._client.post(f"{self._base_url}/sendDocument", files=data.files_dict)
        resp_json = resp.json()
        if resp_json.get('ok'):
            return
        logger.error(f'Не смогли отправить документ с телом: {data.files_dict} в чат: {data.chat_id}.\n{resp_json}')
