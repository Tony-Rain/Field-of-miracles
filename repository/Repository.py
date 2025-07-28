import random
import sqlite3
from typing import List

from main_info.secrets import path_to_words, path_to_db


class GameRound:
    def __init__(self, word):
        self.guessed_word = word
        self.input_letters = []
        self.input_fully_words = []
        self.was_hint_used = False
        self.tries_count = len(word) * 2
        self.total_points = 0
        self.right_full_word = False

    def get_points_in_this_game(self):
        points = self.tries_count
        if not self.was_hint_used:
            points += 5
        return points

    def add_scores(self):
        self.total_points += self.get_points_in_this_game()
        return self.total_points

    def get_guessed_letters(self):  # метод, вызывается когда угадана буква
        guessed_letters = self.guessed_word  # если буква в слове не отгадана, то заменяем ее на *
        for letter in guessed_letters:
            if letter not in self.input_letters:
                guessed_letters = guessed_letters.replace(letter, '*')

        return guessed_letters

    def hint_func(self):
        guessed_letters = self.get_guessed_letters()
        not_open_letters = []
        for i in range(len(guessed_letters)):
            if guessed_letters[i] == '*':
                not_open_letters.append(self.guessed_word[i])
        letter = random.choice(not_open_letters)
        self.input_letters.append(letter)


class Player:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.record = 0
        self.gameRound = None

    def __str__(self):
        return f'player {self.chat_id} with points {self.gameRound.total_points} and record {self.record}'


class Database:  # работа с базой данных
    players_cache: List[Player] = []
    players_id: List = []

    def __init__(self):
        with open(path_to_words, encoding="utf8") as f:
            self.words_to_guess = f.read().split('\n')
            if len(self.players_id) == 0:
                self.players_id = self.execute_and_exit(f"Select user_id from Users")

    def registration_new_user(self, user_id: int):
        self.execute_and_exit(f'''INSERT INTO Users VALUES({user_id}, '0', '0')''')
        self.players_id.append(user_id)

    def update_user(self, player: Player):
        points = player.gameRound.total_points
        self.execute_and_exit(f'UPDATE Users SET record = {player.record} WHERE user_id = {player.chat_id}')
        self.execute_and_exit(f'UPDATE Users SET current_game = {points} WHERE user_id = {player.chat_id}')

        for elem in range(len(self.players_cache)):
            if self.players_cache[elem].chat_id == player.chat_id:
                del self.players_cache[elem]
                return

    def does_player_exits(self, user_id: int) -> bool:
        for elem in self.players_id:
            if elem[0] == user_id:
                return True
        return False

    def getting_user_data(self, user_id: int):
        for elem in self.players_cache:
            if elem.chat_id == user_id:
                return elem
        return False

    def adding_new_user_in_cache(self, user_id: int):
        points, record = self.execute_and_exit(f'SELECT current_game, record FROM Users WHERE user_id = {user_id}')[0]
        player = Player(user_id)
        player.record = record
        player.gameRound = GameRound(random.choice(self.words_to_guess))
        print(player.gameRound.guessed_word)
        player.gameRound.total_points = points
        self.players_cache.append(player)
        return player

    def show_progress(self, user_id: int):
        points, record = self.execute_and_exit(f'SELECT current_game, record FROM Users WHERE user_id = {user_id}')[0]
        return points, record

    def reset_record(self, user_id: int):
        self.execute_and_exit(f'UPDATE Users SET record = {0} WHERE user_id = {user_id}')

    @staticmethod
    def execute_and_exit(
            command: str):  # создаёт соединение к базе данных, выполняет команды и закрывает соединение
        connection = Connection(path_to_db)
        result = connection.execute_command(command)
        connection.exit()
        return result


class Connection:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_command(self, command: str):
        self.cursor.execute(command)
        result = [list(x) for x in self.cursor.fetchall()]
        self.connection.commit()
        return result

    def exit(self):
        self.connection.close()
