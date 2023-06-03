from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db.crud import add_reminder
from bot.db.pydantic_models import Reminder
from bot.state import NewReminder


router = Router(name="reminder-router")


@router.message(Command("set_reminder"))
async def cmd_set_reminder(message: Message, state: FSMContext):
    await state.set_state(NewReminder.description)
    await message.reply("Please enter the reminder text:")


@router.message(NewReminder.description)
async def receive_text(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.reply("Please enter the reminder time (YYYY-MM-DD HH:MM):")
    await state.set_state(NewReminder.response_time)


@router.message(NewReminder.response_time)
async def receive_time(message: Message, state: FSMContext):
    data = await state.get_data()
    reminder_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
    await add_reminder(
        Reminder(
            user_id=message.from_user.id,
            description=data.get("description"),
            response_time=reminder_time,
        )
    )

    await state.clear()
    await message.reply("Reminder set!")


# @router.message(Command("my_reminders"))
# async def cmd_my_reminders(message: Message):
#     '''
#     reminder[0] => chat-id
#     reminder[1] => text
#     reminder[2] => time
#     '''
#     # reminder_list = await select_all(message.from_user.id, "reminders")
#     reminder_list =[]
#     await message.answer("Your reminders:\n")

#     for reminder in reminder_list:
#         await message.answer(f'{reminder[2]} ":" {reminder[1]}\n')
