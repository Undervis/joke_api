import random

from fastapi import FastAPI
import sqlite3

sql = sqlite3.connect("jokes.sqlite3")
cursor = sql.cursor()

cursor.execute("create table if not exists Jokes("
               "id integer primary key autoincrement, title varchar(32), content text)")
sql.commit()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Сборник анекдотов про Штирлица"}


@app.get("/joke/{joke_id}")
async def say_hello(joke_id: int):
    return get_joke(joke_id)


@app.get("/joke")
async def say_hello():
    return get_joke(0)


def get_joke(joke_id=0):
    if joke_id > 0:
        cursor.execute(f"select * from Jokes where id = {joke_id}")
        joke = cursor.fetchone()
        return {"id": joke[0], "title": joke[1], "content": joke[2]}
    else:
        cursor.execute(f"select * from Jokes")
        rand_id = random.randrange(1, len(cursor.fetchall()))
        cursor.execute(f"select * from Jokes where id = {rand_id}")
        joke = cursor.fetchone()
        return {"id": joke[0], "title": joke[1], "content": joke[2]}
