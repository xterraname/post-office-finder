import telebot
from telebot.types import Location
from decouple import config

from nearest import get_nearest


TOKEN = config("TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "<b>The nearest post office finder bot!</b>", parse_mode="html")


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
	n_phone_number = nearest_office["phone_number"]

	bot.send_location(
			latitude=n_lat,
			longitude=n_lng, 
			chat_id=message.chat.id,
		)
	
	s_text = f"<b>Name</b>: {n_name}\n"\
			 f"<b>Postal code</b>: <code>{n_code}</code>\n"\
			 f"<b>Address</b>: {n_address}\n"\
			 f"<b>Phone number</b>: {n_phone_number}\n"\

	bot.send_message(
		message.chat.id,
		text=s_text,
		parse_mode="html"
	)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "Send your location!")


bot.infinity_polling()