from config import get_db
from utils.data_generator import get_file_type

db = get_db()
files_collection = db['files']

def insert_files():
    messages_with_files = list(db['messages'].find({
        "messageType": {"$in": ["imagen", "video", "audio", "archivo"]}
    }))
    files = []

    for index, message in enumerate(messages_with_files):
        file_type = get_file_type(message['messageType'])

        if file_type:
            file = {
                'fileId': f'file{index + 1}',
                'chatId': message['chatId'],
                'messageId': message['messageId'],
                'fileType': file_type,
                'uploadedAt': message['timestamp']
            }
            files.append(file)

        if len(files) == 10000:
            files_collection.insert_many(files)
            files = []

    if files:
        files_collection.insert_many(files)

    print("Se han insertado todos los archivos correspondientes a los mensajes con archivos.")
