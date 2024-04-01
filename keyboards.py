from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# создаем кнопки клавиатуры и пишим заготовочный текст на них
btn1 = KeyboardButton(text="🟦 Древний")
btn2 = KeyboardButton(text="🟪 Темный")
btn3 = KeyboardButton(text="🟧 Сакральный")
btn4 = KeyboardButton(text="🟥 Первозданный")
btn5 = KeyboardButton(text="Посмотреть количество")
btn6 = KeyboardButton(text="Сбросить счётчик(лега пришла)")
btn7 = KeyboardButton(text="Сбросить счётчик(мифик пришел)")
# btn8 = KeyboardButton("Показать расписание событий 2х или 10х")
btn8 = KeyboardButton(text="Показать мою статистику")
btn9 = KeyboardButton(text="Показать меткость и скорость КБ")
btn10 = KeyboardButton(text="Показать cколько краски надо")

keyboard: list[list[KeyboardButton]] = [
    [btn1, btn2, btn3, btn4],
    [btn5, btn6, btn7],
    [btn8, btn9, btn10],
]
control_kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
# # распологаем на клавиатуре наши кнопик
# # control_kb.add(btn1).add(btn2).add(btn3)
# control_kb.row(btn1, btn2, btn3, btn4)
# control_kb.row(btn5, btn6, btn7)
# control_kb.row(btn9, btn10)
