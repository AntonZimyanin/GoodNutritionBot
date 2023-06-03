from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db.crud import add_meal
from bot.db.pydantic_models import Meal
from bot.patterns import LETTER_MATCH_PATTERN
from bot.state import AddMeal


router = Router(name="meal-router")


@router.message(Command("addmeal"))
async def cmd_addmeal(message: Message, state: FSMContext):
    await state.set_state(AddMeal.meal_name)
    await message.answer("Please enter the name of the meal:")


@router.message(AddMeal.meal_name, F.text.regexp(LETTER_MATCH_PATTERN))
async def save_meal_name(message: Message, state: FSMContext):
    await state.update_data(meal_name=message.text)
    await message.answer("Enter the number of calories in the meal:")
    await state.set_state(AddMeal.meal_calories)


@router.message(AddMeal.meal_name)
async def incorrect_meal_name(message: Message):
    await message.answer("Please enter the correct name of the meal:")


@router.message(AddMeal.meal_calories, F.text.regexp(r"[0-9]{1,5}"))
async def save_meal_calories(message: Message, state: FSMContext):
    user_meal = await state.get_data()
    meal = Meal(
        user_id=message.from_user.id,
        name=user_meal.get("meal_name"),
        calories=message.text,
    )
    await add_meal(meal)
    await state.clear()
    await message.answer("Meal added to your daily log!")


@router.message(AddMeal.meal_calories)
async def incorrect_meal_calories(message: Message):
    await message.answer("Enter the correct number of calories in the meal:")
