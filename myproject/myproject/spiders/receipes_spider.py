import scrapy
import json
import re
from ..items import RecipeItem

class RecipesSpider(scrapy.Spider):
    name = 'recipes'
    page_number = 2
    start_urls = ['https://www.vegrecipesofindia.com/recipes/south-indian-recipes/']

    def __init__(self):
        self.recipe_count = 0
        self.ingredient_count = 0


    def parse(self, response):
        # Each recipe URL in a page
        recipe_links = response.css('h2.post-summary__title a::attr(href)').getall()

        for recipe_link in recipe_links:
            yield response.follow(recipe_link, callback=self.parse_recipe)
        # Pagination till 25 pages
        next_page = 'https://www.vegrecipesofindia.com/recipes/south-indian-recipes/page/' + str(RecipesSpider.page_number) + '/'
        if RecipesSpider.page_number <= 26:
            RecipesSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

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
            # Combining all (amount, unit, name) together and append it in ingredients list
            full_ingredient = ' '.join(part.strip() for part in [amount, unit, name] if part.strip())
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

        recipe_item = RecipeItem()
        recipe_item['title'] = title
        recipe_item['ingredients'] = formatted_ingredients
        recipe_item['instructions'] = instructions
        recipe_item['description'] = description
        recipe_item['prep_time'] = prep_time
        recipe_item['cook_time'] = cook_time
        recipe_item['total_time'] = total_time
        recipe_item['cuisine'] = cuisine
        recipe_item['course'] = course
        yield recipe_item
        
        # The format used to store the data
        recipe_item = {
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
        
        # Created a new list to append the data
        if not hasattr(self, 'recipe_list'):
            self.recipe_list = []
        self.recipe_list.append(recipe_item)
        yield recipe_item
        
        # Inserted that created new list into the Dictionary
        json_data = {
            "code": 200,
            "status": "Success",
            "Message": "Successfully Fetched the Receipes List",
            "receipe_data": self.recipe_list
        }
        # Save the recipe item to a JSON file
        with open('final_recipes.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            

        
    # Close function which will print the number recipes in log
    def closed(self, reason):
        self.logger.info(f"Scraped {self.recipe_count} recipe titles.")
        self.logger.info(f"Scraped {self.ingredient_count} ingredients.")




            #amount = ' '.join(re.sub('<[^<]+?>', '', ingredient.css('.wprm-recipe-ingredient-amount').getall()).strip()for ingredient in ingredients)
            #unit = ' '.join(re.sub('<[^<]+?>', '', ingredient.css('.wprm-recipe-ingredient-unit::text').getall()).strip()for ingredient in ingredients)
            #name = ' '.join(re.sub('<[^<]+?>', '', ingredient.css('.wprm-recipe-ingredient-name::text').getall()).strip()for ingredient in ingredients)
            #other = ' '.join(re.sub('<[^<]+?>', '', ingredient.css('span.wprm-recipe-ingredient-notes wprm-recipe-ingredient-notes-normal::text').getall()).strip()for ingredient in ingredients)

            #amount = ingredient.css('.wprm-recipe-ingredient-amount').getall(default='')
            #unit = ingredient.css('.wprm-recipe-ingredient-unit::text').getall(default='')
            #name = ingredient.css('.wprm-recipe-ingredient-name::text').getall(default='')
            #other = ingredient.css('span.wprm-recipe-ingredient-notes wprm-recipe-ingredient-notes-normal::text').getall(default='').strip()

