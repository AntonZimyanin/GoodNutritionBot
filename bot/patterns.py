import re

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
DIGIT_MATCH_PATTERN = re.compile(r"[0-9]{2,3}")
GENDER_LIST = ["male", "female"]
ACTIVITY_LEVEL_LIST = ["1", "2", "3", "4", "5"]
