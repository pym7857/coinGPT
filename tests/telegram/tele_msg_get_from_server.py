import sqlite3
from datetime import datetime
import os

db_file_path = os.path.join('tests', 'telegram', 'temp.db')

def get_messages_by_date(date):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE date(created_at) = date(?)
        ORDER BY created_at DESC
    ''', (date,))
    messages = cursor.fetchall()
    conn.close()
    return messages

DATE = '2024-03-30'
messages = get_messages_by_date(DATE)
print(messages)
with open(os.path.join('outputs', f'telegram_{DATE}.txt'), 'w') as file:
    file.write(str(messages))