from datetime import datetime
import json
from json import JSONEncoder


class Kakao:

    def __init__(self, _id, rest_name, phone_no, address,
                 website, rating, url, menus, reviews):
        self.source = "KAKAO"
        self._id = _id
        self.rest_name = rest_name
        self.phone_no = phone_no
        self.address = address
        self.website = website
        self.rating = rating
        self.url = url
        self.last_update = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.menus = menus
        if "user_reviews" in reviews:
            self.reviews = reviews["user_reviews"]
        if "blog_reviews" in reviews:
            self.blog_reviews = reviews["blog_reviews"]

    def store_data(self, obj):
        with open('data//kakao.txt', 'a+', encoding='utf8') as f:
            f.write(obj + '\n')
