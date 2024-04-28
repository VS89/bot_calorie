import logging
from contextlib import asynccontextmanager

import httpx
import requests
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.requests import Request

from app.constants import CommandName, PrefixCallbackData
from app.db.pg_connection_manager import PGConnectionManager
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.handler.commands.command_help import HandlerCommandHelp
from app.handler.commands.command_start import HandlerCommandStart
from app.handler.messages.handler_text import HandlerText
from app.models.telegram.tg_request_models import SendMessageModel
from app.models.telegram.tg_response_models import TelegramResponse, EntitiesType


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logging.info("Открываю подключение к бд")
    pg = PGConnectionManager()
    await pg.get_cursor()
    app_.pg = pg
    yield
    logging.info("Закрываю подключение к бд")
    await pg.close()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# todo токен надо спрятать в pydantic setting модель
TOKEN = "7126934059:AAF5QjfYEOKtolSuYYttRXBTnv0CLD5TMlI"

# todo надо будет написать свой апи класс для работы с телегой
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()
tg_api_client = TelegramApi(telegram_api_token=TOKEN)

app = FastAPI(lifespan=lifespan)

handler_activity_coef = HandlerCommandActivityCoef(tg_api_client=tg_api_client)





@app.post(f"/webhook{TOKEN}")
async def webhook(req: Request):
    data = await req.json()
    logging.info(f"{data=}")
    response_model = TelegramResponse(**data)
    try:
        if response_model.callback_query:
            match response_model.callback_query.data.split('_'):
                case PrefixCallbackData.ACTIVITY_COEF, *v:
                    await handler_activity_coef.handler_callback_data(callback_query=response_model.callback_query,
                                                                      users_db=req.app.pg.users_db,
                                                                      message_db=req.app.pg.messages_db)
                case _:
                    logging.error(f'Получили неизвестный и необработанный callback: {response_model.callback_query}')
            return
        if response_model.message.entities:
            if response_model.message.entities[0].type == EntitiesType.BOT_COMMAND.value:
                chat_id = response_model.message.chat.user_id
                match response_model.message.text:
                    case CommandName.START:
                        await HandlerCommandStart(tg_api_client=tg_api_client, chat_id=chat_id,
                                                  users_db=req.app.pg.users_db,
                                                  messages_db=req.app.pg.messages_db).handler_start_command()
                    case CommandName.HELP:
                        await HandlerCommandHelp(tg_api_client=tg_api_client, chat_id=chat_id).send_help_message()
                    case CommandName.ACTIVITY_COEF:
                        await handler_activity_coef.send_activity_coef_message(chat_id=chat_id,
                                                                               message_db=req.app.pg.messages_db)
                    case CommandName.STATISTICS:
                        text = f"Обработка команды {CommandName.STATISTICS}"
                    case CommandName.EXPORT:
                        text = f"Обработка команды {CommandName.EXPORT}"
                    case _:
                        logging.info(f'Пользователь: {response_model.message.chat.user_id} '
                                     f'пытался использовать команду: {response_model.message.text}')
            return
        # await tg_api_client.send_message(data=SendMessageModel(
        #     chat_id=response_model.message.chat.user_id,
        #     text=f'Я то получил что ты написал: {response_model.message.text} но что мне с этим делать'))
        logging.info(f"В обработчик текста передаем текст == {response_model.message.text}")
        await HandlerText(
            tg_api_client=tg_api_client,
            chat_id=response_model.message.chat.user_id,
            statistics_db=req.app.pg.statistics_db,
            messages_db=req.app.pg.messages_db,
            users_db=req.app.pg.users_db
        ).handler_text(text=response_model.message.text)
    except Exception as e:
        logging.error(e)

    return data


# tg id 281626882
# DELETE FROM statistics WHERE user_id = 281626882;
if __name__ == '__main__':
    # tuna_url = "https://pohudiziryi-bot-tg.ru.tuna.am"
    # todo запрос нужен чтобы заработал вебхук, его надо перенести в startup event
    # resp = requests.get(url=f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={tuna_url}/webhook{TOKEN}")
    # logging.info(f"Ответ от метода установки хука для телеги: {resp.json()}")
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
