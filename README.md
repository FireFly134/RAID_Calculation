# RAID_Calculation
![python-version](https://img.shields.io/badge/python-3.8.7-blue.svg)
![pandas-version](https://img.shields.io/badge/pandas-1.2.4-orange.svg)
![pandas-version](https://img.shields.io/badge/PostgreSQL-2.svg)
Вот ссылочка на бота [RAID_Calculation](https://t.me/RAID_Calculation_bot)

В проекте имеется файл .env отсюда в окружение системы временно помещаются переменные для проекта. Пример:
```shell
BOT_TOKEN="Токен бота"
DB_POSTGRESQL='postgresql://логин:пароль@IP:порт/название базы данных'
PATH='/home/.../raid/'# Тут путь до папки с ботом
```

...на всякий случай...
Необходимые библиотеки:
```shell
pip install pandas==0.25.3
pip install SQLAlchemy==1.3.12
pip install python-dotenv==0.21.1
pip install psycopg2
```
Если возникла проблема с установкой `psycopg2` на сервере, то попробуй это
```shell
pip install psycopg2-binary==2.8.4
```

Добавил файл `requirements.txt` из моего `venv`