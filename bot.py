import os
import telebot
import schedule
import time
import ssl
from aiohttp import web
from threading import Thread
from cat_api import CatApi


bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])
channel_id = -1001409952434
cat = CatApi()

WEBHOOK_HOST = ''
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

app = web.Application()

async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post('/{token}/', handle)

@bot.message_handler(commands=['start'])
def start_message(message):
    Thread(target=publisher).start()
    bot.send_message(message.chat.id, "Опять работать?(")


def publish():
    image = cat.get_image_url()
    bot.send_photo(channel_id, image)


def publisher():
    schedule.every().day.at("06:30").do(publish)
    schedule.every().day.at("09:00").do(publish)
    schedule.every().day.at("12:30").do(publish)
    schedule.every().day.at("16:30").do(publish)
    schedule.every().day.at("20:00").do(publish)
    while True:
        schedule.run_pending()
        time.sleep(1)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)

