import asyncio
import os
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from get_statistics import get_statistics

from keyboards import control_kb

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import text as sql_text


# данные для соединия с сервером
engine = create_engine(os.getenv("DB_POSTGRESQL"))

TOKEN: str = os.getenv("BOT_TOKEN", "")

dp = Dispatcher()

enter_crys: str = "Введите количество кристалов"


class UserData:
    def __init__(self) -> None:
        self._dict: dict[int, dict[str, str]] = dict()
        return

    @property
    def data(self) -> dict[int, dict[str, str]]:
        return self._dict

    def update(self, user_id: int, data: dict[str, str]) -> None:
        if user_id not in self._dict:
            self._dict.update({user_id: {}})
        self._dict[user_id].update(data)
        return

    def delete(self, user_id: int) -> None:
        if user_id in self._dict:
            self._dict.pop(user_id)
        return


async def sql(
    sql_text_request: str, params: dict[str, Any] | None = None
) -> bool:
    try:
        # Выполнение SQL - запроса с параметрами
        with engine.connect() as connection:
            connection.execute(sql_text(sql_text_request), parameters=params)
            connection.commit()
        return True
    except Exception as err:
        # logging.error(err)
        print(err)
        return False


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if message.from_user is not None:
        user_id: int = int(message.from_user.id)
        df = pd.read_sql(
            "SELECT count(*) FROM users WHERE user_id = %(user_id)s;",
            params={"user_id": user_id},
            con=engine,
        )
        if df.iloc[0, 0] == 0:
            await sql(
                sql_text_request="""
                INSERT INTO users (
                        user_id,
                        first_name,
                        last_name,
                        username,
                        language_code
                ) VALUES(
                        :user_id,
                        :first_name,
                        :last_name,
                        :username,
                        :language_code
                );
                   """,
                params={
                    "user_id": user_id,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "username": message.from_user.username,
                    "language_code": message.from_user.language_code,
                },
            )
            await sql(
                sql_text_request="INSERT INTO raid (user_id) \
                VALUES(:user_id);",
                params={
                    "user_id": message.from_user.id,
                },
            )
        await message.answer(enter_crys, reply_markup=control_kb)
        u_data.delete(user_id)
    return


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message) -> None:
    if message.from_user is not None:
        u_data.delete(int(message.from_user.id))
    return


@dp.message(Command("get_stat"))
async def get_stat(message: types.Message) -> None:
    await message.answer(text="Собираю данные...")
    if message.from_user is not None:
        path_img = get_statistics(int(message.from_user.id))
        photo = FSInputFile(path_img)
        await message.answer_photo(photo=photo, caption="Вот твоя статистика")
    return


async def write_in_db(message: types.Message) -> None:
    if message.from_user is not None:
        user_id: int = int(message.from_user.id)
    if user_id in u_data.data:
        if "num" in u_data.data[user_id] and "choice" in u_data.data[user_id]:
            num: int = 0
            old_num: int = 0
            pristine_mif_num: int = 0
            df: pd.DataFrame = pd.read_sql(
                "SELECT * FROM raid WHERE user_id = %(user_id)s;",
                params={"user_id": user_id},
                con=engine,
            )
            for idx, row in df.iterrows():
                old_num = int(row[u_data.data[user_id]["choice"]])
                pristine_mif_num = int(row["pristine_mif"])
            if u_data.data[user_id]["num"] != "del":
                num = int(u_data.data[user_id]["num"]) + old_num
                if u_data.data[user_id]["choice"] == "sacred":
                    await message.answer(
                        f"Добавил. Осталось примерно {56 - num} \
{enter_crys}",
                        reply_markup=control_kb,
                    )
                elif u_data.data[user_id]["choice"] == "pristine":
                    num_mif = (
                        int(u_data.data[user_id]["num"]) + pristine_mif_num
                    )
                    await message.answer(
                        f"Добавил. Осталось примерно до легендарного \
{180 - num} и до мифического {210 - num_mif}\n{enter_crys}",
                        reply_markup=control_kb,
                    )
                    await sql(
                        sql_text_request="""
                        UPDATE raid SET pristine_mif = :num_mif
                        WHERE user_id = :user_id;
                        """,
                        params={"num_mif": num_mif, "user_id": user_id},
                    )
                else:
                    await message.answer(
                        f"Добавил. Осталось примерно {226 - num} {enter_crys}",
                        reply_markup=control_kb,
                    )
            else:
                await sql(
                    sql_text_request="""
                    INSERT INTO arrival_legend (
                            user_id,
                            quantity,
                            crystal
                    ) VALUES(
                            :user_id,
                            :quantity,
                            :crystal
                    );
                            """,
                    params={
                        "user_id": user_id,
                        "quantity": old_num + 1,
                        "crystal": u_data.data[user_id]["choice"],
                    },
                )
                await message.answer(
                    f"Счетчик обнулил. {enter_crys}...",
                    reply_markup=control_kb,
                )

            await sql(
                sql_text_request=f"""
                UPDATE raid SET {u_data.data[user_id]['choice']} = '{num}'
                WHERE user_id = '{user_id}';
                """
            )
            u_data.delete(user_id)
    return


