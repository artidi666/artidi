import pyowm
import telebot
import os
import time


owm = pyowm.OWM('871b40aa533b9bf62facc00df3544be8', language='ru') # API с сайта погоды.
bot = telebot.TeleBot('1797191920:AAHkZ5kodmnxgUtQ9qYHaxgAL85GiTaqcb4') # Токен телеграм.



@bot.message_handler(content_types=['text'])
def send_message(message):
    """Send the message to user with the weather"""
    

    if message.text.lower() == "/start" or message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Привет. Хочешь узнать погоду? Просто напиши название своего города." + "\n")
    else:
        
        
        try:
            
            observation = owm.weather_at_place(message.text)
            weather = observation.get_weather()
            temp = weather.get_temperature("celsius")["temp"]
            temp = round(temp)
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), temp, "C", weather.get_detailed_status())

            
            answer = "В городе " + message.text.title() + " сейчас " + weather.get_detailed_status() + "." + "\n"
            answer += "Температура около: " + str(temp) + " С" + "\n\n"
            if temp < -10:
                answer += "Холодно!!! По улице бродят БЕЛЫЕ ХОДОКИ!"
            elif temp < 10:
                answer += "Прохладно, но жить можно!"
            elif temp > 25:
                answer += "Жарко, как в аду!"
            else:
                answer += "Идеальная температура!!!"
        except Exception:
            answer = "Не найден город, попробуйте ввести название снова.\n"
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), 'Error')

        bot.send_message(message.chat.id, answer)  


bot.polling(none_stop=True)