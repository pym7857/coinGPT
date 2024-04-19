import asyncio
import sqlite3
from datetime import timedelta
import os

from telethon import TelegramClient

api_id = '20585814'
api_hash = '855b204e613f8c0862814c34290bd037'
phone = '+821020497699'
dialog_name = 'GMB LABS'
db_file_path = os.path.join('tests', 'telegram', 'temp.db')
scrap_interval_secs = 60 * 60

client = TelegramClient('session_name', api_id, api_hash)

def init_db():
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        message TEXT,
        created_at DATE
    )
    '''
    c.execute(sql)
    conn.commit()
    conn.close()

def insert_message(message):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    sql = 'INSERT OR IGNORE INTO messages(id, message, created_at) VALUES(?,?,?)'

    created_at = message.date + timedelta(hours=9)
    data = (message.id, message.text, created_at)
    c.execute(sql, data)
    conn.commit()
    conn.close()

async def main():
    init_db()

    if not await client.is_user_authorized():
        await client.start()

    dialogs = await client.get_dialogs()
    target_dialog_id = ''
    for dialog in dialogs:
        if dialog_name == dialog.name:
            target_dialog_id = dialog.id
            break

    target_chat = await client.get_input_entity(target_dialog_id)

    while True:
        messages = await client.get_messages(target_chat.channel_id, 1000)
        for message in messages:
            insert_message(message)
        await asyncio.sleep(scrap_interval_secs)

with client:
    client.loop.run_until_complete(main())