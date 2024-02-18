import argparse
import logging

import telebot

import handlers
from config_handler import get_token

logger = telebot.logger
logger.setLevel(logging.ERROR)
logging.basicConfig(filemode="a", filename="logs.txt")

parser = argparse.ArgumentParser()

parser.add_argument(
    "-m", "--mode", default="local", choices=["local", "dev"], help="Run mode"
)
args = parser.parse_args()


def register_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        handlers.send_welcome, commands=["start", "help"], pass_bot=True
    )
    bot.register_message_handler(
        handlers.finder, content_types=["location"], pass_bot=True
    )
    bot.register_message_handler(
        handlers.echo_all, unc=lambda message: True, pass_bot=True
    )

    bot.register_callback_query_handler(
        handlers.back_callback,
        func=lambda c: c.data.startswith(handlers.location_factory.prefix),
        pass_bot=True
    )


TOKEN = get_token(args.mode)

bot = telebot.TeleBot(TOKEN, parse_mode="html")
register_handlers(bot)

me = bot.get_me()

print("Bot running...")
print("mode:", args.mode)
print("token:", TOKEN)
print("username:", me.username)

bot.infinity_polling()
