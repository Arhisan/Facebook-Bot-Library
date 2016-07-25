# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

from datetime import datetime
from flask import request

from facebook_messaging.fbbot import FBBot
from facebook_messaging.order import FBOrder
from facebook_messaging.attachment import FBAttachment

import json
myID = "1139030979472570"
token = "EAAEJHb3j43EBAOBCw4b8p1imgCuItxznCXpVqslKwq3D4geJEWZAAkbZCxngTy9jm6335PgsCSV7S5vbZCJLZCRGGKZBB0mPL5mBdznnwQVZA7ejF8vS2tyw2mraoFq3GeEZCch97CYHHfiwYQ4BtK4k6AG7xzCkkwOT7gWFipdgAZDZD"
print(token)
verify_token = "secret"
bot = FBBot(token, verify_token)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    return bot.webhook(request, on_message, on_postback, on_linked, on_unlinked)

def on_linked(sender, login, requestInfo):
    print(sender+" "+ login)

def on_unlinked(sender, requestInfo):
    print(sender+" unlink")

def on_postback(sender, text, requestInfo):
    bot.send_text_message(sender, 'Received postback "{0}"'.format(text))

def on_message(sender, text, requestInfo):
    if(text == "Video"):
        bot.send_message_file_attachment(sender, FBAttachment.File.video, "http://img-9gag-fun.9cache.com/photo/adXLy8N_460sv.mp4")
    elif(text == "Image"):
        bot.send_message_file_attachment(sender, FBAttachment.File.image, "http://img-9gag-fun.9cache.com/photo/aEnxQve_460s_v1.jpg")
    elif(text == "Generic"):
        bot.send_message_generic(sender, "Generic message", "with image and button", "https://scontent.xx.fbcdn.net/t39.3138-6/p128x128/12056981_908479762570256_1493516739_n.jpg", 
                                 [ 
                                     FBAttachment.button_account_unlink()
                                 ])
    elif(text == "Receipt"):
        order = FBOrder(
            "Stephane Crozatier", 
            "125352345", 
            "USD", 
            "Visa", 
            "http://google.com", 
            "1273246346", 
            [
                FBOrder.one_purchase("T-Shirt", "yellow", 1, 5, "USD", "http://cdn01.shopclues.net/images/detailed/19936/yellowtshirt_1434534567.jpg"),
                FBOrder.one_purchase("Baseball cap", "white", 2, 2, "USD", "http://i01.i.aliimg.com/img/pb/630/860/383/383860630_626.jpg")
            ],
            FBOrder.address("1 Hacker Way", "", "Menlo Park", "94025", "CA", "US"),
            FBOrder.price_summary(9, 0, 1, 8),
            [  
                FBOrder.price_one_adjustment("2$ Off coupon", 2)
            ]
        )
        bot.send_message_receipt(sender, order)
    else:
        #bot.send_text_message(sender, str(requestInfo))
        #return 0
        bot.send_text_message(sender, "Hello, What do you want?",[ 
            FBAttachment.quick_reply("Video"), 
            FBAttachment.quick_reply("Image"),
            FBAttachment.quick_reply("Generic"),
            FBAttachment.quick_reply("Receipt")
        ])
