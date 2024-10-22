from pymongo import MongoClient

def get_db():
    # Configura tu URI con las credenciales y la base de datos de autenticación
    client = MongoClient('mongodb://root:root@localhost:27017/?authSource=admin')
    db = client['whatsappDB']
    return db
