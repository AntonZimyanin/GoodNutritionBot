# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.types import KeyboardButton
# from aiogram.types import InlineKeyboardButton
# from aiogram.types import InlineKeyboardMarkup
# def create_gender_keyboard() -> InlineKeyboardMarkup:
#     '''
#     create a keyboard with two buttons: male and famale
#     return: ReplyKeyboardMarkup
#     '''
#     kb = InlineKeyboardMarkup()
#     wordcount_buttons = [
#         InlineKeyboardButton(text="male", callback_data="male"),
#         InlineKeyboardButton(text="famale", callback_data="famale"),
#         ]
#     return kb.add(*wordcount_buttons)
# def create_activity_level_keyboard() -> ReplyKeyboardMarkup:
#     '''
#     create a keyboard with 5 buttons
#     return: ReplyKeyboardMarkup
#     '''
#     kb = []
#     for number in range(1, 6):
#         kb.append([KeyboardButton(text=number)])
#     return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
# def start_keyboard(update=True) -> ReplyKeyboardMarkup:
#     kb = InlineKeyboardMarkup()
#     if not update:
#         kb.add(InlineKeyboardButton(text="register", callback_data="m/registerale"))
#     else:
#         kb.add(InlineKeyboardButton(text="update", callback_data="/update"))
#     return kb
