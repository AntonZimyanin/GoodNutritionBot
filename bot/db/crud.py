from datetime import datetime
from sqlite3 import Connection

from aiosqlite import Row

from bot.config_reader import config
from bot.db.dependency import connect_db
from bot.db.pydantic_models import Meal
from bot.db.pydantic_models import Reminder
from bot.db.pydantic_models import User


##############################
#   BLOCK FOR CREATE ALL TABLE
#############################


############################
#   BLOCK FOR ADDING DATA
###########################


@connect_db(db_url=config.db_url)
async def add_reminder(db: Connection, reminder: Reminder) -> None:
    await db.execute(
        """ INSERT INTO
                        reminders (
                            user_id
                            , description
                            , response_time
                            )
                            VALUES (?, ?, ?)""",
        (reminder.user_id, reminder.description, reminder.response_time),
    )

    await db.commit()


@connect_db(db_url=config.db_url)
async def add_meal(db: Connection, meal: Meal) -> None:
    await db.execute(
        """ INSERT INTO
                meals (
                    user_id
                    , name
                    , calories
                    , add_time
                    )
                    VALUES (?, ?, ?, ?)""",
        (meal.user_id, meal.name, meal.calories, meal.add_time),
    )

    await db.commit()


@connect_db(db_url=config.db_url)
async def add_user(db: Connection, user: User) -> None:
    await db.execute(
        """ INSERT INTO
                users (
                    chat_id
                    , weight
                    , height
                    , age
                    , gender
                    , activity_level
                    )
                    VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user.chat_id,
            user.weight,
            user.height,
            user.age,
            user.gender,
            user.activity_level,
        ),
    )

    await db.commit()


##################################
#  BLOCK TO UPDATE OR CHANGE DATA
#################################


@connect_db(db_url=config.db_url)
async def delete_remider(db: Connection, user_id: str):
    await db.execute(
        """DELETE
                FROM reminders
                WHERE user_id = ?""",
        (user_id,),
    )
    await db.commit()


# Note:
# create keyboard with all meal
# where somebody wanted delete
# meal and push on button with
# meal -> calback data in button
# it's meal_id
# in the meantime, we will
# delete by name and user-id
@connect_db(db_url=config.db_url)
async def delete_meal(db: Connection, meal_name, user_id):
    await db.execute(
        """DELETE
                    FROM meals
                    WHERE user_id = ?
                    AND
                    name = ?
                    """,
        (user_id, meal_name),
    )
    await db.commit()


@connect_db(db_url=config.db_url)
async def update_params(db: Connection, **kwargs):
    chat_id = kwargs.get("chat_id")
    for key, val in kwargs.items():
        await db.execute(
            f"""UPDATE users
                    SET
                    {key} = ?
                WHERE chat_id = ?
                """,
            (val, chat_id),
        )
    await db.commit()


###########################################
#  BLOCK FOR SENDING DATA / OR FOR GET DATA
###########################################


@connect_db(db_url=config.db_url)
async def select_meals(db: Connection, user_id: str) -> Row | None:
    """
    return:  name, calories, add_time
    """
    async with db.execute(
        """SELECT
            name
            , calories
            , add_time
            FROM meals
            WHERE user_id = ?""",
        (user_id,),
    ) as cursor:
        meals = await cursor.fetchall()

    if meals is not None:
        return meals


@connect_db(db_url=config.db_url)
async def is_user(db: Connection, user_id: str) -> True | False:
    """
    function checks
    if the user exists in the database
    return: True or False
    """
    async with db.execute(
        """SELECT
                chat_id
                FROM users
                WHERE chat_id = ?""",
        (user_id,),
    ) as cursor:
        user = await cursor.fetchone()

    if user is not None:
        return True
    return False


@connect_db(db_url=config.db_url)
async def get_user(db: Connection, user_id: str) -> Row | None:
    """
    return: (weight, height, age, gender, activity_level) or None
    """
    async with db.execute(
        """SELECT
                weight
                , height
                , age
                , gender
                , activity_level
                FROM users
                WHERE chat_id = ?""",
        (user_id,),
    ) as cursor:
        user = await cursor.fetchone()

    if user is not None:
        return user


@connect_db(db_url=config.db_url)
async def get_le_current_time(db: Connection) -> Row | None:
    """
    if there is a reminder whose time is less
    than or equal to the current one,
    then the function returns the values

    return: user_id and reminder description
    """
    async with db.execute(
        """SELECT
                user_id
                , description
                FROM reminders
                WHERE response_time <= ?""",
        (datetime.now(),),
    ) as cursor:
        row = await cursor.fetchone()

    return row
