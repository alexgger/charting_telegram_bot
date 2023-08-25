import matplotlib.pyplot as chart
import numpy as np
import numexpr as ne
import telebot
import time
import os

import matplotlib
matplotlib.use('agg')

bot = telebot.TeleBot('token-telegram-bot')


@bot.message_handler(commands=['start'])
def first_message(message):
    bot.reply_to(message, 'Привет! Это твой новый помощник, который по твоему запросу построит необходимый двухмерный график :)\n\nОтправь мне свою функцию y = (ваше уравнение с X)')


@bot.message_handler(content_types=['text'])
def input_equations(message):
        charting(message)


@bot.message_handler(content_types=['document', 'audio', 'video', 'sticker', 'voice', 'location', 'contact', 'photo', 'video_note'])
def handle_docs_audio(message):
    bot.reply_to(message, 'Бот не работает с этим типом данных!')


def charting(message):
    try:
            x = np.arange(-5, 5, 0.2)
            y = ne.evaluate(str(message.text))

            bot.reply_to(message, 'Вы ввели след. уравнение: y = ' + message.text)

            chart.xlabel('Ось х')  # Подпись для оси х
            chart.ylabel('Ось y')  # Подпись для оси y
            chart.title('График y = {}'.format(message.text))  # Название
            chart.plot(x, y)

            chart.autoscale()

            ax = chart.gca()

            # plot X - axis
            ax.axhline(y=0, color='k')

            # plot Y - axis
            ax.axvline(x=0, color='k')

            ax.grid(color='g', linestyle='-', linewidth=0.6)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            namefile = 'GC-{}.png'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
            chart.savefig(namefile, dpi=300)
            bot.send_photo(message.chat.id, photo=open(namefile, 'rb'))

            if os.path.isfile(namefile):
                    os.remove(namefile)

            chart.clf()
    except:
        bot.reply_to(message, 'Я не могу построить график этого уравнения.\nПример: x**2+2*x+7+x/2')


bot.infinity_polling()