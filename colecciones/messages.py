from faker import Faker
from config import get_db
import random
from utils.data_generator import select_message_type, generate_content, select_message_status

fake = Faker()
db = get_db()
messages_collection = db['messages']

def insert_messages(batch_size=80000, total=8000000):
    chats = list(db['chats'].find())
    users = set()
    messages = []

    # Crear un diccionario para mapear usuarios a los chats en los que participan
    user_chat_map = {}
    for chat in chats:
        for participant in chat['participants']:
            if participant not in user_chat_map:
                user_chat_map[participant] = []
            user_chat_map[participant].append(chat)

    # Asegurar que cada usuario mande al menos un mensaje
    for user, user_chats in user_chat_map.items():
        chat = random.choice(user_chats)
        message_type = select_message_type()
        content = generate_content(message_type)
        status = select_message_status()

        message = {
            'messageId': f'msg{len(messages) + 1}',
            'chatId': chat['chatId'],
            'senderId': user,
            'messageType': message_type,
            'content': content,
            'timestamp': fake.date_time_this_year(),
            'status': status
        }
        messages.append(message)

        # Agregar el usuario al conjunto para asegurarnos de que no se repita
        users.add(user)

        if len(messages) == batch_size:
            messages_collection.insert_many(messages)
            messages = []

    # Generar mensajes aleatorios hasta alcanzar el total deseado
    remaining_messages = total - len(messages)
    for i in range(remaining_messages):
        chat = random.choice(chats)
        sender_id = random.choice(chat['participants'])
        message_type = select_message_type()
        content = generate_content(message_type)
        status = select_message_status()

        message = {
            'messageId': f'msg{len(messages) + 1}',
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
