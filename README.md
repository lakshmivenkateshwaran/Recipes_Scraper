# SCRAPY_DATA_PROJECT_APP

This Scrapy project is designed to scrape recipes and related information from a verified website dedicated to culinary delights. The spider crawls through the website's pages, extracting recipe titles, ingredients, instructions, cooking times, and more. The extracted data is then stored in structured JSON format for further analysis and use.

# Scraped Website: 'https://www.vegrecipesofindia.com/recipes/south-indian-recipes/'

## Project Structure

- scrapy.cfg            # Scrapy configuration file
- myproject             # Scrapy project directory
- spiders               # Directory for Scrapy spiders
- __init__.py           # Python initialization file
- receipes_spider.py    # Scrapy spider for scraping recipes
- items.py              # Defines the data model for scraped items
- middlewares.py        # Scrapy middleware settings
- pipelines.py          # Pipeline for processing scraped items
- settings.py           # Scrapy project settings
- data_cleaning.py      # Python script for data cleaning with pandas
- data_insertion.py     # Python script for storing the data into MongoDB
- receipes_spider_mushroom.py   # Python script for scraping Mushroom recipes
- receipes_spider_snacks.py     # Python script for scraping Snacks recipes
- receipes_spider_banana.py     # Python script for scraping Banana recipes
- main.py               # Python scrapy scripts inside FastAPI
- final_recipes.json    # Final json data which has some empty objects
- updated_final_recipes.json    # Updated and cleaned Data
- README.md             # Project documentation
- requirements.txt      # List of project dependencies

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Set up a virtual environment (optional but recommended).
   python -m venv env
   env\Scripts\activate  # On Windows
   source env/bin/activate  # On macOS/Linux
4. Install the required dependencies using `pip install -r requirements.txt`.