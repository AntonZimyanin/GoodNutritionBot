from typing import Union
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

from aiosqlite import Connection

from bot.api.schemas import User, Reminder



#######################
#   Enum Class       #
######################


class Gender(str, Enum):
    male = "male"
    female = "female"
    

class ActivityLevel(str, Enum):
    first = 1
    second = 2
    third =  3
    fourth =  4 
    fifth = 5


#######################
#   Abstract Class    #
######################


class DAL(ABC): 
    '''Abstract Class Data Access Layer'''
    @abstractmethod
    def __init__(self,db: Connection) -> None:
        self.db = db



#######################
#   User Class       #
######################


class UserDAL(DAL): 
    '''Data Access Layer for operating user info'''
    def __init__(self,db: Connection) -> None:
        super(UserDAL, self).__init__(db)


    async def create_user(
            self,
            user_id: str,
            weight: int, 
            height: int, 
            age: int, 
            gender: Gender,
            activity_level: ActivityLevel, 
            is_active: bool = True
            ) -> User:
        query = """ INSERT INTO
                    users (
                        user_id
                        , weight
                        , height
                        , age
                        , gender
                        , activity_level
                        , is_active
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                        """
        params = (
                user_id,
                weight,
                height,
                age,
                gender,
                activity_level,
                is_active,
                )
        async with self.db.execute(query, params):
            await self.db.commit()
            return await self.get_user_by_id(user_id)

        
    async def delete_user(self, user_id: str) -> Union[str, None]: 
        query = f"""
                UPDATE
                    users
                SET is_active = False
                WHERE is_active = True AND user_id = '{user_id}';
                """
        async with self.db.execute(query) as cursor:
            await self.db.commit()
            
            return cursor.lastrowid


    async def update_user(self, user_id: str, **kwargs) -> Union[str, None]: 
        kwargs_items = kwargs.items()
        params_dict = ", ".join(f"{key} = '{val}'" for key, val in kwargs_items)
        query = f'''
            UPDATE users 
            SET {params_dict}
            WHERE username = "{user_id}";
        '''
        async with self.db.execute(query) as cursor: 
            await self.db.commit()
            return cursor.lastrowid
        

    async def get_user_by_id(self, user_id) -> Union[User, None]: 
        query = f'''SELECT * 
                    FROM users
                    WHERE user_id = "{user_id}";
                    '''
        async with self.db.execute(query) as cursor: 
                res = await cursor.fetchone()

                if res is not None:
                    user_keys = User.__fields__.keys()
                    return User(**{key: res[i] for i, key in enumerate(user_keys)})



##########################
#   Reminder Class      #
#########################


class ReminderDAL(DAL): 
    '''Data Acces Layer for operating reminder info'''
    def __init__(self, db: Connection) -> None:
        super(ReminderDAL, self).__init__(db)


    async def add_reminder(
                            self, 
                            user_id: str,
                            description: str, 
                            response_time: datetime,
                           ) -> Reminder: 
        query = """ INSERT INTO
                        reminders (
                            user_id
                            , description
                            , response_time
                            )
                            VALUES (?, ?, ?);
                            """
        params = (user_id, description, response_time)

        async with self.db.execute(query, params) as cursor: 
            await self.db.commit()  
            return await self.get_riminder(
                                            cursor.lastrowid, 
                                            user_id
                                            )      


    async def delete_reminder(self, ): 
        query = f''' '''


        async with self.db.execute(query) as cursor: 
            await self.db.commit()
            return cursor.lastrowid


    async def update_reminder(self, reminder_id: int, user_id: str, **kwargs) -> Union[tuple, None]: 
        kwargs_items = kwargs.items()
        params_dict = ", ".join(f'{key} = {val}' for key, val in kwargs_items)
        query = f''' UPDATE reminder
                    SET {params_dict} 
                    WHERE user_id = '{user_id}'
                    AND 
                    reminder_id = '{reminder_id}';
                    '''
        
        async with self.db.execute(query) as cursor: 
            await self.db.commit()
            return (cursor.lastrowid, user_id)


    async def get_riminder(
                            self, 
                            reminder_id: int, 
                            user_id: str
                            ) -> Union[Reminder, None]: 
        query = f''' SELECT * FROM reminders 
                    WHERE id = "{reminder_id}"
                    AND user_id = "{user_id}"'''
        async with self.db.execute(query) as cursor:
            res = cursor.fetchone()

            if res is not None: 
                reminder_keys = Reminder.__fields__.keys()
                return Reminder(**{ key: res[i] for i, key in enumerate(reminder_keys) })



##########################
#       Meal Class      #
#########################


class MealDAL(DAL): 
    '''Data Acces Layer for operating meal info'''
    def __init__(self, db: Connection) -> None:
        super(MealDAL, self).__init__(db)


    async def add_meal(
                        self,
                        ): 
        pass 


    async def delete_meal(
                        self,
                        ): 
        query = f''' '''


        async with self.db.execute(query) as cursor: 
            await self.db.commit()
            return cursor.lastrowid


    async def update_meal(
                        self,
                        ): 
        query = f''' '''


        async with self.db.execute(query) as cursor: 
            await self.db.commit()
            return cursor.lastrowid


    
    










