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

from keyboards import control_kb


from dotenv import load_dotenv
# Берем переменные из окружения
load_dotenv()

engine = create_engine(os.getenv('DB_POSTGRESQL'))  # данные для соединия с сервером

bot = Bot(token=os.getenv('BOT_TOKEN'))

loop = asyncio.new_event_loop()

dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

path = os.getenv('PATH')

class user_data:
    def __init__(self):
        self.dist = {}
    def update(self,user_id, dist):
        if user_id not in self.dist:
            self.dist.update({user_id: {}})
        self.dist[user_id].update(dist)
    def delete(self,user_id):
        if user_id in self.dist:
            self.dist.pop(user_id)

async def cmd_start(message: types.Message):
    df = pd.read_sql(f"SELECT count(*) FROM users WHERE user_id = '{message.from_user.id}'", engine)
    if df.iloc[0, 0] == 0:
        engine.execute(f"INSERT INTO users (user_id, first_name, last_name, username, language_code) VALUES('{message.from_user.id}', '{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.language_code}');")
        engine.execute(f"INSERT INTO raid (user_id, ancient, dark, sacred) VALUES('{message.from_user.id}', '0', '0', '0');")
    await message.answer("Введите количество кристалов", reply_markup=control_kb)
    u_data.delete(message.from_user.id)

async def write_in_db(message: types.Message):
    user_id = message.from_user.id
    if user_id in u_data.dist:
        if 'num' in u_data.dist[user_id] and 'choice' in u_data.dist[user_id]:
            if u_data.dist[user_id]['num'] != 'del':
                num = int(u_data.dist[user_id]['num'])
                df = pd.read_sql(f"SELECT * FROM raid WHERE user_id = '{user_id}';",engine)
                if not df.empty:
                    num += int(df.loc[0, u_data.dist[user_id]['choice']])
                if u_data.dist[user_id]['choice'] == 'sacred':
                    await message.answer(f"Добавил. Осталось примерно {26 - num} Введите количество кристалов", reply_markup=control_kb)
                else:
                    await message.answer(f"Добавил. Осталось примерно {226 - num} Введите количество кристалов", reply_markup=control_kb)
            else:
                num = 0
                await message.answer(f"Счетчик обнулил. Введите количество кристалов...",
                                     reply_markup=control_kb)

            engine.execute(f"UPDATE raid SET {u_data.dist[user_id]['choice']} = '{num}' WHERE user_id = '{user_id}';")
            u_data.delete(user_id)

async def content_type_text(message: types.Message):
    user_id = message.from_user.id
    msg = message.text
    if msg.isnumeric() and msg.isdecimal():
        if user_id not in u_data.dist:
            u_data.update(user_id, {'num': msg})
            await message.answer("Выберите тип кристалов\n🟦 Древний\n🟪 Темный\n🟧 Сакральный\n👇", reply_markup=control_kb)
        else:
            if 'choice' not in u_data.dist[user_id]:
                await message.answer("Выберите тип кристалов\n🟦 Древний\n🟪 Темный\n🟧 Сакральный\n👇", reply_markup=control_kb)
            u_data.update(user_id, {'num': msg})
            await write_in_db(message)
    elif "древн" in msg.lower() or "темн" in msg.lower() or "сакрал" in msg.lower() or "синий" in msg.lower() or "фиол" in msg.lower() or "оранж" in msg.lower():
        choice = 0
        if "древн" in msg.lower() or "синий" in msg.lower():
            choice = 'ancient'
        elif "темн" in msg.lower() or "фиол" in msg.lower():
            choice = 'dark'
        elif "сакрал" in msg.lower() or "оранж" in msg.lower():
            choice = 'sacred'
        if choice != 0:
            if user_id not in u_data.dist:
                u_data.update(user_id, {'choice': choice})
                await message.answer("Введите количество кристалов")
            else:
                if 'num' not in u_data.dist[user_id]:
                    await message.answer("Введите количество кристалов")
                u_data.update(user_id, {'choice': choice})
                await write_in_db(message)
    elif "посмотреть количество" in msg.lower():
        df = pd.read_sql(f"SELECT * FROM raid WHERE user_id = '{user_id}';", engine)
        await message.answer(f"🟦 Древний - всего {df.loc[0, 'ancient']}, осталось {226 - int(df.loc[0, 'ancient'])}\n🟪 Темный - всего {df.loc[0, 'dark']}, осталось {226 - int(df.loc[0, 'dark'])}\n🟧 Сакральный - всего {df.loc[0, 'sacred']}, осталось {26 - int(df.loc[0, 'sacred'])}")
    elif "сбросить счётчик" in msg.lower():
        await message.answer("Поздравляю! Выберите тип кристалов на котором нужно сбросить счетчик.\n🟦🟪🟧 👇", reply_markup=control_kb)
        u_data.update(user_id, {'num': 'del'})
    elif "показать расписание событий" in msg.lower():
        with open(path+"event.jpg","rb") as photo:
            await message.answer_photo(photo=photo)
    elif "показать меткость и скорость кб" in msg.lower():
        with open(path+"clan_boss_speed_and_accuracy.jpg", "rb") as photo:
            await message.answer_photo(photo=photo)
    elif "показать cколько краски надо" in msg.lower():
        with open(path+"potion.jpg","rb") as photo:
            await message.answer_photo(photo=photo)

async def cmd_cancel(message: types.Message):
    user_id = message.from_id
    u_data.delete(user_id)

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("cancel", "Отменить текущее действие и начать все с начала"),
    ])

async def main():
    await set_default_commands(dp)
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(content_type_text, content_types=types.ContentType.TEXT)

    await dp.skip_updates()
    await dp.start_polling()

if __name__ == "__main__":
    u_data = user_data()
    asyncio.run(main())
