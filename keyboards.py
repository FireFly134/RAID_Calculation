from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton("🟦 Древний")
btn2 = KeyboardButton("🟪 Темный")
btn3 = KeyboardButton("🟧 Сакральный")
btn4 = KeyboardButton("Посмотреть количество")
btn5 = KeyboardButton("Сбросить счётчик(лега пришла)")
btn6 = KeyboardButton("Показать расписание событий 2х или 10х")


control_kb = ReplyKeyboardMarkup(resize_keyboard=True)
control_kb.add(btn1).add(btn2).add(btn3)
control_kb.row(btn4, btn5)
control_kb.add(btn6)