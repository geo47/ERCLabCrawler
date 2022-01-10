from scrapy.selector import Selector

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from config.YelpConfig import YelpConfig
from config import Config as cfg



class YelpSpider:
    def __init__(self):
        self.driver = cfg.get_driver()
        self.yelp_config = YelpConfig()

    ''' Scrap the Restaurant Menu list'''
    def scrap_menu(self, url):

        driver = self.driver
        driver.get(url)

        # try:
        #     WebDriverWait(driver, 15).until(
        #         EC.presence_of_element_located((
        #             By.CSS_SELECTOR, self.yelp_config.get_menu()["title"])))
        # except TimeoutException:
        #     print("KAKAO: No Search Result")

        scrapy_selector = Selector(text=driver.page_source)
        print(self.yelp_config.get_menu()['title'])
        menus = scrapy_selector.css(self.yelp_config.get_template()['menus'])
        # print(menus.extract())

        menu_list = []
        for i in range(len(menus)):
            menu_dic = {}
            menu = menus[i]

            # print(self.yelp_config.get_menu()["title"] % "")
            menu_title = menu.xpath(self.yelp_config.get_menu()["title"] % "").extract_first().strip()
            if not menu_title:
                # print(self.yelp_config.get_menu()["title"] % "/a")
                menu_title = menu.xpath(self.yelp_config.get_menu()["title"] % "/a").extract_first()

            # menu_title = scrapy_selector.css(self.yelp_config.get_menu()["title"]).text
            # menu_title = menu.xpath(self.yelp_config.get_menu()["title"] %"").extract_first()
            # print(menu_title)

            if menu_title:
                # print("menu_title: " + menu_title)
                print(menu_title)
                menu_dic["title"] = menu_title
                menu_list.append(menu_dic)

        return menu_list