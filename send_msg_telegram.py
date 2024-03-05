import asyncio
import os

from aiogram import Bot

import pandas as pd

from sqlalchemy import create_engine

bot = Bot(os.getenv("BOT_TOKEN", ""))
engine = create_engine(os.getenv("DB_POSTGRESQL"))


async def send_message(msg: str, chat_id: str) -> None:
    await bot.send_message(chat_id=chat_id, text=msg)


async def mass_send_message(msg: str, resend: bool = False) -> None:
    if not resend:
        engine.execute("UPDATE users SET send_msg = 'false';")
    info = pd.read_sql(
        "SELECT user_id FROM users WHERE send_msg = 'false';", engine
    )
    for idx, row in info.iterrows():
        try:
            await bot.send_message(chat_id=str(row["user_id"]), text=msg)
            engine.execute(
                f"""UPDATE users SET send_msg = 'true'
                    WHERE user_id = '{row["user_id"]}';"""
            )
        except Exception as err:
            await bot.send_message(
                chat_id=os.getenv("MY_USER_ID"),
                text="Error2: \
                Не удалось отправить сообщение пользователю! - "
                + str(err)
                + "\n",
            )


def go_main(msg: str, chat_id: str = "943180118") -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if chat_id == "all":
        loop.run_until_complete(mass_send_message(msg))
    else:
        loop.run_until_complete(send_message(msg, chat_id))


if __name__ == "__main__":
    go_main(
        msg="""Привет, я обновился!🥳
Теперь тебе доступен подсчет  ️"Первозданных кристаллов"♦️,  а также могу \
отдельно рассчитывать сколько осталось до гаранта легендарного и мифического \
героя из этих же осколков♦️.
    """
    )
#     go_main(
#         msg="""Привет, я обновился!🥳
# Теперь тебе доступен подсчет "Первозданных кристаллов"♦️,  а также могу
# отдельно рассчитывать сколько осталось до гаранта легендарного и мифического
# героя из этих же осколков♦️.
# """,
#         chat_id="all",
#         resend=True,
#     )
