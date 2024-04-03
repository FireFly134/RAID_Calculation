import asyncio
import os
from typing import Any

from aiogram import Bot

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import text as sql_text

bot = Bot(os.getenv("BOT_TOKEN", ""))
engine = create_engine(os.getenv("DB_POSTGRESQL"))


async def send_message(
    msg: str, chat_id: str, parse_mode: str | None = None
) -> None:
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode=parse_mode)


async def sql(
    sql_text_request: str, params: dict[str, Any] | None = None
) -> bool:
    try:
        # Выполнение SQL - запроса с параметрами
        with engine.connect() as connection:
            connection.execute(sql_text(sql_text_request), parameters=params)
            print(sql_text_request)
            print(params)
            connection.commit()
        return True
    except Exception as err:
        # logging.error(err)
        print(err)
        return False


async def mass_send_message(
    msg: str, resend: bool = False, parse_mode: str | None = None
) -> None:
    answer: bool = True
    if not resend:
        answer = await sql("UPDATE users SET send_msg = 'false';")
    if answer:
        info = pd.read_sql(
            "SELECT user_id FROM users WHERE send_msg = 'false';", con=engine
        )
        for idx, row in info.iterrows():
            try:
                await bot.send_message(
                    chat_id=str(row["user_id"]),
                    text=msg,
                    parse_mode=parse_mode,
                )
                await sql(
                    """UPDATE users SET send_msg = 'true'
                        WHERE user_id = :user_id;""",
                    params={"user_id": int(row["user_id"])},
                )
            except Exception as err:
                print(
                    "Error2: \
Не удалось отправить сообщение пользователю! - "
                    + str(err)
                    + "\n",
                )


def go_main(
    msg: str,
    chat_id: str = "943180118",
    resend: bool = False,
    parse_mode: str | None = None,
) -> None:
    if chat_id == "all":
        asyncio.run(mass_send_message(msg, resend))
    else:
        asyncio.run(send_message(msg, chat_id, parse_mode))


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
