from telebot.types import (
    Location,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from telebot import TeleBot
from telebot.callback_data import CallbackData
from telebot.types import Message


from nearest import get_nearest
import texts
from models import User


location_factory = CallbackData("lat", "lng", prefix="location")


def send_welcome(message: Message, bot: TeleBot):
    user = message.from_user

    try:
        db_user, created = User.get_or_create(
            user_id=user.id,
            defaults={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )
    except Exception as e:
        print(e)

    bot.send_message(message.chat.id, texts.START_MSG)


def finder(message: Message, bot: TeleBot):
    loc: Location = message.location
    lat, lng = loc.latitude, loc.longitude

    nearest_office = get_nearest(lat, lng)

    n_lat = float(nearest_office["lat"])
    n_lng = float(nearest_office["lng"])

    n_name = nearest_office["name"]
    n_code = nearest_office["code"]
    n_address = nearest_office["address"]
    n_region = nearest_office["region"]
    n_phone_number = nearest_office["phone_number"]

    s_text = (
        f"<b>Nomi</b>: {n_name}\n"
        f"<b>Po'chta indeksi:</b> <code>{n_code}</code>\n"
        f"<b>Viloyat:</b> {n_region}\n"
        f"<b>Manzil:</b> {n_address}\n"
        f"<b>Telefon raqam:</b> {n_phone_number}\n\n"
        f'🔗 <i>Manba:</i> <a href="uz.post">UzPost</a>'
    )

    callback_data = location_factory.new(lat=n_lat, lng=n_lng)
    keyboard = InlineKeyboardButton("📍 Joylashuv", callback_data=callback_data)

    markup = InlineKeyboardMarkup().add(keyboard)

    bot.send_message(message.chat.id, text=s_text, reply_markup=markup)


def back_callback(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    c_data = location_factory.parse(call.data)

    bot.send_location(
        latitude=c_data["lat"],
        longitude=c_data["lng"],
        chat_id=chat_id,
        reply_to_message_id=message_id,
    )


def echo_all(message: Message, bot: TeleBot):
    bot.reply_to(message, texts.SEND_LOCATION)
