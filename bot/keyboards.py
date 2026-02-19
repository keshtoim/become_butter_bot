from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (внизу у юзера)
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🧈 Мой профиль"), KeyboardButton(text="🚀 Следующее задание")],
    [KeyboardButton(text="☕️ Взять отдых")]
], resize_keyboard=True)

# Кнопки под заданием
def get_task_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сделано!", callback_data="task_done")],
        [InlineKeyboardButton(text="❌ Не вышло", callback_data="task_failed")]
    ])