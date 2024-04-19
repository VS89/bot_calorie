import json
import logging
import httpx
import requests
import uvicorn
import uvloop
from fastapi import FastAPI
from starlette.requests import Request
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Какой-то текст")
#
#
# if __name__ == '__main__':
#     app = ApplicationBuilder().token('7126934059:AAF5QjfYEOKtolSuYYttRXBTnv0CLD5TMlI').build()
#     start_handler = CommandHandler('start', start)
#     app.add_handler(start_handler)
#
#     app.run_polling()

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
    try:
        if data.get('callback_query'):
            if data['callback_query'].get('data') == 'callback text 2':
                chat_id = data['callback_query']['message']['chat']['id']
                text = "Вы нажали кнопку 2"
        else:
            chat_id = data['message']['chat']['id']
            text = data['message']['text']

        logging.info(f'мой чат ид == {chat_id}')
        # await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={text}")
        # todo надо разобраться как крепить кнопки к сообщению через апи
        # Prepare the data payload
        data = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": replay_markup
        }
        resp = await client.post(f"{BASE_URL}/sendMessage", data=data)
        logging.info(resp.json())
    except Exception as e:
        logging.error(e)

    return data


# tg id 281626882
if __name__ == '__main__':
    # tuna_url = "https://zzvj7k-31-134-187-85.ru.tuna.am"
    # todo запрос нужен чтобы заработал вебхук, его надо перенести в startup event
    # requests.get(url=f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={tuna_url}/webhook{TOKEN}")
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
