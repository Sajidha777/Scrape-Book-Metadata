# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonebooksItem(scrapy.Item):
    asin = scrapy.Field()
    genre = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    publisher = scrapy.Field()
    published_date = scrapy.Field()
    description_html = scrapy.Field()
    average_rating = scrapy.Field()
    ratings_count = scrapy.Field()
    print_length = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    book_url = scrapy.Field()
    reviews_url = scrapy.Field()
    
    
# class BookreviewsItem(scrapy.Item):
#     id = scrapy.Field()
#     asin = scrapy.Field()
#     title =  scrapy.Field()
#     user_id =  scrapy.Field()
#     review_helpfulness =  scrapy.Field()
#     review_score =  scrapy.Field()
#     review_date = scrapy.Field()
#     review_summary = scrapy.Field()
#     review_text = scrapy.Field()