import json
import os.path

import re

from googletrans import Translator
from telebot import *

import tokens

#  set time
current_datetime = datetime.now()
set_day = 86400
set_hour = 3600
set_minute = 60

#  reddit token
reddit = tokens.reddit

#  telegram token
tg_bot = tokens.tg_bot

#                     ----------------------TRANSLATING----------------------
translator = Translator()


def translate_title(title, language):
    return translator.translate(title, language)


#                     ------------------------SCRAPING------------------------
# get posts information
def scrape_reddit(sub, amount):
    current_datetime = datetime.now()
    # if time before previous scape less than an hour -> don't scrape again
    if os.path.isfile(('hot_posts_' + sub + '.json')) == False or (
            int(os.path.getmtime(('hot_posts_' + sub + '.json')) + set_hour) < int(current_datetime.timestamp())):
        posts = []
        chosen_subreddit = reddit.subreddit(sub)
        for post in chosen_subreddit.hot(limit=amount):

            title = (translate_title(post.title, 'ru').text)

            # get rid of bracketed resolution if it's present, needs optimising
            if title[-1] == "]":
                title = re.sub(r"\[.*?]", "", title) # strip the resolution

            # score = post.score
            url = post.url
            if (url.find('.jpg') != -1) or (url.find('.png') != -1):
                posts.append([title, url])
            else:
                print("Wrong format in", sub)

        with open(('hot_posts_' + sub + '.json'), 'w', encoding='utf8') as jsonFile:
            json.dump(posts, jsonFile, ensure_ascii=False)
        # print(posts)
        return ('hot_posts_' + sub + '.json')

    else:
        return ('hot_posts_' + sub + '.json')


# scrape_reddit('History', 3)

#                      --------------------------BOTING--------------------------
# post creation as well as scrape calling
def send_posts(message, sub):
    print("Someone sent a message:", sub, "at:", datetime.now())  # send feedback on messages

    scrape_reddit(sub, 8)
    f = open('hot_posts_' + sub + '.json', 'r', encoding='utf8')
    data = json.loads(f.read())
    for line in data:
        try:
            tg_bot.send_photo(message.from_user.id, caption=line[0], photo=line[1])
        except:
            print("Exception sending a message in", sub)
            pass


@tg_bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("HistoryPorn")
    button2 = types.KeyboardButton("EarthPorn")
    button3 = types.KeyboardButton("Architecture")
    button4 = types.KeyboardButton("FoodPorn")
    button5 = types.KeyboardButton("Pics")
    button6 = types.KeyboardButton("aiArt")
    markup.add(button1, button2, button3, button4, button5, button6)

    tg_bot.send_message(message.chat.id,
                        "Добро пожаловать, в Reddit Scraper.".format(
                            message.from_user, tg_bot.get_me()),
                        parse_mode='html', reply_markup=markup)


@tg_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    send_posts(message, message.text)

    if message.text == "/help":
        tg_bot.send_message(message.from_user.id, "/start")
    # else:
    #     tg_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# # Keyboard setup
# keyboard = telebot.types.InlineKeyboardMarkup()
# # Buttons setup
# butt_sub1 = telebot.types.InlineKeyboardButton(text="HistoryPorn", callback_data="HistoryPorn")
# keyboard.add(butt_sub1)
# butt_sub2 = telebot.types.InlineKeyboardButton(text="EarthPorn", callback_data="EarthPorn")
# keyboard.add(butt_sub2)
# butt_sub3 = telebot.types.InlineKeyboardButton(text="Architecture", callback_data="architecture")
# keyboard.add(butt_sub3)
# butt_sub4 = telebot.types.InlineKeyboardButton(text="Tattoos", callback_data="tattoos")
# keyboard.add(butt_sub4)
# butt_sub5 = telebot.types.InlineKeyboardButton(text="FoodPorn", callback_data="FoodPorn")
# keyboard.add(butt_sub5)
# butt_back = telebot.types.InlineKeyboardButton(text="<-", callback_data="GoBack")
# keyboard.add(butt_back)


# Buttons handler
# @tg_bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     #
#     sub = call.data
#     scrape_reddit(sub, 5)
#     f = open('hot_posts_' + sub + '.json', 'r', encoding='utf8')
#     data = json.loads(f.read())
#     for line in data:
#         tg_bot.send_photo(call.message.chat.id, caption=line[0], photo=line[1])
#
#     if call.data == "HistoryPorn":
#
#
#
#     # Отправляем текст в Телеграм
#     # tg_bot.send_message(call.message.chat.id, msg)


tg_bot.polling(none_stop=True, interval=0)
