import os
import shutil
import sqlite3

old_path = os.getcwd()
dir_path = os.path.join(old_path, 'main_info')
in_txt_path = os.path.join(dir_path, 'in.txt')
user_id_database_db_path = os.path.join(dir_path, 'user_id_database.db')

print('You started installer of  Field-of-miracles...')
print('1 - Standard installing')
print('2 - Reconfiguration (change only configuration)')
number = int(input('Choose number to continue: '))
while  number != 1 and number != 2:
    print()
    number = int(input('Choose only number 1 or 2: '))
else:
    if number == 1:
        print('You started standard installing Field-of-miracles...')
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        in_txt = open(fr'{in_txt_path}', 'w', encoding="utf8")  # create list of words
        in_txt.write('засада\nискра\nпортал\nкисель\nроль')
        in_txt.close()
        connection = sqlite3.connect(user_id_database_db_path)  # create database and field
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        current_game INTEGER,
        record INTEGER
        )
        ''')
        connection.commit()
        connection.close()
    elif number == 2:
        print('You started reconfigure Field-of-miracles...')
token = input("Enter bot'S API token: ")
print('Enter the telegram account id who will have administrator rights')
admin_id = input("If you don't need this function, just press Enter: ")
if admin_id == '':
    admin_id = [None]
else:
    admin_id = list(map(int, admin_id.split(' ')))
secrets_py_path = os.path.join(dir_path, 'secrets.py')
secrets_py = open(fr'{secrets_py_path}', 'w', encoding='utf8')  # create file secrets and write in it
secrets_py.write(
    f"TOKEN = '{token}'\nadmin_id = {admin_id}\n"
    f"path_to_words = r'{in_txt_path}'\npath_to_db = r'{user_id_database_db_path}'\n")
secrets_py.close()
print('Success!')
