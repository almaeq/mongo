from faker import Faker
from config import get_db
from random import randint
import random

fake = Faker()
db = get_db()
users_collection = db['users']

def generate_user(index):
    return {
        'userId': f'user{index + 1}',
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
        'phone': f"+549261{random.randint(1000000, 9999999)}",
        'profilePicture': "https://example.com/profile-pic.jpg",
        'status': "Available",
        'lastSeen': fake.date_time_this_year()
    }

def insert_users(batch_size=10000, total=1000000):
    users = []
    for i in range(total):
        users.append(generate_user(i))
        if len(users) == batch_size:
            users_collection.insert_many(users)
            users = []

    if users:
        users_collection.insert_many(users)

    print(f"Se han insertado {total} usuarios correctamente.")
