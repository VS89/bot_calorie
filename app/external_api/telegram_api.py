import httpx

from app.models.telegram.tg_request_models import SendMessageModel, GetHistoryModel, GetUpdatesModel


class TelegramApi:

    def __init__(self, telegram_api_token):
        self.__client = httpx.AsyncClient()
        self.__base_url = f"https://api.telegram.org/bot{telegram_api_token}"

    async def send_message(self, data: SendMessageModel):
        """
        Отправляем сообщение в чат
        """
        await self.__client.post(f"{self.__base_url}/sendMessage", data=data.model_dump())

    # todo этот метод пока не работает, возможно откажусь от него
    async def get_history(self, params: GetHistoryModel):
        """
        Получаем историю сообщений из чата
        """
        await self.__client.post(f"{self.__base_url}/getHistory", data=params.model_dump())

    # todo тоже пока не работает вместе с вебхуком эта херь не работает
    async def get_updates(self, data: GetUpdatesModel):
        """
        Получаем данные из чата
        """
        await self.__client.post(f"{self.__base_url}/getUpdates", data=data.model_dump())
