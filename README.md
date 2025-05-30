# My TGBot

Телеграм бот написанный полностью на Python. Для взаимодействия с telegram api используется библиотека telebot.
Для синхронного взаимодействия с базой данных используется библиотека sqlite.

Данных бот был создан как проект для изучения построения телеграм ботов, баз данных и всего программирования в целом.

## Работа бота
Данный бот запускает игру в которой игрок должен угадать слово по буквам.

### Начало

Чтоб начать новую игру надо использовать команду`/start_game`.
После ввода этой команды начнётся новый раунд.
У Вас будет ограниченное количество попыток.
Ваша задача угадать слово вводя по одной букве.
При каждом вводе буквы у Вас уменьшиться количество попыток на один.

### Раунды и очки

В этой игре есть система раундов. Каждая игра может состоять из нескольких раундов. 
Если Вы полностью угадали слово не потратив все попытки,
у Вас автоматически начнется новый раунд с новым словом и новыми попытками.
Количество попыток в каждом раунде это длинна угадываемого слово умноженная на 2.
Однако если Вы используете все попытки, но не откроете все буквы в слове игра автоматически закончится.
За каждый победный раунд Вы получаете очки. Они равны количеству неиспользованных попыток.
Очки за каждый победный раунд в рамках одной игры суммируются. Однако если Вы проиграете раунд ваши набранные
очки будут сброшены. Также в игре реализована функционал рекорда очков.

### Дополнительный функционал

* В этой игре помимо ввода по одной букве есть возможность попробовать угадать все слово целиком.
Для этого надо отправить команда `/fully` и следующим сообщением само слово полностью.
* Реализована функция подсказки. Она открывает одну случайную закрытую букву. Однако в одном рауде можно использовать 
подсказку только **один** раз. Также если Вы угадали слово не использовав подсказу Вы дополнительно получите 5 очков за 
раунд. Чтоб использовать подсказу необходимо отправить команду `/hint`.
* Также Вы можете посмотреть текущие очки и личный рекорд использовав команду `/show_progress`.
* Сбросить личный рекорд Вы можете использовав команду `/reset_record`.
* Реализован функционал раннее вводимых букв и слов. Все они будут отображаться рядом с угадываемым словом. Таким образом если Вы 
отправите раннее вводимую букву или слово бот предупредит Вас. (за их ввод ваши попытки не уменьшатся)
* Реализован функционал игры в групповых чатах. Чтоб бот обрабатывал сообщения в группах отправляйте с `/` в начале сообщения.

### Ограничения

1. Игрок не может отправлять любые типы сообщений кроме текстовых.
2. Игрок не может отправлять стрикеры и буквы не русского алфавита.
3. Игрок не может отправлять команды `/start_game`, `/reset_record` и `/start` во время запущенного раунда.
4. Игрок не может отправлять команды `/hint` и `/fully` пока не запущена игра.
5. Игрок не может отправлять больше одной буквы во время запущенного раунда(исключения все команды).
6. Игрок не может отправлять текстовые сообщения пока раунд не запущен(исключения все команды).

### Список команд

1. `/start` - запускает бота
2. `/help` - выводит сокращенную инструкцию к боту
3. `/start_game` - запускает раунд игры
4. `/hint` - открывает одну случайную букву в слове
5. `/fully` - дает возможность угадать слово целиком
6. `/show_progress` - отображает Ваши очки и личный рекорд
7. `/reset_record` - сбрасывает Ваш личный рекорд

## Для разработчиков

### Для локального запуска
Для запуска проекта локально сначала надо запустить скрипт `installer.py`. Введите токен бота и admin_id пользователя в телеграмме.
Скрипт создаст папку `main_info` в директории 
проекта с файлами:
1. `in.txt` - содержит список слов, из которых бот будет случайно выбирать слова для игры.
2. `secrets.py` - содержит 4 переменные: токен телеграм бота, путь до файла `in.txt`, путь до файла базы данных, admin_id.
3. `user_id_database.db` - файл базы данных.

### Устройство базы данных
Файл базы данных (`user_id_database.db`) состоит из 3 полей:
1. `id` - primary key (id игрока в телеграмм)
2. `current_game` - очки игрока
3. `record` - личный рекорд игрока

## Планы на дальнейшее развитие 
1. Улучшить систему кеширования активных игроков.
2. Увеличить функционал для администраторов.
3. Переработать групповой режим.