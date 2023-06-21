# GoodNutritionBot

GoodNutritionBot is a Telegram bot that helps you track your nutrition and fitness. It has a number of features, including:

* **Add meals:** You can add meals to your log by providing the food name, quantity, and calories.
* **Daily log:** You can view your daily log of meals and exercise.
* **Exercises:** You can add exercises to your log by providing the exercise name, duration, and calories burned.
* **Exercise plan:** You can create an exercise plan by adding exercises and specifying the days and times that you want to do them.
* **Set reminder:** You can set reminders for yourself to eat meals, exercise, or take medication.

## Planned features

* **My reminders:** You can view a list of your reminders.
* **Set time zone:** You can set the time zone for your bot.
* **Update user data:** You can update your profile information, such as your name, weight, and height.
* **Site localization into Russian:** The bot will be translated into Russian.
* **JSON (possibly sql table) with different recipes:** A database of recipes will be added to the bot.
* **A table with the calorie content of a particular food:** A table with the calorie content of different foods will be added to the bot.


## Prerequisites

- Python 3.8 or higher
- aiogram 3.0 or higher
- aioslite
- yoyo-migrations


## Getting started

1. Clone the repository:

   ```
   git clone https://github.com/AntonZimyanin/GoodNutritionBot.git
   ```

2. Navigate to the project directory:

   ```
   cd GoodNutritionBot
   ```

3. Install the required dependencies:

   ```
   poetry install
   ```
4. Rename .env.example to .env and add db path


5. Add your token to .env file


6. Apply migrations to a SQLite database at location /GoodNutritionBot/database.db:

   ```
   yoyo apply --database sqlite:////GoodNutritionBot/database.db ./migrations
   ```



## Usage


1. Run the application:

   ```
   python run_bot.py
   ```

To use GoodNutritionBot, you can send it commands. The following is a list of the available commands:

* **addmeal:** Add a meal to your log.
* **dailylog:** View your daily log of meals and exercise.
* **exercises:** View a list of your exercises.
* **exercise_plan:** View your exercise plan.
* **set_reminder:** Set a reminder for yourself.

You can also use the following commands to get information about the bot:

* **help:** Get help with the available commands.
* **about:** Get information about the bot.

## Contributing

If you would like to contribute to GoodNutritionBot, you can:

* Report bugs and suggest features in the Issues tab.
* Submit pull requests with bug fixes and new features.

## Acknowledgements

- [Aiogram](https://docs.aiogram.dev/en/dev-3.x/index.html) - aiogram is a modern and fully asynchronous framework for Telegram Bot API written in Python 3.8 using asyncio and aiohttp.
- [aiosqlite](https://readthedocs.org/projects/aiosqlite/) - aiosqlite provides a friendly, async interface to sqlite databases.
- [Poetry](https://python-poetry.org/) - Poetry is a tool for dependency management and packaging in Python
- [HTML](https://www.w3.org/html/) - Hypertext Markup Language for creating web pages
- [CSS](https://www.w3.org/Style/CSS/Overview.en.html) - Cascading Style Sheets for styling web pages
- [Yoyo database migrations](https://ollycope.com/software/yoyo/latest/) - Yoyo is a database schema migration tool

## License

GoodNutritionBot is released under the MIT License.
