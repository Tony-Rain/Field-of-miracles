import os
import sqlite3

old_path = os.getcwd()
dir_path = os.path.join(old_path, 'main_info')  # создание директория
os.mkdir(dir_path)

in_txt_path = os.path.join(dir_path, 'in.txt')
in_txt = open(fr'{in_txt_path}', 'w', encoding="utf8")  # создание списка слов
in_txt.write('засада\nискра\nпортал\nкисель\nроль')

user_id_database_db_path = os.path.join(dir_path, 'user_id_database.db')
connection = sqlite3.connect(user_id_database_db_path)  # создание базы данных и полей в ней
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

token = input('Введите токен бота: ')
print('Введите id аккаунта в телеграмме, на него будут приходить имена пользователей бота.')
admin_id = input('Если эта функция Вам не нужна просто нажмите Enter: ')
if admin_id == '':
	admin_id = None
secrets_py_path = os.path.join(dir_path, 'secrets.py')
secrets_py = open(fr'{secrets_py_path}', 'w', encoding='utf8')  # создание файла secrets и заполнение его
secrets_py.write(
	f"TOKEN = '{token}'\nadmin_id = {admin_id}\n"
	f"path_to_words = r'{in_txt_path}'\npath_to_db = r'{user_id_database_db_path}'\n")