@dp.message()
async def content_type_text(message: types.Message) -> None:
    chois_type_crystal: str = """
Выберите тип кристалов
🟦 Древний
🟪 Темный
🟧 Сакральный
🟥 Первозданный
👇
"""
    if message.text is not None:
        msg: str = str(message.text)
        if message.from_user is not None:
            user_id: int = int(message.from_user.id)
            if msg.isnumeric() and msg.isdecimal():
                if user_id not in u_data.data:
                    u_data.update(user_id, {"num": msg})
                    await message.answer(
                        chois_type_crystal,
                        reply_markup=control_kb,
                    )
                else:
                    if "choice" not in u_data.data[user_id]:
                        await message.answer(
                            chois_type_crystal,
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
                await message.answer(
                    "Поздравляю!🤩🥳", reply_markup=control_kb
                )
                await sql(
                    sql_text_request="""
                    UPDATE raid SET pristine_mif = '0'
                    WHERE user_id = :user_id;
                    """,
                    params={"user_id": user_id},
                )
            elif "показать мою статистику" == msg.lower():
                await get_stat(message)
            elif "показать расписание событий" == msg.lower():
                photo = FSInputFile("./event.jpg")
                await message.answer_photo(photo=photo)
            elif "показать меткость и скорость кб" == msg.lower():
                photo = FSInputFile("./clan_boss_speed_and_accuracy.jpg")
                await message.answer_photo(photo=photo)
            elif "показать cколько краски надо" == msg.lower():
                photo = FSInputFile("./potion.jpg")
                await message.answer_photo(photo=photo)
            elif "посмотреть количество" == msg.lower():
                df = pd.read_sql(
                    "SELECT * FROM raid WHERE user_id = %(user_id)s;",
                    params={"user_id": user_id},
                    con=engine,
                )
                for idx, row in df.iterrows():
                    ancient: int = int(row["ancient"])
                    dark: int = int(row["dark"])
                    sacred: int = int(row["sacred"])
                    pristine: int = int(row["pristine"])
                    pristine_mif: int = int(row["pristine_mif"])
                    break
                await message.answer(
                    f"""🟦 Древний - всего {ancient}, \
осталось {226 - ancient}\n\
🟪 Темный - всего {dark}, осталось {226 - dark}\
\n🟧 Сакральный - всего {sacred}, \
осталось {56 - sacred}\n🟥 Первозданный:\n\
- для легендарного героя всего {pristine}, \
осталось {180 - pristine}\n\
- для мифического героя всего {pristine_mif}, \
осталось {210 - pristine_mif}"""
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
                    if user_id not in u_data.data:
                        u_data.update(user_id, {"choice": choice})
                        await message.answer(enter_crys)
                    else:
                        if "num" not in u_data.data[user_id]:
                            await message.answer(enter_crys)
                        u_data.update(user_id, {"choice": choice})
                        await write_in_db(message)
    return


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(
                command="cancel",
                description="Отменить текущее действие и начать все с начала",
            ),
        ]
    )
    return


# async def main() -> None:
#     await set_default_commands()
#     dp.register_message_handler(cmd_start, commands="start", state="*")
#     dp.register_message_handler(
#         cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
#     )
#     dp.register_message_handler(
#         content_type_text, content_types=types.ContentType.TEXT
#     )
#
#     await dp.skip_updates()
#     await dp.start_polling()
#     return


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed
    # to all API calls
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_default_commands(bot)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    u_data = UserData()
    asyncio.run(main())
