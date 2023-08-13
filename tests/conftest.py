import asyncio 
import os


from aiosqlite import connect, Connection
import pytest


from bot.config_reader import config


CLEAN_TABLES = (
    "users",
)


@pytest.fixture(scope="session")
async def run_migrations(): 
    os.system("yoyo apply --database sqlite:////GoodNutritionBot/database.db ./migrations")



@pytest.fixture(scope="session")
async def async_db_test() -> Connection: 
    async with connect(config.test_db_url) as db: 
        yield db
        #or return?



@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_db_test):
    """Clean data in all tables before running test function"""
    async with async_db_test() as db: 
        for table_for_cleaning in CLEAN_TABLES: 
            await db.e