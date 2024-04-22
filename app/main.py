import json
import logging
import httpx
import requests
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.requests import Request

from app.constants import CommandName
from app.external_api.telegram_api import TelegramApi
from app.handler_commands.command_activity_coef import HandlerCommandActivityCoef
from app.handler_commands.command_help import HandlerCommandHelp
from app.handler_commands.command_start import HandlerCommandStart
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram_response_models import  TelegramResponse, EntitiesType

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# todo токен надо спрятать в pydantic setting модель
TOKEN = "7126934059:AAF5QjfYEOKtolSuYYttRXBTnv0CLD5TMlI"

# todo надо будет написать свой апи класс для работы с телегой
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()
tg_api_client = TelegramApi(telegram_api_token=TOKEN)

app = FastAPI()


@app.post(f"/webhook{TOKEN}")
async def webhook(req: Request):
    logging.info("Я зашел в вебхук")
    data = await req.json()
    logging.info(f"{data=}")
    response_model = TelegramResponse(**data)
    try:
        if response_model.callback_query:
            resp_data = {
                'chat_id': response_model.callback_query.message.chat.user_id,
                'text': f"Я на кнопку с callback_data == {response_model.callback_query.data}"
            }
            await client.post(f"{BASE_URL}/sendMessage", data=resp_data)
            return
        if response_model.message.entities:
            if response_model.message.entities[0].type == EntitiesType.BOT_COMMAND.value:
                chat_id = response_model.message.chat.user_id
                match response_model.message.text:
                    case CommandName.START:
                        await HandlerCommandStart(tg_api_client=tg_api_client, chat_id=chat_id).send_start_message()
                    case CommandName.HELP:
                        await HandlerCommandHelp(tg_api_client=tg_api_client, chat_id=chat_id).send_help_message()
                    case CommandName.ACTIVITY_COEF:
                        await HandlerCommandActivityCoef(tg_api_client=tg_api_client,
                                                         chat_id=chat_id).send_activity_coef_message()
                    case CommandName.STATISTICS:
                        text = f"Обработка команды {CommandName.STATISTICS}"
                    case CommandName.EXPORT:
                        text = f"Обработка команды {CommandName.EXPORT}"
                    case _:
                        logging.info(f'Пользователь: {response_model.message.chat.user_id} '
                                     f'пытался использовать команду: {response_model.message.text}')
            # resp_data = {
            #     'chat_id': response_model.message.chat.user_id,
            #     'text': text
            # }
            # await client.post(f"{BASE_URL}/sendMessage", data=resp_data)
            return
    except Exception as e:
        logging.error(e)

    return data


# tg id 281626882
if __name__ == '__main__':
    tuna_url = "https://cu4hnz-31-134-187-85.ru.tuna.am"
    # todo запрос нужен чтобы заработал вебхук, его надо перенести в startup event
    resp = requests.get(url=f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={tuna_url}/webhook{TOKEN}")
    logging.info(f"Ответ от метода установки хука для телеги: {resp.json()}")
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
