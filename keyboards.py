from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# создаем кнопки клавиатуры и пишим заготовочный текст на них
btn1 = KeyboardButton("🟦 Древний")
btn2 = KeyboardButton("🟪 Темный")
btn3 = KeyboardButton("🟧 Сакральный")
btn4 = KeyboardButton("🟥 Первозданный")
btn5 = KeyboardButton("Посмотреть количество")
btn6 = KeyboardButton("Сбросить счётчик(лега пришла)")
btn7 = KeyboardButton("Сбросить счётчик(мифик пришел)")
btn8 = KeyboardButton("Показать расписание событий 2х или 10х")
btn9 = KeyboardButton("Показать меткость и скорость КБ")
btn10 = KeyboardButton("Показать cколько краски надо")

control_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# распологаем на клавиатуре наши кнопик
# control_kb.add(btn1).add(btn2).add(btn3)
control_kb.row(btn1, btn2, btn3, btn4)
control_kb.row(btn5, btn6, btn7)
control_kb.row(btn8, btn9, btn10)
