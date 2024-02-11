import telebot
from telebot.types import (
	Location,
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	CallbackQuery
)
from telebot.callback_data import CallbackData
from decouple import config

from nearest import get_nearest
import texts


TOKEN = config("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="html")

location_factory = CallbackData('lat', 'lng', prefix='location')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, texts.START_MSG)


@bot.message_handler(content_types=["location"])
def finder_handla(message):
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
	
	s_text = f"<b>Nomi</b>: {n_name}\n"\
			 f"<b>Po'chta indeksi:</b> <code>{n_code}</code>\n"\
			 f"<b>Viloyat:</b> {n_region}\n"\
			 f"<b>Manzil:</b> {n_address}\n"\
			 f"<b>Telefon raqam:</b> {n_phone_number}\n\n"\
			 f'🔗 <i>Manba:</i> <a href="uz.post">UzPost</a>'
	
	callback_data = location_factory.new(lat=n_lat, lng=n_lng)
	keyboard = InlineKeyboardButton("📍 Joylashuv", callback_data=callback_data)

	markup = InlineKeyboardMarkup().add(keyboard)

	bot.send_message(
		message.chat.id,
		text=s_text,
		reply_markup=markup
	)

@bot.callback_query_handler(func=lambda c: c.data.startswith(location_factory.prefix))
def back_callback(call: CallbackQuery):
	chat_id=call.message.chat.id
	message_id=call.message.message_id

	c_data = location_factory.parse(call.data)

	bot.send_location(
			latitude=c_data["lat"],
			longitude=c_data["lng"], 
			chat_id=chat_id,
			reply_to_message_id=message_id
	)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, texts.SEND_LOCATION)


bot.infinity_polling()