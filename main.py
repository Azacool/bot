import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.reply_to(message, "Hey there!")

@bot.message_handler(commands=['weather'])
def get_weather(message):
    city = message.text[9:]
    data = get_full_data(city)
    
    if data['cod'] != '404':
        temperature = round(data.get("main", {}).get('temp', 0) - 273.15)
        weather_description = data.get("weather", [{}])[0].get('description', 'none')
        location = data.get("name", 'none')
        
        bot.send_message(message.chat.id, f"Current weather in {location}: {temperature}°C, {weather_description}.")
    else:
        bot.send_message(message.chat.id, f"Sorry, could not find information for {city}.")

@bot.message_handler(func=lambda msg: True)
def reply_msg(message):
    if message.text and message.text.startswith('/'):
        bot.send_message(message.chat.id, f"Received command: {message.text}")
    else:
        bot.send_message(message.chat.id, "I apologize, I only understand messages with commands.")



def get_full_data(city):
    url = os.environ.get("WEATHER_API")+city
    response = requests.get(url)
    return response.json()

bot.infinity_polling()
