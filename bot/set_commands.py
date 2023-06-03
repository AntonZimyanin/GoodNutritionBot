from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Beginning of work"),
        BotCommand(command="/addmeal", description="add food"),
        BotCommand(command="/dailylog", description="daily report"),
        BotCommand(command="/exercises", description="exercises"),
        BotCommand(command="/exercise_plan", description="exercise plan"),
        BotCommand(command="/set_reminder", description="set a reminder"),
        BotCommand(command="/my_reminders", description="reminder list"),
    ]

    await bot.set_my_commands(commands)
