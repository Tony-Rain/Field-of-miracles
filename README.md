# My TGBot

Это телеграм бот с использованием небольшой базы
данных sqlite. Бот использует две библиотеки: telebot, sqlite3. При желании запустить бота на
своём устройстве, клонируйте репозиторий и запустите файл installer. Он настроит все файлы для работы программы.

## Работа бота

Чтоб начать игру надо запустить раунд командой /start_game.
После ввода этой команды начьнётся новый раунд и Ваша задача угадать слово
вводя по одной букве. Выбор слова происходит из файла со списком слов.
Для каждого игрока в базе данных храняться текущие очки и рекорд.

## Устройство  системы очков

За каждый раунд можно получить очки.
Это сумма неиспользованных попыток плюс
5 очков за угаданное слово без испозования подсказки.
Набранные вами очки сохраняються пока Вы не проиграете.
Как только Вы проиграете, Ваши очки будут сброшены.

## Команды

1. /start - запускает бота
2. /help - выводит инструкцию к боту
3. /start_game - запускает раунд игры
4. /hint - открывает онду рандомную букву в слове

### В будующем планируется команды:

1. /fully - позволяет угадывать слово целиком
2. /show_progress - отбображает текущие очки и рекорд
3. /reset_record - сбрасывает рекорд

## Тесты

1. бот фильтрует любые типы сообщений кроме текстовых
2. бот фильтрует стрикиры и буквы не русского алфавита
3. бот игнорирует команду /start_game во время запущенного раунда
4. бот фильтрует ввод больше одной буквы во время запущенного раунда
5. бот фильтрует ввод букв пока раунд не запущен