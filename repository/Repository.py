import random
import sqlite3
from typing import List


class GameRound:
	def __init__(self, word):  # информация о текущем раунде игрока
		self.game_started = False
		self.guessed_word = word
		self.printed_word = word
		self.input_letters = []
		self.input_fully_words = []
		self.was_hint_used = False
		self.tries_count = len(word) * 2
		self.is_first_time = True
		self.total_points = 0
		self.next_is_right_full_word = False
		self.guessed_letters = ['*'] * len(word)  # массив звездочек, которые заменяются отгаданными буквами

	def get_points_in_this_game(self):
		points = self.tries_count
		# if not self.was_hint_used: временно!!!!!
		# 	points += 5
		return points

	def add_scores(self):
		self.total_points += self.get_points_in_this_game()
		return self.total_points

	def get_guessed_letters(self):  # метод, вызывается когда угаданна буква
		# !!!! не переписать
		letters = self.guessed_word  # если буква в слове не отгадана, то заменяем ее на *
		for letter in letters:
			if letter not in self.input_letters:
				letters = letters.replace(letter, '*')

		return letters


class Player:  # текущая информация об игроке
	def __init__(self, chat_id):
		self.chat_id = chat_id
		self.record = 0
		self.gameRound = None


# def __str__(self):
# 	return f'player {self.chat_id} with points {self.gameRound.points} and record {self.record}'


class Database:  # работа с базой данных
	players_cache: List[Player] = []

	def __init__(self):
		with open('in.txt', encoding="utf8") as f:
			self.words_to_guess = f.read().split('\n')

	def does_player_exits(self, user_id: int) -> bool:  # проверка существования игрока
		result = self.execute_and_exit(f"Select user_id from Users")
		for x in result:
			if x[0] == user_id:
				return True
		return False

	def create_user(self, user_id: int):  # добавление нового игрока в базу данных
		self.execute_and_exit(f'''INSERT INTO Users VALUES({user_id}, '0', '0')''')

	def update_user(self, player: Player):  # изменение показателей игрока
		points = player.gameRound.total_points
		self.execute_and_exit(f'UPDATE Users SET record = {player.record} WHERE user_id = {player.chat_id}')
		self.execute_and_exit(f'UPDATE Users SET current_game = {points} WHERE user_id = {player.chat_id}')

		for x in range(len(self.players_cache)):
			if self.players_cache[x].chat_id == player.chat_id:
				del self.players_cache[x]

	def get_user(self, user_id: int):  # создание нового класса(игрока)
		for p in self.players_cache:
			if p.chat_id == user_id:
				return p

		points, record = self.execute_and_exit(f'SELECT current_game, record FROM Users WHERE user_id = {user_id}')[0]

		player = Player(user_id)
		player.record = record
		player.gameRound = GameRound(random.choice(self.words_to_guess))
		print(player.gameRound.guessed_word)
		assert type(points) is int
		player.gameRound.total_points = points

		self.players_cache.append(player)

		return player

	@staticmethod
	def execute_and_exit(command: str):  # создаёт соединение к базе данных, выполнение команды и закрывает соединение
		c = Connection('user_id_database.db')
		result = c.execute_command(command)
		c.exit()
		return result


class Connection:
	def __init__(self, db_name):  # инициализация полей для работы с базой данных
		self.connection = sqlite3.connect(db_name)
		self.cursor = self.connection.cursor()

	def execute_command(self, command: str):  # выполнение команды для базы данных
		self.cursor.execute(command)
		result = [list(x) for x in self.cursor.fetchall()]
		self.connection.commit()
		return result

	def exit(self):  # закрытие соединения
		self.connection.close()
