from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


def calculate_exercises(user_tuple: tuple) -> str:
    """
    Calculates various exercise-related values and returns a list
    of recommended exercises based on the user's activity level.

    Args:
        weight (float): user_tuple[0]
        height (float): user_tuple[1].
        age (int): user_tuple[2].
        gender (str): user_tuple[3].
        activity_level (float): user_tuple[4]

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
    weight = user_tuple[0]
    height = user_tuple[1]
    age = user_tuple[2]
    gender = user_tuple[3]
    activity_level = user_tuple[4]

    bmr = calculate_daily_calories(weight, height, age, gender, activity_level)
    # Calculate TDEE (total daily energy expenditure) based on activity level
    tdee = bmr * activity_level

    # Calculate BMI (body mass index)
    bmi = weight / (height**2)

    # Calculate ideal weight based on BMI and height
    ideal_weight = bmi * (height**2)

    # Determine recommended exercises based on activity level
    if activity_level < 1.5:
        exercises = "Walking, Yoga"
    elif activity_level >= 1.5 and activity_level < 2.0:
        exercises = "Jogging, Swimming"
    else:
        exercises = "High-Intensity Interval Training (HIIT), Weightlifting"

    # Return the calculated values and recommended exercises as a list
    return f"""total daily energy expenditure: {tdee}
body mass index: {bmi}
ideal weight: {ideal_weight}
recommended exercises: {exercises}"""


# Calorie calculator
def calculate_daily_calories(user_tuple: tuple) -> int:
    # Formula for calculating daily calories
    weight = user_tuple[0]
    height = user_tuple[1]
    age = user_tuple[2]
    gender = user_tuple[3]
    activity_level = user_tuple[4]

    if gender == Gender.male:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
    elif gender == Gender.female:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
    else:
        raise ValueError("Invalid gender. Must be 'male' or 'female'.")

    activity_factors = {
        # Sedentary (little or no exercise)
        1: 1.2,
        # Lightly active (light exercise or sports 1-3 days a week)
        2: 1.375,
        # Moderately active (moderate exercise or sports 3-5 days a week)
        3: 1.55,
        # Very active (hard exercise or sports 6-7 days a week)
        4: 1.725,
        # Super active
        # (very hard exercise or sports, physical job or training twice a day)
        5: 1.9,
    }

    return int(bmr * activity_factors[activity_level])


def generate_exercise_plan(daily_calories) -> str:
    """Generates an exercise plan based on daily calorie burn."""
    if daily_calories < 1500:
        return """
Your daily calorie burn is too low to support exercise.
Focus on increasing your calorie intake and consulting with a healthcare professional.
"""
    elif daily_calories < 2000:
        return """For a moderate exercise plan, aim for 30 minutes of cardio 3-4 times per week,
and incorporate strength training 2-3 times per week."""
    elif daily_calories < 2500:
        return """For an active exercise plan, aim for 30-60 minutes of cardio 5-7 times per week,
and incorporate strength training 3-4 times per week."""
    else:
        return """For an intense exercise plan, aim for 60+ minutes of cardio 7 times per week,
and incorporate strength training 4-5 times per week."""
