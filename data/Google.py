import json
from simplejson import JSONEncoder


class Google:

    def __init__(self, rest_name, phone_no, address,
                 website, rating, url, menus, reviews):
        self.source = "GOOGLE"
        self.rest_name = rest_name
        self.phone_no = phone_no
        self.address = address
        self.website = website
        self.rating = rating
        self.url = url
        self.menus = menus
        if "user_reviews" in reviews:
            self.reviews = reviews["user_reviews"]
        if "blog_reviews" in reviews:
            self.blog_reviews = reviews["blog_reviews"]


    def store_data(self, obj):
        with open('data//google.txt', 'a+', encoding='utf8') as f:
            f.write(obj+'\n')