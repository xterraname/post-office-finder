import texts
import logging
from telebot.types import (
    Location,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)
from telebot import TeleBot
from telebot.callback_data import CallbackData

from models import User
from nearest import get_nearest

# Create a callback data factory for location data with a specified prefix.
location_factory = CallbackData("lat", "lng", prefix="location")


def send_welcome(message: Message, bot: TeleBot):
    """
    Handle the /start and /help commands by creating or retrieving a user
    and sending a welcome message.

    Args:
        message (Message): The incoming message containing the command.
        bot (TeleBot): The instance of the TeleBot.
    """
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

        if created:
            logging.info(f"New user: {db_user.user_id}")
    except Exception as e:
        logging.error(f"Error creating or retrieving user: {e}")

    bot.send_message(message.chat.id, texts.START_MSG)


def finder(message: Message, bot: TeleBot):
    """
    Handle location messages by finding the nearest office, formatting its details,
    and sending the information along with an inline button that contains a callback.

    Args:
        message (Message): The incoming message that contains the location.
        bot (TeleBot): The instance of the TeleBot.
    """
    loc: Location = message.location
    lat, lng = loc.latitude, loc.longitude

    nearest_office = get_nearest(lat, lng)

    # Parse and convert coordinates of the nearest office
    n_lat = float(nearest_office["lat"])
    n_lng = float(nearest_office["lng"])

    # Create a formatted text message with office details
    s_text = (
        f"<b>Nomi</b>: {nearest_office['name']}\n"
        f"<b>Po'chta indeksi:</b> <code>{nearest_office['code']}</code>\n"
        f"<b>Viloyat:</b> {nearest_office['region']}\n"
        f"<b>Manzil:</b> {nearest_office['address']}\n"
        f"<b>Telefon raqam:</b> {nearest_office['phone_number']}\n\n"
        '🔗 <i>Manba:</i> <a href="uz.post">UzPost</a>'
    )

    # Generate callback data using the nearest office's coordinates
    callback_data = location_factory.new(lat=n_lat, lng=n_lng)
    # Create an inline keyboard button for sending the location
    button = InlineKeyboardButton("📍 Joylashuv", callback_data=callback_data)
    markup = InlineKeyboardMarkup().add(button)

    bot.send_message(message.chat.id, text=s_text, reply_markup=markup)


def back_callback(call: CallbackQuery, bot: TeleBot):
    """
    Handle the callback query by parsing the callback data and sending the location
    back to the user.

    Args:
        call (CallbackQuery): The callback query containing location data.
        bot (TeleBot): The instance of the TeleBot.
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Parse the callback data to extract latitude and longitude values
    data = location_factory.parse(call.data)

    bot.send_location(
        chat_id=chat_id,
        latitude=data["lat"],
        longitude=data["lng"],
        reply_to_message_id=message_id,
    )


def echo_all(message: Message, bot: TeleBot):
    """
    Respond to any message that does not match a specific handler
    by prompting the user to send a location.

    Args:
        message (Message): The incoming message.
        bot (TeleBot): The instance of the TeleBot.
    """
    bot.reply_to(message, texts.SEND_LOCATION)
