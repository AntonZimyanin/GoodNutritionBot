from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.count_function import calculate_daily_calories
from bot.count_function import calculate_exercises
from bot.count_function import generate_exercise_plan
from bot.db.crud import get_user
from bot.db.crud import is_user
from bot.db.crud import select_meals


router = Router(name="commands-router")


@router.message(CommandStart())
async def command_start(message: Message):
    user = await is_user(message.from_user.id)
    if user:
        await message.answer(
            """Welcome to the GoodNutritionBot!
Press /update if you want to update the previously entered data""",
        )
    else:
        await message.answer(
            """Welcome to the GoodNutritionBot!
Press /register to register with the GoodNutritionBot service""",
        )


@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(
        """Bot can
Add food to your diet -> Press /addmeal
Provide daily log -> Press /dailylog",
Based on your physical characteristics,
generate a training program -> Press /exercise_plan
Provide recommended exercises -> Press /exercise """
    )


@router.message(Command("exercise_plan"))
async def cdm_exercise_plan(message: Message):
    user = await get_user(message.from_user.id)

    if user is not None:
        daily_calories = calculate_daily_calories(user)
        exercise_plan = generate_exercise_plan(daily_calories)
        await message.answer(exercise_plan)
    else:
        await message.answer(
            "Press /register to register with the GoodNutritionBot service"
        )


@router.message(Command("exercises"))
async def cdm_exercises(message: Message):
    user = await get_user(message.from_user.id)
    if user is not None:
        recommended_exercises = calculate_exercises(user)
        await message.answer(
            "Here are some exercises that may help you reach your weight loss goals:"
        )
        await message.answer(recommended_exercises)
    else:
        await message.answer(
            "Press /register to register with the GoodNutritionBot service"
        )


@router.message(Command("get_characteristics"))
async def cdm_get_characteristics(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(user)


@router.message(Command("get_calories"))
async def cmd_get_calories(message: Message):
    user = await get_user(message.from_user.id)
    daily_calories = calculate_daily_calories(user)

    await message.reply(
        f"""Your daily calorie goal is {daily_calories} calories!
To log a meal, use the /addmeal command."""
    )


@router.message(Command("dailylog"))
async def cmd_dailylog(message: Message):
    """
    meal[0] => name
    meal[1] => calories
    meal[2] => time
    """
    user = await is_user(message.from_user.id)
    if user:
        meals_list = await select_meals(message.from_user.id)
        if meals_list:
            total_calories = sum([meal[1] for meal in meals_list])
            chart_meal = "\n".join(
                [
                    f"{meal[0]}: {meal[1]} calories ({meal[2][-5:]})"
                    for meal in meals_list
                ]
            )
            await message.reply(
                f"Your daily log:\n\n{chart_meal}\n\nTotal calories: {total_calories}"
            )
        else:
            await message.reply(
                """You haven't logged any meals yet!
Use the /addmeal command to log a meal."""
            )
    else:
        await message.answer(
            "Press /register to register with the GoodNutritionBot service"
        )
