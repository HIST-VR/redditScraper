import json
import os.path
from datetime import datetime

import praw
import telebot
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
# bruh

#                     ----------------------TRANSLATING----------------------
# print(translator.translate('안녕하세요', dest='ru'))
translator = Translator()


def translate_title(title, language):
    return translator.translate(title, language)


#                     ------------------------SCRAPING------------------------
# get posts information
def scrape_reddit(sub, amount):
    #  if time before previous scape less than an hour -> don't scrape again
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


# scrape_reddit('HistoryPorn', 3)

#                      --------------------------BOTING--------------------------
@tg_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "HistoryPorn":
        scrape_reddit('HistoryPorn', 10)
        f = open('hot_posts.json', 'r', encoding='utf8')
        data = json.loads(f.read())
        for line in data:
            final_message = ''
            for part in line:
                final_message += part
                final_message += '\n'
            tg_bot.send_message(message.from_user.id, final_message)

    elif message.text == "/help":
        tg_bot.send_message(message.from_user.id, "Напиши HistoryPorn")
    else:
        tg_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


tg_bot.polling(none_stop=True, interval=0)

# q = 'bitcoin' #query
# sub = 'CryptoCurrency' #subreddit -- Multiple subreddits can be combined with a +.
# sort = "top"                        #e.g. sub='CryptoCurrency+SatoshiStreetBets'
# limit = 50
#
# top_posts = r.subreddit(sub).search(q, sort=sort, limit=limit) #creating a search tot the subreddit
#
# total_posts = list()
#
# #Iterate over the top_posts, and for each instance, create a dictionary to store
# #the scraped data in an ordered collection. Also, for each instance, append the
# #newly created dictionary into the empty list.
#
# for post in top_posts:
#     print(vars(post)) # print all properties
#     Title = post.title,
#     Score = post.score,
#     Number_Of_Comments = post.num_comments,
#     Publish_Date = post.created,
#     Link = post.permalink,
#     data_set = {"Title":Title[0],"Score":Score[0],   "Number_Of_Comments":Number_Of_Comments[0],"Publish_Date":Publish_Da te[0],"Link":'https://www.reddit.com'+Link[0]}
# total_posts.append(data_set)
#
# # create csv file
# df = pd.DataFrame(total_posts)
# df.to_csv('data.csv', sep=',', index=False)
#
# #create json file
# json_string = json.dumps(total_posts)
# jsonFile = open("data.json", "w")
# jsonFile.write(json_string)
# jsonFile.close()
#
