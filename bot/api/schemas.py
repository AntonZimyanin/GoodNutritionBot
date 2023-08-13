from datetime import datetime

from pydantic import BaseModel


#####################
#   User Schemas   #
####################


class User(BaseModel): 
    '''for build object'''
    user_id: str
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int
    is_active: bool = True

    


class BaseUser(BaseModel, ):
    weight: int
    height: int
    age: int
    gender: str
    activity_level: int



class UserIn(BaseUser):
    pass


class ShowUser(BaseUser):
    user_id: str
    is_active: bool 


######################
#   Meal Schemas    #
#####################


# class BaseMeal(BaseModel): 
#     user_id: str
#     name: str
#     calories: int
#     add_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# class CreateMeal(BaseMeal):
#     pass


# class ShowMeal(BaseModel):
#     id: int
    


class Meal(BaseModel):
    id: int
    user_id: str
    name: str
    calories: int
    add_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


##########################
#   Reminder Schemas    #
#########################


class Reminder(BaseModel):
    id: int
    user_id: str
    description: str
    response_time: datetime
