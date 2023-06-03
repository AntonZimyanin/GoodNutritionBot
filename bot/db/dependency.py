from functools import wraps

from aiosqlite import connect


############################################
# DECORATOR THAT RETURNS A CONNECTION OBJECT
###########################################


def connect_db(db_url):
    def decorator(func):
        wraps(func)

        async def wrapper(*args, **kwargs):
            async with connect(db_url) as db:
                return await func(db, *args, **kwargs)

        return wrapper

    return decorator
