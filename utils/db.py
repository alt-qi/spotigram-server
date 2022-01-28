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
    try:
        cur.execute("CREATE TABLE spotify (user_id INTEGER, code TEXT)")
    except:
        ...
    con.commit()

def code_exists(code: int) -> bool:
    cur.execute("SELECT EXISTS (SELECT * FROM auth WHERE code = %s)", (code,))
    return cur.fetchall()[0][0]

def delete_code(code: int) -> None:
    cur.execute("DELETE FROM auth WHERE code = %s", (code,))
    con.commit()

def get_user_id(code: int) -> int:
    cur.execute("SELECT user_id FROM auth WHERE code = %s", (code,))
    return int(cur.fetchall())