from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db.crud import add_user
from bot.db.pydantic_models import User
from bot.patterns import ACTIVITY_LEVEL_LIST
from bot.patterns import DIGIT_MATCH_PATTERN
from bot.patterns import GENDER_LIST
from bot.state import RegForm


reg_router = Router(name="register-router")


@reg_router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(RegForm.weight)
    await message.reply("Please enter your weight in kg:")


@reg_router.message(RegForm.weight, F.text.regexp(DIGIT_MATCH_PATTERN))
async def enter_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(RegForm.height)
    await message.reply("Thanks! Now enter your height in cm:")


@reg_router.message(RegForm.weight)
async def enter_incorrect_weight(message: Message):
    await message.reply("Please, enter correct weight")


@reg_router.message(RegForm.height, F.text.regexp(DIGIT_MATCH_PATTERN))
async def enter_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(RegForm.age)
    await message.reply("Got it! Now enter your age:")


@reg_router.message(RegForm.height)
async def enter_incorrect_height(message: Message):
    await message.reply("Please, enter correct height (in cm)")


@reg_router.message(RegForm.age, F.text.regexp(DIGIT_MATCH_PATTERN))
async def enter_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(RegForm.gender)

    await message.reply("Please enter your gender (male/female):")


@reg_router.message(RegForm.age)
async def enter_incorrect_age(message: Message):
    await message.reply("Please, enter correct age")


@reg_router.message(RegForm.gender, F.text.lower().in_(GENDER_LIST))
async def enter_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(RegForm.activity_level)
    await message.reply(
        """What is your activity level?\n
1 - Sedentary (little or no exercise)\n
2 - Lightly active (light exercise or sports 1-3 days a week)\n
3 - Moderately active (moderate exercise or sports 3-5 days a week)\n
4 - Very active (hard exercise or sports 6-7 days a week)\n
5 - Super active (very hard exercise or sports, physical job or training twice a day)"""
    )


@reg_router.message(RegForm.gender)
async def enter_incorrect_gender(message: Message):
    await message.reply("Please, enter correct gender")


@reg_router.message(RegForm.activity_level, F.text.in_(ACTIVITY_LEVEL_LIST))
async def enter_activity_level(message: Message, state: FSMContext):
    user_info = await state.get_data()

    user = User(
        chat_id=message.from_user.id,
        weight=user_info.get("weight"),
        height=user_info.get("height"),
        age=user_info.get("age"),
        gender=user_info.get("gender").lower(),
        activity_level=message.text,
    )

    await add_user(user)
    await state.clear()
    await message.reply("To calculate the amount you need daily press /get_calories")


@reg_router.message(RegForm.activity_level)
async def enter_incorrect_activity_level(message: Message):
    await message.reply("Please, enter correct activity level")
