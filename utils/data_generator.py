import random

# Función para seleccionar aleatoriamente el tipo de archivo basado en el tipo de mensaje
def get_file_type(message_type):
    file_types = {
        "imagen": "image",
        "video": "video",
        "audio": "audio",
        "archivo": "file"
    }
    return file_types.get(message_type)

def select_message_type():
    types = ['texto', 'imagen', 'video', 'audio', 'archivo']
    return random.choice(types)

def generate_content(message_type):
    if message_type == 'texto':
        return 'Este es un mensaje de texto simulado'
    elif message_type == 'imagen':
        return 'https://example.com/imagen.jpg'
    elif message_type == 'video':
        return 'https://example.com/video.mp4'
    elif message_type == 'audio':
        return 'https://example.com/audio.mp3'
    elif message_type == 'archivo':
        return 'https://example.com/archivo.pdf'
    else:
        return 'Contenido no disponible'

def select_message_status():
    statuses = ['enviado', 'recibido', 'leído']
    return random.choice(statuses)

def select_admins(members):
    num_admins = random.randint(1, 2)
    return random.sample(members, num_admins)

def generate_group_name():
    group_names = ['Amigos', 'Familia', 'Trabajo', 'Viaje', 'Estudio', 'Proyecto', 'Equipo', 'Vecinos', 'Deportes', 'Música']
    return f"{random.choice(group_names)} {random.randint(1, 100)}"
