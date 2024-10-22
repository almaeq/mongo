from config import get_db
import random

db = get_db()
chats_collection = db['chats']

def select_participants(is_group, total_users):
    if is_group:
        num_participants = random.randint(3, 5)  # Grupos tienen entre 3 y 5 participantes
    else:
        num_participants = 2  # Chats individuales tienen exactamente 2 participantes

    participants = set()
    while len(participants) < num_participants:
        user_id = f"user{random.randint(1, total_users)}"
        participants.add(user_id)

    return list(participants)

def insert_chats(total_chats=100000, total_users=1000000):
    chats = []
    for i in range(total_chats):
        is_group = random.random() < 0.5  # 50% probabilidad de que sea un grupo
        participants = select_participants(is_group, total_users)

        chat = {
            'chatId': f'chat{i + 1}',
            'participants': participants,
            'isGroup': is_group,
            'updatedAt': random_date()
        }
        chats.append(chat)

        if len(chats) == 1000:
            chats_collection.insert_many(chats)
            chats = []

    if chats:
        chats_collection.insert_many(chats)

    print(f"Se han insertado {total_chats} chats correctamente.")

def random_date():
    from faker import Faker
    fake = Faker()
    return fake.date_time_this_year()
