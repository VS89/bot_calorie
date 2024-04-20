import json
import logging
import httpx
import requests
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.requests import Request

from app.constants import CommandName
from app.handler_commands.command_help import HandlerCommandHelp
from app.handler_commands.command_start import HandlerCommandStart
from app.keyboards import InlineKeyboardsModel, InlineKeyboardButtonModel
from app.models.telegram_response_models import CallbackQueryModel, MessageModel, TelegramResponse, EntitiesType

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# todo токен надо спрятать в pydantic setting модель
TOKEN = "7126934059:AAF5QjfYEOKtolSuYYttRXBTnv0CLD5TMlI"

# todo надо будет написать свой апи класс для работы с телегой
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()

app = FastAPI()

# создание кнопок
replay_markup = json.dumps({
    "inline_keyboard": [
        [
            {
                "text": "Кнопка 1",
                "callback_data": "callback text 1"
            },
            {
                "text": "Кнопка 2",
                "callback_data": "callback text 2"
            }
        ]
    ]
})


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
                'text': "Я на что-то нажал"
            }
            await client.post(f"{BASE_URL}/sendMessage", data=resp_data)
            return
        if response_model.message.entities:
            if response_model.message.entities[0].type == EntitiesType.BOT_COMMAND.value:
                match response_model.message.text:
                    case CommandName.START:
                        text = HandlerCommandStart.get_start_message()
                    case CommandName.HELP:
                        text = HandlerCommandHelp.get_help_message()
                    case CommandName.ACTIVITY_COEF:
                        text = f"Обработка команды {CommandName.ACTIVITY_COEF}"
                    case CommandName.STATISTICS:
                        text = f"Обработка команды {CommandName.STATISTICS}"
                    case CommandName.EXPORT:
                        text = f"Обработка команды {CommandName.EXPORT}"
                    case _:
                        logging.info(f'Пользователь: {response_model.message.chat.user_id} '
                                     f'пытался использовать команду: {response_model.message.text}')
            resp_data = {
                'chat_id': response_model.message.chat.user_id,
                'text': text
            }
            await client.post(f"{BASE_URL}/sendMessage", data=resp_data)
            return
        else:
            logging.info(f"{response_model=}")
            resp_data = {
                "chat_id": response_model.message.chat.user_id,
                "text": "Какое-то сообщение",
                "reply_markup": InlineKeyboardsModel(rows=1).create_keyboard(buttons=[
                    InlineKeyboardButtonModel(text='1', callback_data='1'),
                    InlineKeyboardButtonModel(text='2', callback_data='callback text 2'),
                    InlineKeyboardButtonModel(text='3', callback_data='1'),
                    InlineKeyboardButtonModel(text='4', callback_data='1'),
                    InlineKeyboardButtonModel(text='5', callback_data='1'),
                ])
            }
            await client.post(f"{BASE_URL}/sendMessage", data=resp_data)
            return
    except Exception as e:
        logging.error(e)

    return data


# tg id 281626882
if __name__ == '__main__':
    tuna_url = "https://23jwez-31-134-187-85.ru.tuna.am"
    # todo запрос нужен чтобы заработал вебхук, его надо перенести в startup event
    resp = requests.get(url=f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={tuna_url}/webhook{TOKEN}")
    logging.info(f"Ответ от метода установки хука для телеги: {resp.json()}")
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
