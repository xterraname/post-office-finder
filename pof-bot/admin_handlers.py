from telebot.types import Message
from telebot import TeleBot

from models import User


def admin_command(message: Message, bot: TeleBot):
    users_count = User.select().count()
    
    bot.send_message(message.chat.id, f"Users count: {users_count}")