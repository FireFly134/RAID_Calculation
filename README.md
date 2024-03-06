# RAID_Calculation
![python-version](https://img.shields.io/badge/python-3.11.6-blue.svg)
![python-version](https://img.shields.io/badge/aiogram-2.25.1-blue.svg)
![pandas-version](https://img.shields.io/badge/pandas-2.2.1-orange.svg)
![pandas-version](https://img.shields.io/badge/PostgreSQL-green.svg)
![pandas-version](https://img.shields.io/badge/SQLAlchemy-2.0.28-green.svg)\
Вот ссылочка на бота [RAID_Calculation](https://t.me/RAID_Culatalcion_bot)

В данном проекте используется `pipenv`.\
Все библиотеки находятся в Pipfile.

Для запуска проекта локально нужно в корне проекта создать файл `.env`
отсюда в окружение системы временно помещаются переменные для проекта.\
Пример:
```shell
BOT_TOKEN="Токен бота"
DB_POSTGRESQL='postgresql://логин:пароль@IP:порт/название базы данных'
MY_USER_ID="Ваш user id из телеграмма"
```

Затем запускаем проект. 
У нас есть 2 варианта, использовать просто docker файл или docker-compose.\
1)`docker build -t raid-calculation .`\
2)`docker-compose up --build -d`