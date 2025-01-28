import sqlite3
import asyncio


def create_database_sync():
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    print('Entered the database')

    print('Database creating function started')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            age TEXT,
            telephone_number TEXT NOT NULL,
            is_confirmed BOOLEAN NOT NULL DEFAULT 0,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    print('Database creating function completed')
    database.commit()
    database.close()
    print('Database committed')


async def create_database():
    await asyncio.to_thread(create_database_sync)
    print('Database creation completed')


asyncio.run(create_database())


database = sqlite3.connect('bot.db')
cursor = database.cursor()