from faker import Faker
from config import get_db
import random
from utils.data_generator import select_message_type, generate_content, select_message_status

fake = Faker()
db = get_db()
messages_collection = db['messages']

def insert_messages(batch_size=80000, total=8000000):
    chats = list(db['chats'].find())
    messages = []

    for i in range(total):
        chat = random.choice(chats)
        sender_id = random.choice(chat['participants'])
        message_type = select_message_type()
        content = generate_content(message_type)
        status = select_message_status()

        message = {
            'messageId': f'msg{i + 1}',
            'chatId': chat['chatId'],
            'senderId': sender_id,
            'messageType': message_type,
            'content': content,
            'timestamp': fake.date_time_this_year(),
            'status': status
        }
        messages.append(message)

        if len(messages) == batch_size:
            messages_collection.insert_many(messages)
            messages = []

    if messages:
        messages_collection.insert_many(messages)

    print(f"Se han insertado {total} mensajes correctamente.")
