from aiogram.utils.keyboard import ReplyKeyboardBuilder


builder = ReplyKeyboardBuilder()

for btn in ["/model", "/help"]:
    builder.button(text=btn)

start_kb = builder.as_markup(resize_keyboard=True)
