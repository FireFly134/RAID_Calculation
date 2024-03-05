# RAID_Calculation
![python-version](https://img.shields.io/badge/python-3.8.7-blue.svg)
![pandas-version](https://img.shields.io/badge/pandas-1.2.4-orange.svg)
![pandas-version](https://img.shields.io/badge/PostgreSQL-2.svg)
Вот ссылочка на бота [RAID_Calculation](https://t.me/RAID_Calculation_bot)

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