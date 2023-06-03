from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class RegForm(StatesGroup):
    weight = State()
    height = State()
    age = State()
    gender = State()
    activity_level = State()


class AddMeal(StatesGroup):
    meal_name = State()
    meal_calories = State()


class NewReminder(StatesGroup):
    description = State()
    response_time = State()
