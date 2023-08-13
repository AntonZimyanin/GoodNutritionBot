from typing import Union

from aiosqlite import connect

from bot.api.schemas import ShowUser
from bot.db.dals import UserDAL
from bot.config_reader import config
from bot.api.schemas import User


async def _create_new_user(
                            user_id: str,
                            weight: int,
                            height: int,
                            age: int,
                            gender: Gender,
                            activity_level: ActivityLevel
                            ) -> ShowUser: 
    async with connect(config.db_url) as db: 
        user_dal = UserDAL(db)
        user = await user_dal.create_user(
            user_id=user_id,
            weight=weight,
            height=height, 
            age=age,
            gender=gender, 
            activity_level=activity_level
        )

        return ShowUser(
            **user.dict(),
        )


async def _delete_user(user_id: str) -> Union[str, None]:
    async with connect(config.db_url) as db: 
        user_dal = UserDAL(db) 
        deleted_user_id = await user_dal.delete_user( 
            user_id=user_id,
        )

        return deleted_user_id


async def _update_user(
        updated_user_params: dict, 
        user_id: str, 
        ) -> Union[str, None]: 
    async with connect(config.db_url) as db: 
        user_dal = UserDAL(db) 
        update_user_id = await user_dal.update_user(user_id, **updated_user_params)

        return update_user_id
    


async def _get_user_by_id(chat_id: str) -> Union[User, None]: 
    async with connect(config.db_url) as db: 
        user_dal = UserDAL(db) 
        user = await user_dal.get_user_by_id(chat_id)

        return user
        







