from datetime import datetime
from typing import Union;

from aiosqlite import connect

from bot.db.dals import ReminderDAL 
from bot.config_reader import config 
from bot.api.schemas import Reminder



async def _add_reminder(
                        user_id: str,
                        description: str, 
                        response_time: datetime
                        ) -> Reminder: 
    async with connect(config.db_url) as db:
        reminder_dal = ReminderDAL(db)
        reminder =  await reminder_dal.add_reminder(user_id=user_id, description=description, response_time=response_time)

        return Reminder(
            **reminder.dict()
        )
    

async def _update_reminder(id: int, user_id: str, updated_reminder_params: dict) -> Union[tuple, None]:
    async with connect(config.db_url) as db:
        reminder_dal = ReminderDAL(db)
        tuple_of_id = await reminder_dal.update_reminder(reminder_id=id, user_id=user_id, **updated_reminder_params)

        return tuple_of_id