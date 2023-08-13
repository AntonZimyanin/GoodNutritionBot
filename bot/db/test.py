# # from pydantic import BaseModel
# from abc import ABC, abstractmethod

# class Car(ABC):
#     condition = "new"

#     @abstractmethod
#     def __init__(self, model, color, mpg):
#         self.model = model
#         self.color = color
#         self.mpg   = mpg

# class ElectricCar(Car):
#     def __init__(self, battery_type, model, color, mpg):
#         self.battery_type=battery_type
#         super(ElectricCar, self).__init__(model, color, mpg)


# # not_car = Car(1, 1, 1)
# # print(not_car)

# car = ElectricCar('battery', 'ford', 'golden', 10)
# print(car.__dict__)

from datetime import datetime
from typing import Union

from pydantic import BaseModel


#####################
#   User Schemas   #
####################


class BaseUser(BaseModel):
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int




class UserIn(BaseUser):
    pass



class User(BaseModel): 
    user_id: str
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int
    is_active: bool = True



# class User(BaseUser): 


class CreateUser(BaseUser):
    user_id: str


class ShowUser(BaseUser):
    user_id: str
    is_active: bool 




from abc import ABC, abstractmethod


import aiosqlite
from aiosqlite import Connection




# async def create_table(db: Connection): 
#     async with con





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
            user_id,
            weight, 
            height, 
            age, 
            gender,
            activity_level, 
            is_active=True) -> User:
        
        async with self.db.execute(
            """ INSERT INTO
                    users (
                        user_id
                        , weight
                        , height
                        , age
                        , gender
                        , activity_level
                        , is_active
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                        (
                            user_id, 
                            weight, 
                            height, 
                            age, 
                            gender,
                            activity_level,
                            is_active )): 
            await self.db.commit()
            res = await self.get_user(2)
            return res

        
    async def get_user(self, user_id: str) -> User: 
        query =  f'''SELECT * FROM users WHERE user_id = "{user_id}" '''
        async with self.db.execute(query) as cursor: 
                res = await cursor.fetchone()
                print(res)
                return User(**{key: res[i] for i, key in enumerate(User.__fields__.keys())})
    
        
    async def delete_user(user_id: str) -> Union[str, None]: 
        pass 


    async def update_user() -> Union[str, None]: 
        pass


    async def get_user_by_id() -> Union[User, None]: 
        pass


from aiosqlite import connect
import asyncio

async def _create_new_user(body: CreateUser) -> ShowUser: 
    async with connect("mydatabase.db") as db: 
        user_dal = UserDAL(db)
        user = await user_dal.create_user(
            **body.dict(), 
        )


        return ShowUser(
            **user.dict()
        )
    


async def create_users_table():
    conn = await aiosqlite.connect("mydatabase.db")
    cursor = await conn.cursor()
    await cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        weight INTEGER,
        height INTEGER,
        age INTEGER,
        gender TEXT,
        activity_level INTEGER,
        is_active BOOLEAN
    );
    """)

    await conn.commit()

    await cursor.close()
    await conn.close()





async def main(): 
    body = CreateUser(user_id="2", height=99, weight=99, age=99, gender="male", activity_level=4)
    body2 = CreateUser(user_id="3", height=99, weight=99, age=99, gender="male", activity_level=4)
    body1 = CreateUser(user_id="4", height=99, weight=99, age=99, gender="male", activity_level=4)


    await create_users_table()
    user = await _create_new_user(body=body)
    user = await _create_new_user(body=body1)
    user = await _create_new_user(body=body2)



    # async with connect("mydatabase.db") as db: 
    #     user_dal = UserDAL(db)
    #     get_user = await user_dal.get_user(
    #         user_id=2
    #     )
    #     print(get_user)
    #     dyn_us = await User(*get_user)
    #     print(dyn_us)
    

    print(user)



# if __name__ == "__main__": 
#     asyncio.run(main())

from typing import Union 


