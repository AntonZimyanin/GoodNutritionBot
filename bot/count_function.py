from enum import Enum

from bot.body_data import activity_factors
from bot.body_data import diets, BMR_MALE, BMR_FEMALE
from bot.api.schemas import UserIn



class Gender(str, Enum):
    male = "male"
    female = "female"


def calculate_bmi(height: int, weight: int) -> int:
    height_in_meters = height / 100
    bmi = weight / (height_in_meters * height_in_meters)

    return bmi


def calculate_bmr(user: UserIn) -> int:
    '''bmr = basal metabolic +
    (
    the coefficients that are
    used to adjust the BMR for weight * weight in kg
    ) +
    (
    are the coefficients that are
    used to adjust the BMR for height * height in cm)
    ) -
    (
    the coefficients that are
    used to adjust the BMR for age age in years
    )

    66.5 and 655.1 are the basal metabolic rates for a 20-year-old, 70-kilogram (154-pound) male and female, respectively.
    13.75 and 9.563 are the coefficients that are used to adjust the BMR for weight.
    5.003 and 1.850 are the coefficients that are used to adjust the BMR for height.
    6.755 and 4.676 are the coefficients that are used to adjust the BMR for age.

    '''

    match user.gender:
        case Gender.male:
            bmr = (
                BMR_MALE.get("basal_metabolic")
                + (BMR_MALE.get("adjust_weight") * user.weight)
                + (BMR_MALE.get("adjust_height") * user.height * 100)
                - (BMR_MALE.get("adjust_age") * user.age)
            )
        case Gender.female:
            bmr = (
               BMR_FEMALE.get("basal_metabolic")
                + (BMR_FEMALE.get("adjust_weight") * user.weight)
                + (BMR_FEMALE.get("adjust_height") * user.height * 100)
                - (BMR_FEMALE.get("adjust_age") * user.age)
            )


    return bmr


def calculate_exercises(user: UserIn) -> str:
    """
    Calculates various exercise-related values and returns a list
    of recommended exercises based on the user's activity level.

    Args:
        user (User)

    Returns:
        A list of calculated values and recommended exercises, including:
        - BMR (basal metabolic rate):
          the number of calories burned per day at rest
        - TDEE (total daily energy expenditure):
          the number of calories burned per day
          based on activity level
        - BMI (body mass index):
          a measure of body fat based on weight and height
        - ideal_weight (float):
          the user's ideal weight, based on BMI and height
        - Recommended exercises:
          a list of recommended exercises based on the user's activity level
    """

    # Calculate BMR (basal metabolic rate) using the Harris-Benedict equation

    bmr = calculate_daily_calories(user)
    # Calculate TDEE (total daily energy expenditure) based on activity level
    tdee = bmr * user.activity_level

    # Calculate BMI (body mass index)
    bmi = calculate_bmi(user.height, user.weight)

    # Calculate ideal weight based on BMI and height
    ideal_weight = bmi * (user.height**2)

    # Determine recommended exercises based on activity level
    recommended_exercise = {
        1: "Walking, Yoga",
        2: "Jogging, Swimming",
        3: "High-Intensity Interval Training (HIIT), Weightlifting",
        4: "let go chat work for your rodina, such as Belarus",
        5:
    }

    # Return the calculated values and recommended exercises as a list
    return f"""
total daily energy expenditure: {tdee}
body mass index: {bmi}
ideal weight: {ideal_weight}
recommended exercises: {recommended_exercise}
"""


# Calorie calculator
def calculate_daily_calories(user: UserIn) -> int:
    # Formula for calculating daily calories
    bmr = calculate_bmr(user)

    return bmr * activity_factors[user.activity_level]


def generate_exercise_plan(daily_calories) -> str:
    """Generates an exercise plan based on daily calorie burn."""
    if daily_calories < 1500:
        return """
Your daily calorie burn is too low to support exercise.
Focus on increasing your calorie intake and consulting with a healthcare professional.
"""
    elif daily_calories < 2000:
        return """
For a moderate exercise plan, aim for 30 minutes of cardio 3-4 times per week,
and incorporate strength training 2-3 times per week.
"""
    elif daily_calories < 2500:
        return """
For an active exercise plan, aim for 30-60 minutes of cardio 5-7 times per week,
and incorporate strength training 3-4 times per week.
"""
    else:
        return """
For an intense exercise plan, aim for 60+ minutes of cardio 7 times per week,
and incorporate strength training 4-5 times per week.
"""


def choose_diet(user: UserIn):
    # Calculate BMI (Body Mass Index)
    bmi = calculate_bmi(user.height, user.weight)

    # Select a diet plan based on the calculated BMI and daily calorie intake
    if bmi >= 30:
        return {"Keto Diet": diets["Keto Diet"]}
    elif bmi >= 25:
        return {"Mediterranean Diet": diets["Mediterranean Diet"]}
    elif bmi >= 18.5:
        return {"DASH Diet": diets["DASH Diet"]}
    else:
        return {"Weight Watchers": diets["Weight Watchers"]}
