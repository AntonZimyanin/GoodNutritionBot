from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    chat_id: str
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int


class Meal(BaseModel):
    user_id: str
    name: str
    calories: int
    add_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Reminder(BaseModel):
    user_id: str
    description: str
    response_time: datetime
