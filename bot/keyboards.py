from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_kb(is_resting: bool = False):
    # Динамический текст для кнопки задания
    task_text = "🔄 Вернуться к заданию" if is_resting else "🚀 Следующее задание"

    # Кнопка отдыха тоже меняется: если юзер уже отдыхает, предлагаем закончить отдых
    rest_text = "☀️ Закончить отдых" if is_resting else "☕️ Взять отдых"

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🧈 Мой профиль"), KeyboardButton(text=task_text)],
        [KeyboardButton(text=rest_text)]
    ], resize_keyboard=True)


# Кнопки под самим заданием (остаются без изменений)
def get_task_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сделано!", callback_data="task_done")],
        [InlineKeyboardButton(text="❌ Не вышло", callback_data="task_failed")]
    ])