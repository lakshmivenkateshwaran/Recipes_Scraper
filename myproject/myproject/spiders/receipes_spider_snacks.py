import scrapy
import json
import re
from items import SnacksItem
from scrapy import Spider

class RecipesSpider(scrapy.Spider):
    name = 'snacks_recipes'
    start_urls = ['https://www.vegrecipesofindia.com/janmashtami-fasting-recipes/']

    def __init__(self):
        self.recipe_count = 0
        self.ingredient_count = 0


    def parse(self, response):
        # Each recipe URL in a page
        recipe_links = response.css('h2.wprm-recipe-name a::attr(href)').getall()

        for recipe_link in recipe_links:
            yield response.follow(recipe_link, callback=self.parse_recipe)

    def parse_recipe(self, response):
        # Title of the Recipe
        title = response.css('h1.entry-title::text').get()
        # Description of the Recipe
        description = response.css('div.entry-content p::text').get()
        # Ingredients of the Recipe
        ingredients = []
        for ingredient in response.css('div.wprm-recipe-ingredient-group span'):
            amount = ' '.join(re.sub('<[^<]+?>', '', part).strip() for part in ingredient.css('.wprm-recipe-ingredient-amount').getall())
            unit = ' '.join(re.sub('<[^<]+?>', '', part).strip() for part in ingredient.css('.wprm-recipe-ingredient-unit::text').getall())
            name = ' '.join(re.sub('<[^<]+?>', '', part).strip() for part in ingredient.css('.wprm-recipe-ingredient-name::text').getall())
            other = ' '.join(re.sub('<[^<]+?>', '', part).strip() for part in ingredient.css('.wprm-recipe-ingredient-notes::text').getall())
            # Combining all (amount, unit, name) together and append it in ingredients list
            full_ingredient = ' '.join(part.strip() for part in [amount, unit, name, other] if part.strip())
            if full_ingredient:
              ingredients.append(full_ingredient)
        
        formatted_ingredients = ', '.join(ingredients)
                               
        self.recipe_count += 1
        self.ingredient_count += len(ingredients)
        
        # Instructions of the Recipe
        instructions = [instruction.strip().replace('\xa0', ' ') for instruction in response.css('div.wprm-recipe-instruction-text span::text').getall()]

        #Preparation time of the Recipe
        prep_time_number = response.css('span.wprm-recipe-prep_time-minutes::text').get()
        prep_time_unit = 'minutes'
        prep_time = f"{prep_time_number} {prep_time_unit}" if prep_time_number and prep_time_unit else None

        # Cooking time of the Recipe
        cook_time_number = response.css('span.wprm-recipe-cook_time-minutes::text').get()
        cook_time_unit = 'minutes'
        cook_time = f"{cook_time_number} {cook_time_unit}" if cook_time_number and cook_time_unit else None

        # Total time of the Recipe
        total_time = None
        if prep_time_number and cook_time_number:
          total_time_minutes = int(prep_time_number) + int(cook_time_number)
          total_time = f"{total_time_minutes} minutes"
        
        # Cuisine of the Recipe
        cuisine = response.css('span.wprm-recipe-cuisine::text').get()

        # Course of the Recipe
        course = response.css('span.wprm-recipe-course::text').get()
        
        # The format used to store the data
        Snacks_item = {
            'Title': title,
            'Ingredients': formatted_ingredients,
            'Instructions': instructions,
            'Description': description.strip() if description else '',
            'Prep Time': prep_time.strip() if prep_time else '',
            'Cook Time': cook_time.strip() if cook_time else '',
            'Total Time': total_time.strip() if total_time else '',
            'Cuisine': cuisine.strip() if cuisine else '',
            'Course': course.strip() if course else ''
        }
        yield Snacks_item
        
        


