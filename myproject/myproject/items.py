# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    description = scrapy.Field()
    prep_time = scrapy.Field()
    cook_time = scrapy.Field()
    total_time = scrapy.Field()
    cuisine = scrapy.Field()
    course = scrapy.Field()

class BananaItem(scrapy.Item):
    title = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    description = scrapy.Field()
    prep_time = scrapy.Field()
    cook_time = scrapy.Field()
    total_time = scrapy.Field()
    cuisine = scrapy.Field()
    course = scrapy.Field()

class SnacksItem(scrapy.Item):
    title = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    description = scrapy.Field()
    prep_time = scrapy.Field()
    cook_time = scrapy.Field()
    total_time = scrapy.Field()
    cuisine = scrapy.Field()
    course = scrapy.Field()

class MushroomItem(scrapy.Item):
    title = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    description = scrapy.Field()
    prep_time = scrapy.Field()
    cook_time = scrapy.Field()
    total_time = scrapy.Field()
    cuisine = scrapy.Field()
    course = scrapy.Field()