from pydantic import BaseModel


class User(BaseModel):
    id: int 
    username: str
    password: str 
    game: str


def none_return(a: int | None): 
    if a is not None: 
        return 12
    



# print(none_return(124))
# print(none_return(None))
# print(none_return("dffd"))

import sqlite3


connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Create the `users` table
cursor.execute("""CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  game TEXT NOT NULL
);""")
connection.commit()
               

cursor.execute("INSERT INTO users (id, username, password, game) VALUES (2, 'johndoe', 'password', 'minecraft');")


connection.commit()




def update_field(id, **kwargs) -> bool:
  """
  Updates a field in the `users` table.

  Args:
    username: The username of the user.
    **kwargs: The field and new value to update.

  Returns:
    True if the field was updated, False otherwise.
  """

  query = ", ".join(f"{key} = '{val}'" for key, val in kwargs.items())
  sql = f'''
    UPDATE users 
    SET {query}
    WHERE id = "{id}";
  '''
  cursor.execute(sql)
  connection.commit()

  cursor.execute("""select * FROM users""")
  

  res = cursor.fetchall()

  return res


a = update_field(2, game="dota")
print(a)





# # Insert a new user
# cursor.execute("INSERT INTO users (id, username, password, game) VALUES (2, 'johndoe', 'password', 'minecraft');")
# cursor.execute("INSERT INTO users (id, username, password, game) VALUES (3, 'johndoe', 'password', 'minecraft');")
# cursor.execute("INSERT INTO users (id, username, password, game) VALUES (4, 'johndoe', 'password', 'minecraft');")
# cursor.execute("INSERT INTO users (id, username, password, game) VALUES (5, 'johndoe', 'password', 'minecraft');")

# print(cursor.lastrowid)

# connection.commit()
# cursor.close()


# from typing import Union

# def update_field(id, **kwargs) -> bool:
#   """
#   Updates a field in the `users` table.

#   Args:
#     username: The username of the user.
#     **kwargs: The field and new value to update.

#   Returns:
#     True if the field was updated, False otherwise.
#   """

#   connection = sqlite3.connect("users.db")
#   cursor = connection.cursor()
#   query = ", ".join(f"{key} = '{val}'" for key, val in kwargs.items())
#   sql = f'''
#     UPDATE users 
#     SET {query}
#     WHERE id = "{id}";
#   '''

#   cursor.execute(sql)

#   print("update request, id = ", cursor.lastrowid)

#   connection.commit()
#   cursor.close()
#   print(cursor.rowcount)
#   return cursor.rowcount






# def get_user(user_id: int) -> User: 
#     connection = sqlite3.connect("users.db")
#     cursor = connection.cursor()
#     query = f'''
#                 SELECT * FROM users WHERE id = {user_id};
# '''

#     res1 = cursor.execute(query).fetchone()


#     user = User(**{key: res1[i] for i, key in enumerate(User.__fields__.keys())})
#     return user

#     print("update request, id = ", cursor.lastrowid)

#     connection.commit()
#     cursor.close()
#     print(cursor.rowcount)
#     return cursor.rowcount




# res = update_field(2, password="new_password", game="dota")
# user = get_user(2)
# print(res)
# print(user)







# put your python code here

    # если смешать красный и синий, то получится фиолетовый;
    # если смешать красный и желтый, то получится оранжевый;
    # если смешать синий и желтый, то получится зеленый.
    
    
# from enum import Enum

# color_1 = input()
# color_2 = input()


# class Color(str, Enum) :
#     red = 'красный'
#     blue = 'синий'
#     violet = 'фиолетовый'
#     yellow = 'желтый' 
#     green = "зеленый"



# if color_1 == color_2: 
#     print(color_1)
# else: 
#     if color_1 == ''



# if a and b or b and a :
#     print("фиолетовый")
# elif a and a:
#     print("красный")
# elif b and b :
#     print("желтый")  

# else:
#     print('ошибка цвета')

