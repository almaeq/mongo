from config import get_db
from bson import ObjectId
import random
from faker import Faker

fake = Faker()

db = get_db()
users_collection = db['users']
chats_collection = db['chats']
messages_collection = db['messages']
home_collection = db['home']


# Definimos las colecciones y sus campos de ID
collections = {
    #'users': 'userId',
    'chats': 'chatId',
    #'groups': 'groupId',
    #'files': 'fileId',
    'home': 'userId',
    'messages': 'messageId'
}

def fix_duplicates(collection_name, id_field, prefix):
    collection = db[collection_name]

    # Buscar todos los documentos y crear un contador secuencial para los IDs
    documents = list(collection.find().sort(id_field))
    new_ids = set()
    updated_documents = []

    # Generar IDs secuenciales
    for index, doc in enumerate(documents, start=1):
        new_id = f"{prefix}{index}"
        # Verificar si el ID es único y no está repetido
        if doc[id_field] != new_id or doc[id_field] in new_ids:
            print(f"Actualizando {id_field} de {doc[id_field]} a {new_id} en {collection_name}")
            collection.update_one({"_id": doc["_id"]}, {"$set": {id_field: new_id}})
            updated_documents.append(doc["_id"])
        new_ids.add(new_id)

    print(f"Actualización completa en {collection_name}. Total de documentos actualizados: {len(updated_documents)}")

def fix_all_collections():
    for collection_name, id_field in collections.items():
        prefix = id_field[:-2]  # Obtener el prefijo (por ejemplo, "user" de "userId")
        fix_duplicates(collection_name, id_field, prefix)
    print("Corrección de IDs duplicados y secuenciales completa para todas las colecciones.")

# if __name__ == "__main__":
#     fix_all_collections()


def ensure_user_participation():
    users = list(users_collection.find())

    for user in users:
        user_id = user['userId']

        # Verificar si el usuario ya está participando en algún chat
        user_chats = list(chats_collection.find({"participants": user_id}))
        
        if not user_chats:
            # Si el usuario no está en ningún chat, crear uno nuevo con otro usuario aleatorio
            other_user = users_collection.find_one({"userId": {"$ne": user_id}})
            if not other_user:
                print("No hay suficientes usuarios para crear un chat.")
                continue

            other_user_id = other_user['userId']
            new_chat_id = f"chat{ObjectId()}"
            new_chat = {
                "chatId": new_chat_id,
                "participants": [user_id, other_user_id],
                "isGroup": False,  # Crear un chat individual
                "updatedAt": fake.date_time_this_year()
            }
            chats_collection.insert_one(new_chat)
            user_chats.append(new_chat)
            print(f"Se creó un nuevo chat entre el usuario: {user_id} y {other_user_id}")

        # Verificar si el usuario ha enviado al menos un mensaje
        user_messages = list(messages_collection.find({"senderId": user_id}))
        
        if not user_messages:
            # Si no ha enviado mensajes, agregar un mensaje en uno de sus chats existentes
            chat_to_use = user_chats[0]  # Usar el primer chat existente o el recién creado
            new_message_id = f"msg{ObjectId()}"
            new_message = {
                "messageId": new_message_id,
                "chatId": chat_to_use['chatId'],
                "senderId": user_id,
                "messageType": "texto",
                "content": "Este es un mensaje automático para asegurar la participación.",
                "timestamp": fake.date_time_this_year(),
                "status": "enviado"
            }
            messages_collection.insert_one(new_message)
            print(f"Se agregó un mensaje para el usuario: {user_id}")

        # Actualizar o insertar el documento en la colección 'home'
        # update_home(user_id, user_chats)

# # def update_home(user_id, user_chats):
# #     # Construir la lista de chats con nombres adecuados
# #     user_chat_details = []
# #     for chat in user_chats:
# #         if chat['isGroup']:
# #             # Si es un grupo, busca el nombre en la colección de grupos
# #             group = db['groups'].find_one({"groupId": chat['chatId']})
# #             chat_name = group['groupName'] if group else f"Grupo {chat['chatId']}"
# #         else:
# #             # Si es un chat individual, encuentra el otro participante
# #             other_user_id = next((p for p in chat['participants'] if p != user_id), None)
# #             other_user = users_collection.find_one({"userId": other_user_id})
# #             chat_name = f"{other_user['firstName']} {other_user['lastName']}" if other_user else "Desconocido"

# #         user_chat_details.append({
# #             'chatId': chat['chatId'],
# #             'isGroup': chat['isGroup'],
# #             'name': chat_name
# #         })

# #     # Actualizar o insertar el documento en 'home'
# #     home_document = {
# #         'userId': user_id,
# #         'chats': user_chat_details
# #     }
# #     home_collection.update_one(
# #         {"userId": user_id},
# #         {"$set": home_document},
# #         upsert=True  # Esto asegura que se inserte si no existe
# #     )

# # if __name__ == "__main__":
# #     ensure_user_participation()
