import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "database": getenv("database"),
    "user": getenv("user"),
    "password": getenv("password"),
    "port": getenv("port")
}
con = psycopg2.connect(**db_config)
cur = con.cursor()

def create_table() -> None:
    try: cur.execute("CREATE TABLE spotify_tokens (user_id INTEGER, token TEXT)")
    except: ...
    con.commit()
    try: cur.execute("CREATE TABLE auth (user_id INTEGER, code TEXT)")
    except: ...
    con.commit()

def code_exists(code: int) -> bool:
    cur.execute("SELECT EXISTS (SELECT * FROM auth WHERE code = %s)", (code,))
    return cur.fetchall()[0][0]

def delete_code(code: int) -> None:
    cur.execute("DELETE FROM auth WHERE code = %s", (code,))
    con.commit()

def get_user_id(code: int) -> int:
    cur.execute("SELECT user_id FROM auth WHERE code = %s", (code,))
    return int(cur.fetchall()[0][0])

def user_token_exists(user_id: int) -> bool:
    cur.execute("SELECT EXISTS (SELECT * FROM spotify_tokens WHERE user_id = %s)", (user_id,))
    return cur.fetchall()[0][0]

def save_spotify_token(user_id: int, auth_token: str) -> None:
    if not user_token_exists(user_id):
        cur.execute("INSERT INTO spotify_tokens VALUES (%s, %s)", (user_id, auth_token))
    else:
        cur.execute("UPDATE spotify_tokens SET token = %s WHERE user_id = %s", (auth_token, user_id))
    con.commit()

def init() -> None:
    create_table()