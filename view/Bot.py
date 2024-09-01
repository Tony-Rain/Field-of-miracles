import telebot
from main_info.secrets import TOKEN, admin_id

import BotHelpCommand
from repository.Repository import Database

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
	database = Database()
	if database.does_player_exits(message.chat.id):
		if database.get_user(message.chat.id).gameRound.game_started:
			bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
			player = database.get_user(message.chat.id)
			BotHelpCommand.handle_not_in_first_time(bot, player, message)
			return

	bot.send_message(message.chat.id, 'Здравстауйте, Вы запустили игрового бота.\n'
	                                  'Рекомендуем Вам ознакомиться с инструкцией отправив команду /help.')
	if admin_id is not None:
		if message.chat.username is None:
			bot.send_message(admin_id, message.chat.first_name + ' ' + message.chat.last_name + ' запустил(а) бота.')
		else:
			bot.send_message(admin_id, '@' + (message.chat.username) + ' запустил(а) бота.')


@bot.message_handler(commands=['help'])
def handle_help(message):
	# bot.send_message(message.chat.id, BotHelpCommand.get_help_message())
	database = Database()
	if database.does_player_exits(message.chat.id):
		if database.get_user(message.chat.id).gameRound.game_started:
			bot.send_message(message.chat.id, BotHelpCommand.get_help_message(True))
			player = database.get_user(message.chat.id)
			BotHelpCommand.handle_not_in_first_time(bot, player, message)
			return
	bot.send_message(message.chat.id, BotHelpCommand.get_help_message(False))


@bot.message_handler(commands=['start_game'])
def handle_start_game(message):
	database = Database()
	if database.does_player_exits(message.chat.id):
		player = database.get_user(message.chat.id)
		if player.gameRound.game_started:
			bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
			BotHelpCommand.handle_not_in_first_time(bot, player, message)
			return
	else:
		database.create_user(message.chat.id)
		if admin_id is not None:
			if message.chat.username is None:
				bot.send_message(admin_id,
				                 'Зарегистирован новый пользователь под ником' + message.chat.first_name + ' ' + message.chat.last_name)
			else:
				bot.send_message(admin_id,
				                 'Зарегистирован новый пользоветель с usermane ' + '@' + (message.chat.username))
	player = database.get_user(message.chat.id)
	player.gameRound.game_started = True
	BotHelpCommand.handle_first_time(bot, player, message)


@bot.message_handler(commands=['hint'])
def hint_handler(message):
	database = Database()
	if database.does_player_exits(message.chat.id):
		player = database.get_user(message.chat.id)
		if player.gameRound.game_started:
			if not player.gameRound.was_hint_used:
				player.gameRound.hint_func()
				player.gameRound.tries_count -= 1
				player.gameRound.was_hint_used = True
				if BotHelpCommand.win_and_lose_system(bot, player, message):
					return
			else:
				bot.send_message(message.chat.id, 'Вы уже использовали подсказку,\n'
				                                  'её можно использовать только один раз.')
			BotHelpCommand.handle_not_in_first_time(bot, player, message)
			return
	bot.send_message(message.chat.id, 'Начните новую игру, чтоб отправлять буквы и команды.\n'
	                                  'Чтоб начать новый раунд введите команду /start_game.')


@bot.message_handler(
	content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'animation', 'video_note', 'voice',
	               'location', 'contact'])
def handle_game_not_started(message):
	database = Database()
	if database.does_player_exits(message.chat.id):
		player = Database().get_user(message.chat.id)
		if player.gameRound.game_started:
			handle_player_input(message)
		return
	bot.send_message(message.chat.id, 'Начните новую игру, чтоб отправлять буквы и команды.\n'
	                                  'Чтоб начать новый раунд введите команду /start_game.')


def handle_player_input(message):
	player = Database().get_user(message.chat.id)

	if message.text is None:
		bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
	else:
		lowered = message.text.lower()
		if len(lowered) != 1 or (lowered < 'а' or lowered > 'я') and lowered != 'ё':
			bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
		else:
			letter = lowered[0]
			if letter in player.gameRound.input_letters:
				bot.send_message(message.chat.id, 'Вы уже вводили эту букву, попробуйте другую.')
			else:
				if letter in player.gameRound.guessed_word:
					bot.send_message(message.chat.id, 'Вы угадали, эта буква есть в слове.')
				else:
					bot.send_message(message.chat.id, 'Вы не угадали, этой буквы нет в слове.')
				player.gameRound.input_letters.append(letter)
				player.gameRound.tries_count -= 1
				if BotHelpCommand.win_and_lose_system(bot, player, message):
					# if player.gameRound.tries_count == 0 or '*' not in player.gameRound.get_guessed_letters():
					# 	if '*' in player.gameRound.get_guessed_letters():  # система проигрыша
					# 		bot.send_message(message.chat.id,
					# 		                 'Вы потратили все попытки.\n'
					# 		                 'Вы не угадали слово.\n'
					# 		                 f'Задагаданное слово {player.gameRound.guessed_word}.\n'
					# 		                 'Вы проиграли.')
					# 		bot.send_message(message.chat.id, f'Ваш результат: {player.gameRound.total_points}.')
					# 		if player.record < player.gameRound.add_scores():
					# 			bot.send_message(message.chat.id, 'Поздравляем, Вы побили рекорд')
					# 			player.record = player.gameRound.add_scores()
					# 		player.gameRound.total_points = 0
					# 	else:
					# 		output = ''
					# 		if player.gameRound.tries_count == 0:
					# 			output += 'Вы потратили все попытки.\n'
					# 		else:
					# 			len_word = len(player.gameRound.guessed_word)
					# 			output += f'Вы потратили {len_word * 2 - player.gameRound.tries_count} из {len_word * 2} попыток.\n'
					# 		output += f'Загаданное слово: {player.gameRound.guessed_word}.\n'
					# 		output += 'Вы выиграли раунд.\n'
					# 		bot.send_message(message.chat.id, output)
					# 		player.gameRound.add_scores()
					# 		bot.send_message(message.chat.id, f'Ваш результат: {player.gameRound.total_points}.')
					# 	Database().update_user(player)
					# 	return
					return
	BotHelpCommand.handle_not_in_first_time(bot, player, message)


bot.polling()
