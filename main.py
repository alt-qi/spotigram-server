from bottle import route, run, response, request
from os import getenv
from utils import *
import telebot

bot = telebot.TeleBot(getenv("bot_token"))

@route('/auth', method="GET")
def auth():
    response.content_type = 'application/json'
    if not "state" in request.query.keys():
        return "Get away."
    elif not db.code_exists(request.query["state"]):
        return "Outdated or invalid link. Please create a new one."
    else:
        bot.send_message(db.get_user_id(request.query["state"]), "**Authentication successsful!**", "MarkdownV2")
        db.delete_code(request.query["state"])
        return "Authentication successful."

run(host='localhost', port=8080, debug=True)