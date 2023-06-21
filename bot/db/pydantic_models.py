from datetime import datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int


class UserIn(BaseUser):
    pass


class UserDB(BaseUser):
    chat_id: str


class Meal(BaseModel):
    id: int
    user_id: str
    name: str
    calories: int
    add_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Reminder(BaseModel):
    id: int
    user_id: str
    description: str
    response_time: datetime
