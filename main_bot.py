# coding=UTF-8
#
#
import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text as sql_text

from keyboards import control_kb

# данные для соединия с сервером
engine = create_engine(os.getenv("DB_POSTGRESQL"))

bot = Bot(token=os.getenv("BOT_TOKEN"))

loop = asyncio.new_event_loop()

dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

enter_crys: str = "Введите количество кристалов"


class user_data:
    def __init__(self):
        self.dist = {}

    def update(self, user_id, dist):
        if user_id not in self.dist:
            self.dist.update({user_id: {}})
        self.dist[user_id].update(dist)

    def delete(self, user_id):
        if user_id in self.dist:
            self.dist.pop(user_id)


async def sql(sql_text_request: str) -> None:
    # Выполнение SQL - запроса с параметрами
    with engine.connect() as connection:
        connection.execute(sql_text(sql_text_request))
        connection.commit()


async def cmd_start(message: types.Message):
    df = pd.read_sql(
        f"""SELECT count(*) FROM users
    WHERE user_id = '{message.from_user.id}'""",
        engine,
    )
    if df.iloc[0, 0] == 0:
        await sql(
            sql_text_request=f"""INSERT INTO users (
                    user_id,
                    first_name,
                    last_name,
                    username,
                    language_code
                    ) VALUES(
                    '{message.from_user.id}',
                    '{message.from_user.first_name}',
                    '{message.from_user.last_name}',
                    '{message.from_user.username}',
                    '{message.from_user.language_code}'
                    );
               """
        )
        await sql(
            sql_text_request=f"""INSERT INTO raid (user_id)
                    VALUES('{message.from_user.id}');"""
        )
    await message.answer(enter_crys, reply_markup=control_kb)
    u_data.delete(message.from_user.id)


async def write_in_db(message: types.Message):
    user_id = message.from_user.id
    if user_id in u_data.dist:
        if "num" in u_data.dist[user_id] and "choice" in u_data.dist[user_id]:
            num: int = 0
            old_num: int = 0
            df: pd.DataFrame = pd.read_sql(
                f"SELECT * FROM raid WHERE user_id = '{user_id}';", engine
            )
            if not df.empty:
                old_num = int(df.loc[0, u_data.dist[user_id]["choice"]])
            if u_data.dist[user_id]["num"] != "del":
                num = int(u_data.dist[user_id]["num"]) + old_num
                if u_data.dist[user_id]["choice"] == "sacred":
                    await message.answer(
                        f"Добавил. Осталось примерно {56 - num} {enter_crys}",
                        reply_markup=control_kb,
                    )
                elif u_data.dist[user_id]["choice"] == "pristine":
                    num_mif = int(u_data.dist[user_id]["num"]) + int(
                        df.loc[0, "pristine_mif"]
                    )
                    await message.answer(
                        f"Добавил. Осталось примерно до легендарного \
{180 - num} и до мифического {210 - num_mif}\n{enter_crys}",
                        reply_markup=control_kb,
                    )
                    await sql(
                        sql_text_request=f"""UPDATE raid
                        SET pristine_mif = '{num_mif}'
                                    WHERE user_id = '{user_id}';"""
                    )
                else:
                    await message.answer(
                        f"Добавил. Осталось примерно {226 - num} {enter_crys}",
                        reply_markup=control_kb,
                    )
            else:
                await sql(
                    sql_text_request=f"""INSERT INTO arrival_legend (
                            user_id,
                            quantity,
                            crystal
                            )
                            VALUES(
                            '{message.from_user.id}',
                            '{old_num}',
                            '{u_data.dist[user_id]['choice']}'
                            );"""
                )
                await message.answer(
                    f"Счетчик обнулил. {enter_crys}...",
                    reply_markup=control_kb,
                )

            await sql(
                sql_text_request=f"""UPDATE raid SET
{u_data.dist[user_id]['choice']} = '{num}'
                        WHERE user_id = '{user_id}';"""
            )
            u_data.delete(user_id)


