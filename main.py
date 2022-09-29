import json
import os.path
from datetime import datetime

from googletrans import Translator

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
    # if time before previous scape less than an hour -> don't scrape again
    if os.path.isfile('hot_posts.json') == False or (
            int(os.path.getmtime("hot_posts.json") + set_hour) < int(current_datetime.timestamp())):
        posts = []
        chosen_subreddit = reddit.subreddit(sub)
        for post in chosen_subreddit.hot(limit=amount):
            title = translate_title(post.title, 'ru').text
            # score = post.score
            url = post.url
            posts.append([title, url])

        with open('hot_posts.json', 'w', encoding='utf8') as jsonFile:
            json.dump(posts, jsonFile, ensure_ascii=False)
        # print(posts)
        return 'hot_posts.json'

    else:
        return 'hot_posts.json'


# scrape_reddit('History', 3)

#                      --------------------------BOTING--------------------------
@tg_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "HistoryPorn":
        print('Someone used it!', datetime.now())
        scrape_reddit('HistoryPorn', 3)
        f = open('hot_posts.json', 'r', encoding='utf8')
        data = json.loads(f.read())
        for line in data:
            final_message = line[0] + '\n' + line[1]
            tg_bot.send_message(message.from_user.id, final_message)

    elif message.text == "/help":
        tg_bot.send_message(message.from_user.id, "Напиши HistoryPorn")

    else:
        tg_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


tg_bot.polling(none_stop=True, interval=0)
