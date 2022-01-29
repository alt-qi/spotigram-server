from psycopg2 import OperationalError
from bottle import route, run, response, request
from utils import *
import telebot
import os

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write(
'''
# Telegram bot token
bot_token = "INSERT YOUR BOT TOKEN HERE"

# Database creditionals 
database = "INSERT DATABASE NAME HERE"
user = "INSERT DATABASE USER NAME HERE",
password = "INSERT DATABASE USER PASSWORD HERE",
port = "INSERT DATABASE PORT HERE"

# Server settings
host = "localhost"
port = 8080
''')
        file.close()
        
    print("I have created a \".env\" file, please fill required fields in it.")
    exit()

try:
    db.init()
    bot = telebot.TeleBot(os.getenv("bot_token"))
except OperationalError:
    print("Failed to connect to database! Please make sure, that database creditionals stored in \".env\" are valid.")

@route('/auth', method="GET")
def auth():
    response.content_type = 'application/json'
    if not "state" in request.query.keys():
        return "Get away."
    elif not db.code_exists(code := request.query["state"]):
        return "Outdated or invalid link. Please create a new one."
    else:
        db.save_spotify_token(user_id := db.get_user_id(code), request.query["state"])
        db.delete_code(code)
        bot.send_message(user_id, "*Your account is successfully linked\.*", "MarkdownV2")
        return "Authentication successful."

run(host=os.getenv("srv_host"), port=os.getenv("srv_port"))