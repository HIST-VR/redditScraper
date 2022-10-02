import json
import os.path
from datetime import datetime

from googletrans import Translator

import tokens
import telebot

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
    # if time before previous scape less than an hour -> don't scrape again
    if os.path.isfile(('hot_posts_' + sub + '.json')) == False or (
            int(os.path.getmtime(('hot_posts_' + sub + '.json')) + set_hour) < int(current_datetime.timestamp())):
        posts = []
        chosen_subreddit = reddit.subreddit(sub)
        for post in chosen_subreddit.hot(limit=amount):
            title = translate_title(post.title, 'ru').text
            # score = post.score
            url = post.url
            posts.append([title, url])

        with open(('hot_posts_' + sub + '.json'), 'w', encoding='utf8') as jsonFile:
            json.dump(posts, jsonFile, ensure_ascii=False)
        # print(posts)
        return ('hot_posts_' + sub + '.json')

    else:
        return ('hot_posts_' + sub + '.json')


# scrape_reddit('History', 3)

#                      --------------------------BOTING--------------------------



@tg_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Start":
    # Keyboard setup
        keyboard = telebot.types.InlineKeyboardMarkup()
        # Buttons setup
        butt_sub1 = telebot.types.InlineKeyboardButton(text="HistoryPorn", callback_data="HistoryPorn")
        keyboard.add(butt_sub1)
        butt_sub2 = telebot.types.InlineKeyboardButton(text="EarthPorn", callback_data="EarthPorn")
        keyboard.add(butt_sub2)
        butt_sub3 = telebot.types.InlineKeyboardButton(text="Architecture", callback_data="architecture")
        keyboard.add(butt_sub3)
        butt_sub4 = telebot.types.InlineKeyboardButton(text="Tattoos", callback_data="tattoos")
        keyboard.add(butt_sub4)
        butt_sub5 = telebot.types.InlineKeyboardButton(text="FoodPorn", callback_data="FoodPorn")
        keyboard.add(butt_sub5)
        butt_back = telebot.types.InlineKeyboardButton(text="<-", callback_data="GoBack")
        keyboard.add(butt_back)
        tg_bot.send_message(message.from_user.id, text='Choose subreddit', reply_markup=keyboard)

    if message.text == "HistoryPorn":
        print('Someone used it!', datetime.now())
        scrape_reddit('HistoryPorn', 3)
        f = open('hot_posts.json', 'r', encoding='utf8')
        data = json.loads(f.read())
        for line in data:
            #final_message = line[0] + '\n' + line[1]
            #tg_bot.send_message(message.from_user.id, final_message)
            tg_bot.send_photo(message.from_user.id, caption= line[0], photo=line[1])

    elif message.text == "/help":
        tg_bot.send_message(message.from_user.id, "Напиши Start или HistoryPorn")

    else:
        tg_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# Keyboard setup
keyboard = telebot.types.InlineKeyboardMarkup()
# Buttons setup
butt_sub1 = telebot.types.InlineKeyboardButton(text="HistoryPorn", callback_data="HistoryPorn")
keyboard.add(butt_sub1)
butt_sub2 = telebot.types.InlineKeyboardButton(text="EarthPorn", callback_data="EarthPorn")
keyboard.add(butt_sub2)
butt_sub3 = telebot.types.InlineKeyboardButton(text="Architecture", callback_data="architecture")
keyboard.add(butt_sub3)
butt_sub4 = telebot.types.InlineKeyboardButton(text="Tattoos", callback_data="tattoos")
keyboard.add(butt_sub4)
butt_sub5 = telebot.types.InlineKeyboardButton(text="FoodPorn", callback_data="FoodPorn")
keyboard.add(butt_sub5)
butt_back = telebot.types.InlineKeyboardButton(text="<-", callback_data="GoBack")
keyboard.add(butt_back)


# Buttons handler
@tg_bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    #
    sub = call.data
    scrape_reddit(sub, 5)
    f = open('hot_posts_' + sub + '.json', 'r', encoding='utf8')
    data = json.loads(f.read())
    for line in data:
        tg_bot.send_photo(call.message.chat.id, caption=line[0], photo=line[1])

    #if call.data == "HistoryPorn":



    # Отправляем текст в Телеграм
    #tg_bot.send_message(call.message.chat.id, msg)

# def send_posts(sub):
#     scrape_reddit(sub, 5)
#     f = open('hot_posts_' + sub + '.json', 'r', encoding='utf8')
#     data = json.loads(f.read())
#     for line in data:
#         tg_bot.send_photo(call, caption=line[0], photo=line[1])



tg_bot.polling(none_stop=True, interval=0)
