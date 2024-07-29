import telebot
from secrets import TOKEN, user_id
import BotHelpCommand
from repository.Repository import Database

bot = telebot.TeleBot(TOKEN)
user_id = user_id


@bot.message_handler(commands=['start'])
def handle_start(message):
	db = Database()
	if db.does_player_exits(message.chat.id):
		if db.get_user(message.chat.id).gameRound.game_started:
			return

	bot.send_message(
		message.chat.id,
		'Здравстауйте, Вы запустили игрового бота.\n'
		'Рекомендуем Вам ознакомиться с инструкцией отправив команду /help.')

	if message.chat.username is None:
		bot.send_message(user_id, message.chat.first_name + ' ' + message.chat.last_name + ' запустил(а) бота.')
	else:
		bot.send_message(user_id, '@' + (message.chat.username) + ' запустил(а) бота.')


@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.send_message(message.chat.id, BotHelpCommand.get_help_message())
	database = Database()
	if database.does_player_exits(message.chat.id):
		if database.get_user(message.chat.id).gameRound.game_started:
			player = database.get_user(message.chat.id)
			BotHelpCommand.handle_not_in_first_time(bot, player, message)



@bot.message_handler(commands=['start_game'])
def handle_start_game(message):
	database = Database()
	if not database.does_player_exits(message.chat.id):
		database.create_user(message.chat.id)
	player = database.get_user(message.chat.id)
	player.gameRound.game_started = True
	BotHelpCommand.handle_first_time(bot, player, message)


def handle_player_input(message):
	player = Database().get_user(message.chat.id)

	if message.text is None:
		bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
		BotHelpCommand.handle_not_in_first_time(bot, player, message)
		return
	lowered = message.text.lower()
	if len(lowered) != 1 or (lowered < 'А' or lowered > 'я') and lowered != 'ё':
		bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
		BotHelpCommand.handle_not_in_first_time(bot, player, message)
		return
	letter = lowered[0]
	player.gameRound.input_letters.append(letter)
	if '*' in player.gameRound.get_guessed_letters() and player.gameRound.tries_count > 0:
		# bot.send_message(message.chat.id, player.gameRound.get_guessed_letters())
		player.gameRound.tries_count -= 1
		BotHelpCommand.handle_not_in_first_time(bot, player, message)
	else:
		# сисема выигрыша и проигрыша
		bot.send_message(message.chat.id, f'Вы отгадали слово: {player.gameRound.get_guessed_letters()}')
		if player.record < player.gameRound.get_points_in_this_game():
			bot.send_message(message.chat.id, f'Вы побили рекорд')
			player.record = player.gameRound.get_points_in_this_game()

		player.gameRound.add_scores() # брать очки из дазы данных перед каждым раудном
		Database().update_user(player)
		player.gameRound.game_started = False
		player.gameRound.input_letters = []
		return


@bot.message_handler(
	content_types=[
		'text', 'audio', 'document', 'photo', 'sticker', 'video', 'animation', 'video_note', 'voice',
		'location', 'contact', 'pinned_message'])
def handle_game_not_started(message):
	player = Database().get_user(message.chat.id)
	if not player.gameRound.game_started:
		bot.send_message(
			message.chat.id,
			'Начните новую игру, чтоб отправлять буквы и команды.\n'
			'Чтоб начать новый раунд введите команду /start_game.')
	else:
		handle_player_input(message)


bot.polling()
