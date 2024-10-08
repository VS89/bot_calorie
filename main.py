from contextlib import asynccontextmanager

import httpx
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.requests import Request

from app.constants import CommandName, PrefixCallbackData
from app.db.pg_connection_manager import PGConnectionManager
from app.external_api.telegram_api import TelegramApi
from app.handler.commands.command_activity_coef import HandlerCommandActivityCoef
from app.handler.commands.command_exports import HandlerExport
from app.handler.commands.command_help import HandlerCommandHelp
from app.handler.commands.command_start import HandlerCommandStart
from app.handler.commands.command_statistics import HandlerStatistics
from app.handler.handler_edit_weight import HandlerEditWeight
from app.handler.messages.handler_text import HandlerText
from app.models.handlers_model import HandlersModel
from app.models.telegram.tg_response_models import TelegramResponse, EntitiesType
from app.utils.configuration_logger import logger
from app.utils.settings import SettingsModel


settings = SettingsModel()
handlers = HandlersModel()
client = httpx.AsyncClient()
tg_api_client = TelegramApi(telegram_api_token=settings.tg_api_token)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Открываю подключение к бд")
    pg = PGConnectionManager(settings=settings)
    await pg.get_cursor()
    app_.pg = pg
    handlers.handler_edit_weight = HandlerEditWeight(tg_api_client=tg_api_client, users_db=pg.users_db,
                                                     statistics_db=pg.statistics_db, messages_db=pg.messages_db)
    handlers.handler_activity_coef = HandlerCommandActivityCoef(tg_api_client=tg_api_client, message_db=pg.messages_db,
                                                                users_db=pg.users_db)
    handlers.handler_statistics = HandlerStatistics(tg_api_client=tg_api_client, messages_db=pg.messages_db,
                                                    statistics_db=pg.statistics_db, users_db=pg.users_db)
    handlers.handler_export = HandlerExport(tg_api_client=tg_api_client, statistics_db=pg.statistics_db)
    yield
    logger.info("Закрываю подключение к бд")
    await pg.close()


app = FastAPI(lifespan=lifespan)


@app.post(f"/webhook{settings.tg_api_token}")
async def webhook(req: Request):
    data = await req.json()
    logger.info(f"{data=}")
    try:
        response_model = TelegramResponse(**data)
        if response_model.callback_query:
            # todo проверить этот кусок перед мержем в мастер
            match response_model.callback_query.data.split('_'):
                case PrefixCallbackData.ACTIVITY_COEF, *_:
                    await handlers.handler_activity_coef.handler_callback_data(
                        callback_query=response_model.callback_query
                    )
                case PrefixCallbackData.WEIGHT, *_:
                    await handlers.handler_edit_weight.handler_callback_data_edit_weight(
                        callback_query=response_model.callback_query
                    )
                case PrefixCallbackData.STATISTICS, *_:
                    await handlers.handler_statistics.handler_callback_data(
                        callback_query=response_model.callback_query
                    )
                case _:
                    logger.error(f'Получили неизвестный и необработанный callback: {response_model.callback_query}')
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
                        await handlers.handler_activity_coef.send_activity_coef_message(chat_id=chat_id)
                    case CommandName.STATISTICS:
                        await handlers.handler_statistics.send_statistics_message(user_id=chat_id)
                    case CommandName.EXPORT:
                        await handlers.handler_export.handler_export_command(user_id=chat_id)
                    case _:
                        logger.info(f'Пользователь: {response_model.message.chat.user_id} '
                                    f'пытался использовать команду: {response_model.message.text}')
            return
        logger.info(f"В обработчик текста передаем текст == {response_model.message.text}")
        await HandlerText(
            tg_api_client=tg_api_client,
            chat_id=response_model.message.chat.user_id,
            statistics_db=req.app.pg.statistics_db,
            messages_db=req.app.pg.messages_db,
            users_db=req.app.pg.users_db,
            handlers=handlers
        ).handler_text(text=response_model.message.text)
    except Exception as e:
        logger.error(e)

    return data


if __name__ == '__main__':
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
