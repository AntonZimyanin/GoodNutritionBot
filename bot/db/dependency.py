from functools import wraps

from aiosqlite import connect


############################################
# DECORATOR THAT RETURNS A CONNECTION OBJECT
###########################################


def connect_db(db_url):
    """
    soliD — Dependency Inversion
    Top level modules should not depend
    on lower level modules,
    so on I am taking db path as parameter
    """

    def decorator(func):
        wraps(func)

        async def wrapper(*args, **kwargs):
            async with connect(db_url) as db:
                return await func(db, *args, **kwargs)

        return wrapper

    return decorator
