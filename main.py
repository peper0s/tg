import gpt
import config
import telebot
import test

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Я бот который поможет тебе спасти нашу планету\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_chat_action(message.chat.id, action='typing')
    gpt_text = gpt.chat(message.text)
    bot.reply_to(message, gpt_text)
    bot.send_chat_action(message.chat.id, action='typing')
    test.create_image(message.text)
    img = open('test.png','rb')
    bot.send_photo(message.chat.id, img )


bot.infinity_polling()