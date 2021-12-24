import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter



bot = telebot.TeleBot(TOKEN)


           

@bot.message_handler(commands=['start' , 'help'])
def start_help(message: telebot.types.Message):
    text = 'Приветствую Вас в конвертере валют! Для начала работы введите команду в следующем формате (через пробел): \n- <Название валюты, цену которой Вы хотите узнать>  \n- <Название валюты, в которой Вы хотите узнать цену первой валюты> \n- <Количество первой валюты> \n \
Список доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
