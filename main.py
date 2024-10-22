from colecciones.users import insert_users
from colecciones.messages import insert_messages
from colecciones.groups import insert_groups 
from colecciones.files import insert_files
from colecciones.chats import insert_chats
from colecciones.home import create_home_collection

def main():
    create_home_collection()
    """insert_users()
    insert_chats()
    insert_messages()
    insert_groups()
    insert_files()"""

if __name__ == "__main__":
    main()
