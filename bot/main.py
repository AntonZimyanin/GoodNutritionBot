import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.config_reader import config
from bot.config_reader import FSMModeEnum
from bot.db.crud import delete_remider
from bot.db.crud import get_le_current_time
from bot.handlers import commands
from bot.handlers import meal
from bot.handlers import registration
from bot.handlers import reminder
from bot.set_commands import set_commands


async def run_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    if config.fsm_mode == FSMModeEnum.MEMORY:
        storage = MemoryStorage()
    else:
        storage = RedisStorage.from_url(
            url=f"{config.redis.dsn}/{config.redis.fsm_db_id}",
            connection_kwargs={"decode_responses": True},
        )

    dp = Dispatcher(storage=storage)
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    loop = asyncio.get_running_loop()
    try:
        loop.create_task(reminder_loop(bot))

        dp.include_router(registration.reg_router)
        dp.include_router(meal.router)
        dp.include_router(commands.router)
        dp.include_router(reminder.router)

        await set_commands(bot)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.exception(exc_info=e)


# Function to send reminders
async def send_reminder(bot: Bot):
    """
    func get_row_before_current_time return row
    WHERE reminder time <= current time

    row[0] -> chat_id, row[1] - reminders description
    """
    row = await get_le_current_time()

    if row is None:
        return

    await bot.send_message(row[0], f"Reminder: {row[1]}")
    await delete_remider(row[0])


# Start the reminder loop
async def reminder_loop(bot: Bot):
    while True:
        await send_reminder(bot)
        await asyncio.sleep(30)  # Check for reminders every minute
