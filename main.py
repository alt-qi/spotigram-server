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

# Spotify app settings
spotify_client_id = "INSERT YOUR SPOTIFY APP CLIENT ID HERE"
spotify_client_secret = "INSERT YOUR SPOTIFY APP CLIENT SECRET HERE"

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
    if "error" in request.query.keys():
        return "Authorization aborted by user."
    elif not "state" in request.query.keys():
        return "Get away."
    elif not db.auth_code_exists(auth_code := request.query["state"]) or not "code" in request.query.keys():
        return "Outdated or invalid link. Please create a new one."
    else:
        db.save_spotify_token(user_id := db.get_user_id(auth_code), token := spotify.get_token(request.query["code"]))
        db.delete_auth_code(auth_code)
        bot.send_message(user_id, f"*Your account is successfully linked\.*", "MarkdownV2")
        return "Authentication successful."

run(host=os.getenv("srv_host"), port=os.getenv("srv_port"))