async def content_type_text(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    if msg.isnumeric() and msg.isdecimal():
        if user_id not in u_data.dist:
            u_data.update(user_id, {"num": msg})
            await message.answer(
                """
Выберите тип кристалов
🟦 Древний
🟪 Темный
🟧 Сакральный
🟥 Первозданный
👇
""",
                reply_markup=control_kb,
            )
        else:
            if "choice" not in u_data.dist[user_id]:
                await message.answer(
                    """
Выберите тип кристалов
🟦 Древний
🟪 Темный
🟧 Сакральный
🟥 Первозданный
👇
                    """,
                    reply_markup=control_kb,
                )
            u_data.update(user_id, {"num": msg})
            await write_in_db(message)
    elif "сбросить счётчик(лега пришла)" == msg.lower():
        await message.answer(
            """
Поздравляю!🥳 Выберите тип кристалов на котором нужно сбросить счетчик.
🟦🟪🟧🟥 👇
""",
            reply_markup=control_kb,
        )
        u_data.update(user_id, {"num": "del"})
    elif "сбросить счётчик(мифик пришел)" == msg.lower():
        await message.answer("Поздравляю!🤩🥳", reply_markup=control_kb)
        await sql(
            sql_text_request=f"""UPDATE raid SET pristine_mif = '0'
                        WHERE user_id = '{user_id}';"""
        )
    elif "показать расписание событий" == msg.lower():
        with open("./event.jpg", "rb") as photo:
            await message.answer_photo(photo=photo)
    elif "показать меткость и скорость кб" == msg.lower():
        with open("./clan_boss_speed_and_accuracy.jpg", "rb") as photo:
            await message.answer_photo(photo=photo)
    elif "показать cколько краски надо" == msg.lower():
        with open("./potion.jpg", "rb") as photo:
            await message.answer_photo(photo=photo)
    elif "посмотреть количество" == msg.lower():
        df = pd.read_sql(
            f"SELECT * FROM raid WHERE user_id = '{user_id}';", engine
        )
        await message.answer(
            f"""🟦 Древний - всего {df.loc[0, 'ancient']}, \
осталось {226 - int(df.loc[0, 'ancient'])}\n\
🟪 Темный - всего {df.loc[0, 'dark']}, осталось {226 - int(df.loc[0, 'dark'])}\
\n🟧 Сакральный - всего {df.loc[0, 'sacred']}, \
осталось {56 - int(df.loc[0, 'sacred'])}\n🟥 Первозданный:\n\
- для легендарного героя всего {df.loc[0, 'pristine']}, \
осталось {180 - int(df.loc[0, 'pristine'])}\n\
- для мифического героя всего {df.loc[0, 'pristine_mif']}, \
осталось {210 - int(df.loc[0, 'pristine_mif'])}"""
        )
    elif (
        "древн" in msg.lower()
        or "темн" in msg.lower()
        or "сакрал" in msg.lower()
        or "первозд" in msg.lower()
        or "синий" in msg.lower()
        or "фиол" in msg.lower()
        or "оранж" in msg.lower()
        or "красный" in msg.lower()
        or "мифи" in msg.lower()
    ):
        choice: str = "0"
        if "древн" in msg.lower() or "синий" in msg.lower():
            choice = "ancient"
        elif "темн" in msg.lower() or "фиол" in msg.lower():
            choice = "dark"
        elif "сакрал" in msg.lower() or "оранж" in msg.lower():
            choice = "sacred"
        elif (
            "первозд" in msg.lower()
            or "красный" in msg.lower()
            or "мифи" in msg.lower()
        ):
            choice = "pristine"
        if choice != "0":
            if user_id not in u_data.dist:
                u_data.update(user_id, {"choice": choice})
                await message.answer(enter_crys)
            else:
                if "num" not in u_data.dist[user_id]:
                    await message.answer(enter_crys)
                u_data.update(user_id, {"choice": choice})
                await write_in_db(message)


async def cmd_cancel(message: types.Message):
    user_id = message.from_id
    u_data.delete(user_id)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand(
                "cancel", "Отменить текущее действие и начать все с начала"
            ),
        ]
    )


async def main():
    await set_default_commands(dp)
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        content_type_text, content_types=types.ContentType.TEXT
    )

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    u_data = user_data()
    asyncio.run(main())
