
from scrapy.selector import Selector

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from config.GoogleConfig import GoogleConfig
from config import Config as cfg
from data.Google import Google


class GoogleSpider:

    def __init__(self):
        self.driver = cfg.get_driver()
        self.google_config = GoogleConfig()

    ''' Search the Restaurant URL from given search query by calling @scrap_url function
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant
        @:returns: the home url of the restaurant @None otherwise'''
    def search(self, query, address):
        self.__init__()

        self.query = query
        self.address = address

        address_arr = self.address.split(" ")
        # https: // www.google.com / search?q = 안동장
        # 서울특별시
        # 동작구
        # 흑석로

        driver = self.driver
        driver.get(cfg.query_url["google"] % (self.query +" "+address_arr[0]+" "+address_arr[1]+" "+address_arr[2]))

        scrapy_selector = Selector(text=driver.page_source)

        try:
            driver.find_element(By.XPATH, self.google_config.get_template()["body"]) \
                .is_displayed()

            print('Query found')



        except NoSuchElementException:
            print('Query not found')
            pass