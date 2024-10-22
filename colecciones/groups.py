from config import get_db
from faker import Faker

from utils.data_generator import generate_group_name, select_admins
fake = Faker()

db = get_db()
groups_collection = db['groups']

def insert_groups():
    group_chats = list(db['chats'].find({"isGroup": True}))
    groups = []

    for chat in group_chats:
        members = chat['participants']
        admins = select_admins(members)

        group = {
            'groupId': chat['chatId'],
            'adminsIds': admins,
            'members': members,
            'groupName': generate_group_name(),
            'groupPicture': "https://example.com/group-pic.jpg",
            'createdAt': fake.date_time_this_year()
        }
        groups.append(group)

        if len(groups) == 10000:
            groups_collection.insert_many(groups)
            groups = []

    if groups:
        groups_collection.insert_many(groups)

    print("Se han insertado los grupos correspondientes a los chats correctamente.")
