from colecciones.users import insert_users
from colecciones.messages import insert_messages
from colecciones.groups import insert_groups 
from colecciones.files import insert_files
from colecciones.chats import insert_chats
from colecciones.home import create_home_collection
from maintenance import *

def main():
    # update_home()
    insert_users()
    insert_chats()
    insert_groups()
    insert_messages()
    insert_files()
    ensure_user_participation()
    fix_all_collections()
    create_home_collection()

if __name__ == "__main__":
    main()
