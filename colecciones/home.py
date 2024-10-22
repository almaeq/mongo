from config import get_db

db = get_db()
users_collection = db['users']
chats_collection = db['chats']
groups_collection = db['groups']
home_collection = db['home']

def create_home_collection():
    users = list(users_collection.find())

    for user in users:
        user_id = user['userId']

        # Filtrar los chats en los que participa el usuario
        user_chats = []
        chats = list(chats_collection.find({"participants": user_id}))

        for chat in chats:
            # Encontrar el ID del otro participante si es un chat individual
            other_user_id = next((p for p in chat['participants'] if p != user_id), None)
            chat_name = ""

            if chat['isGroup']:
                # Buscar el nombre del grupo en la colección 'groups'
                group = groups_collection.find_one({"groupId": chat['chatId']})
                chat_name = group['groupName'] if group else f"Grupo {chat['chatId']}"
            else:
                other_user = users_collection.find_one({"userId": other_user_id})
                if other_user:
                    # Concatenar el nombre y apellido del otro participante
                    chat_name = f"{other_user['firstName']} {other_user['lastName']}"
                else:
                    chat_name = "Desconocido"  # Nombre del otro participante o "Desconocido"

            user_chats.append({
                'chatId': chat['chatId'],
                'isGroup': chat['isGroup'],
                'name': chat_name
            })

        # Insertar en la colección Home para el usuario actual
        home_document = {
            'userId': user_id,
            'chats': user_chats
        }
        home_collection.insert_one(home_document)

    print("Colección 'Home' creada correctamente con los nombres de los chats.")

if __name__ == "__main__":
    create_home_collection()
