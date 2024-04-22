import httpx


class TelegramApi:

    def __init__(self, telegram_api_token):
        self.__client = httpx.AsyncClient()
        self.__base_url = f"https://api.telegram.org/bot{telegram_api_token}"

    async def send_message(self, data: dict):
        await self.__client.post(f"{self.__base_url}/sendMessage", data=data)
