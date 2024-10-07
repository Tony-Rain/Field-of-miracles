def get_help_message(func_bool):
	output = ''
	if not func_bool:
		output += 'По команде /start_game запустится новый раунд.\n'
	output += ('Ваша задача угадать слово по буквам, за это можно получать очки.\n'
	           'Чем меньше Вы потратили попыток на угадывание слова, тем больше очков вы получите.\n'
	           'Когда Вы полностью угадаете слово или попытки закончатся,\n'
	           'текущий раунд завершится.Чтоб начать новый раунд снова отправьте команду.\n'
	           'По завершению раудна набранные Вами очки сохранятся,\n'
	           'НО ТОЛЬКО В ТОМ СЛУЧАЕ ЕСЛИ ВЫ НЕ ПРОИГРАЛИ!\n'
	           'Вы можете использовать подсказку отправив команду /hint, это откроет одну закрытую букву.\n'
	           'Однако использовать подсказку можно только ОДИН раз.\n'
	           'Если Вы угадали слово, не использовав подсказку, то получите дополнительно 5 очков.\n'
	           'Также Вы можете попробовать угадать слово целиком,\n'
	           'отправив команду /fully и потом, в другом сообщении, само слово полностью.\n'
	           '(без использования этой команды нельзя будет вводить больше одного символа за раз)\n'
	           'Отправив команду /show_progress, будут отображены ваши очки и ваш рекорд.\n'
	           'Команда /reset_record сбросит Ваш рекорд.\n'
	           'Комада /help отобразит эту инструкцию к игре.\n'
	           'Во время запущенной игры необходимо соблюдать несколько правил:\n'
	           '1.Необходимо вводить только русские буквы.\n'
	           '2.Вводить можно только по одному символу.\n'
	           '2.1.Исключение команды: /hint, /fully, /help, /show_progress.\n'
	           '3.Вводить цифры нельзя.\n'
	           'Комадны /hint, /fully не работают, пока не запущена игра.\n'
	           'Команды /start, /reset_record не работают во время запущенной игры.\n'
	           'Если Вы хотите использовать бота в группах,\n'
	           'то бот будет регеагировать только на сообщения с "/" в начале сообщения\n')
	if not func_bool:
		output += 'Начните новую игру прямо сейчас, введя команду /start_game!'
	return output


def handle_first_time(bot, player, message):
	bot.send_message(message.chat.id, 'Вы начали новый раунд.\n'
	                                  f'Сейчас Ваш очки равны  {player.gameRound.total_points}.\n'
	                                  f'У Вас есть {player.gameRound.tries_count} попыток.\n'
	                                  f'Оставшиеся буквы: {player.gameRound.get_guessed_letters()}\n'
	                                  f'Введите букву:')


def handle_not_in_first_time(bot, player, message):
	output = ""
	output += f'У Вас осталось {player.gameRound.tries_count} попыток.\n'

	if len(player.gameRound.input_letters) != 0:
		player.gameRound.input_letters.sort()
		output += f'Введённые буквы:  ' + ', '.join(str(s) for s in player.gameRound.input_letters) + '.\n'
	if len(player.gameRound.input_fully_words) != 0:
		player.gameRound.input_fully_words.sort()
		output += f'Введённые слова:  ' + ', '.join(str(s) for s in player.gameRound.input_fully_words) + '.\n'

	output += 'Оставшиеся буквы:  ' + ''.join(str(s) for s in player.gameRound.get_guessed_letters()) + '\n'
	output += 'Введите букву:'
	bot.send_message(message.chat.id, output)


def check_word(func_word):
	for elem in func_word:
		if (ord(elem) < 1040 or ord(elem) > 1103) and elem != 'ё':
			return False
		else:
			return True


def change_group_message(message_text: str):
	return message_text[1:].lower()
