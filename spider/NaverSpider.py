from time import sleep
from pprint import pprint

import simplejson as json

from scrapy.selector import Selector

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from config.NaverConfig import NaverConfig
from config import Config as cfg
from data.Naver import Naver\
    # , NaverEncoder
from pipeline import KafkaProducer


class NaverSpider:

    def __init__(self):
        self.driver = cfg.get_driver()
        self.naver_config = NaverConfig()

    def set_id(self, index):
        self._id = index

    ''' Search the Restaurant URL from given search query by calling @scrap_url function
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant
        @:returns: the home url of the restaurant @None otherwise'''
    def search(self, query, address):
        self.__init__()

        self.query = query
        self.address = address

        naver_url_id = self.scrap_url()

        if naver_url_id:
            print("Naver URL id found: " + naver_url_id)
        else:
            print("Naver URL id not found")

        return naver_url_id

    ''' Scrap the Restaurant URL from searching result
        @:returns: the ID of the restaurant @None otherwise'''
    def scrap_url(self):
        url_id = ""

        driver = self.driver
        driver.get(cfg.query_url["naver"] % (self.query))

        scrapy_selector = Selector(text=driver.page_source)
        if cfg.debug:
            print("address: " + self.address)
        search_result = scrapy_selector.css(self.naver_config.get_search()["list"])
        for i in range(len(search_result)):
            li_restaurant = search_result[i]

            li_address = li_restaurant.xpath(
                self.naver_config.get_search()["address"] % (str(i+1)))\
                .extract_first()
            if cfg.debug:
                print("li_address: " + li_address)

            li_address_arr = li_address.split(" ")
            address_line = self.address.split(" ")

            '''Address formatting [City] [District] [Street]'''
            if (li_address_arr[0] == cfg.seoul_1 or li_address_arr[0] == cfg.seoul_2) and \
                    li_address_arr[1] == address_line[1] and \
                    li_address_arr[2] == address_line[2]:
                if cfg.debug:
                    print(li_address_arr)
                    print(address_line)
                print("Address matched")
                url_id = li_restaurant.css(self.naver_config.get_search()["url_id"]).extract_first()
                if cfg.debug:
                    print(url_id)
                break

        driver.close()
        driver.quit()
        return url_id

    ''' Scrap the Restaurant home page from the restaurant URL or restaurant ID by 
        calling @scrap_naver_restaurant function
        @:param url_id: URL or the ID of the restaurant home page
        @:param url: whether the url_id is a URL or the ID of the restaurant'''
    def scrap_restaurant(self, url_id, url=False):
        self.__init__()

        if url:
            naver_url = url_id
        else:
            naver_url = cfg.detail_page_url["naver"] % (url_id)

        self.scrap_naver_restaurant(naver_url)

    ''' Scrap the Restaurant home page from the restaurant URL
        @:param naver_url: URL of the restaurant home page'''
    def scrap_naver_restaurant(self, naver_url):

        driver = self.driver

        print("naver_url: "+naver_url)

        driver.get(naver_url)
        driver.implicitly_wait(3)

        tabs = driver.find_elements_by_xpath(self.naver_config.get_template()["tabs"])
        if cfg.debug:
            print(str(len(tabs)))

        name = self.query #driver.find_element_by_xpath(self.naver_config.get_template()["name"]).text
        address = self.address #driver.find_element_by_css_selector(self.naver_config.get_template()["address"]).text
        website = ""
        try:
            website = driver.find_element_by_css_selector(self.naver_config.get_template()["website"]).get_attribute['href']
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass
        if cfg.debug:
            print("ID: " + self._id)
            print("name: "+name)
            print("address: "+address)
            print("website: "+website)

        menus = self.scrap_menus(driver, tabs)
        print("Menus scraped: "+str(len(menus)))
        if cfg.debug:
            pprint(menus)
        reviews = self.scrap_reviews(driver, tabs)
        if cfg.debug:
            pprint(reviews)

        naver = Naver(self._id, name, "", address, website, "", naver_url, menus, reviews)
        encoded_data = json.dumps(naver.__dict__, ensure_ascii=False, encoding="utf-8")
        print(encoded_data)

        if (cfg.data_streaming):
            KafkaProducer.connect_kafka_producer()
        else:
            naver.store_data(encoded_data)

        driver.close()
        driver.quit()


    ''' Scrap the Restaurant Menu list
        @:param driver: HTML dynamic page content extracted by @Selenium driver
        @:param tabs: tabs from the home page'''
    def scrap_menus(self, driver, tabs):
        menu_list = []
        menu_button = ""

        for tab in tabs:
            href_attr = tab.get_attribute("href")
            if href_attr.endswith("/menu"):
                menu_button = tab
                break

        if not isinstance(menu_button, str):
            menu_button.click()

            i = 1
            while True:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, self.naver_config.get_menu()["load_more_btn"]))).click()
                    if cfg.debug:
                        print("Load more menus button clicked")
                        print("Click: " + str(i))
                    i = i + 1
                except TimeoutException:
                    if cfg.debug:
                        print("No more Load more menus button to be clicked")
                    break

            scrapy_selector = Selector(text=driver.page_source)
            menus = scrapy_selector.css(self.naver_config.get_template()["menus"])

            for i in range(len(menus)):
                menu_dic = {}
                menu = menus[i]
                menu_title = menu.xpath(self.naver_config.get_menu()["title"]).extract_first()
                menu_price = menu.xpath(self.naver_config.get_menu()["price"]).extract_first()

                if menu_title and menu_price:
                    if cfg.debug:
                        print("menu_title: " + menu_title)
                        print("menu_price: " + menu_price)
                    menu_dic["title"] = menu_title
                    menu_dic["price"] = menu_price
                    menu_list.append(menu_dic)

        return menu_list


    def scrap_reviews(self, driver, tabs):
        reviews_dic = {}
        review_list = []
        blog_review_list = []
        review_button = ""

        sleep(1)
        for tab in tabs:
            try:
                href_attr = tab.get_attribute("href")
                if href_attr.endswith("/review"):
                    review_button = tab
                    break
            except NoSuchElementException:
                print('No reviews tab found')
                return
                pass

        if not isinstance(review_button, str):
            review_button.click()

            count_review_tabs = 0

            try:
                review_tabs = driver.find_elements_by_xpath(self.naver_config.get_template()["review_tabs_len"])
                count_review_tabs = len(review_tabs)
            except NoSuchElementException:  # spelling error making this code not work as expected
                pass

            print('count_review_tabs: '+str(count_review_tabs))
            index_user_reviews = 1
            index_blog_reviews = 2
            if count_review_tabs > 2:
                index_user_reviews = 2
                index_blog_reviews = 3

            review_tab1 = ""
            '''Click First tab and get the User Reviews'''
            try:
                review_tab1 = driver.find_element_by_xpath(self.naver_config.get_template()["review_tabs"] % str(index_user_reviews))
            except NoSuchElementException:  # spelling error making this code not work as expected
                pass

            if not isinstance(review_tab1, str):

                review_tab1.click()

                i = 1
                while True:
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, self.naver_config.get_review()["load_more_btn"]))).click()
                        if cfg.debug:
                            print("Load more reviews button clicked")
                            print("Click: " + str(i))
                        i = i + 1
                        sleep(0.5)
                    except TimeoutException:
                        if cfg.debug:
                            print("No more Load more reviews button to be clicked")
                        break
                    except StaleElementReferenceException:
                        if cfg.debug:
                            print("No more Load more reviews button to be clicked")
                        break
            else:
                print("No review buttons...")

            scrapy_selector = Selector(text=driver.page_source)
            reviews = scrapy_selector.css(self.naver_config.get_template()["reviews"])

            for i in range(len(reviews)):
                review_dic = {}
                review = reviews[i]
                review_rating = review.xpath(self.naver_config.get_review()["rating"]).extract_first()
                review_text = review.xpath(self.naver_config.get_review()["review"]).extract_first()
                reviewer = review.xpath(self.naver_config.get_review()["reviewer"]).extract_first()
                review_date = review.xpath(self.naver_config.get_review()["review_date"]).extract_first()

                if review_rating:
                    # have to replace this with extract_number()
                    review_rating = str(int(''.join(filter(str.isdigit, review_rating)))/20)
                else:
                    review_rating = ""

                if not review_text:
                    review_text = ""

                # remove the last '.' from date string
                if not reviewer:
                    reviewer = ""

                if review_date:
                    review_date = review_date[:-1]

                if cfg.debug:
                    print("rating: " + review_rating)
                    print("review: " + review_text)
                    print("reviewer: " + reviewer)
                    print("review_date: " + review_date)
                review_dic["rating"] = review_rating
                review_dic["review"] = review_text
                review_dic["reviewer"] = reviewer
                review_dic["review_date"] = review_date
                review_list.append(review_dic)

            print("User reviews scraped: " + str(len(review_list)))
            '''Add reviews in user review list'''
            reviews_dic["user_reviews"] = review_list

            review_tab2 = ""
            '''Click First tab and get the User Reviews'''
            try:
                review_tab2 = driver.find_element_by_xpath(self.naver_config.get_template()["review_tabs"] % str(index_blog_reviews))
            except NoSuchElementException:  # spelling error making this code not work as expected
                pass

            if not isinstance(review_tab2, str):
                '''Click Second tab and get the Blog Reviews'''
                review_tab2.click()

                i = 1
                while True:
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, self.naver_config.get_blog_review()["load_more_btn"]))).click()
                        if cfg.debug:
                            print("Load more blog reviews button clicked")
                            print("Click: " + str(i))
                        i = i + 1
                        sleep(0.5)
                    except TimeoutException:
                        if cfg.debug:
                            print("No more Load more blog reviews button to be clicked")
                        break
                    except StaleElementReferenceException:
                        if cfg.debug:
                            print("No more Load more reviews button to be clicked")
                        break

                scrapy_selector = Selector(text=driver.page_source)
                blog_reviews = scrapy_selector.css(self.naver_config.get_template()["blog_reviews"])

                for i in range(len(blog_reviews)):
                    blog_review_dic = {}
                    blog_review = blog_reviews[i]
                    link = blog_review.xpath(self.naver_config.get_blog_review()["link"]).extract_first()

                    blog_review_dic["link"] = link
                    blog_review_list.append(blog_review_dic)

                print("Blog reviews scraped: " + str(len(blog_review_list)))
            reviews_dic["blog_reviews"] = blog_review_list

        return reviews_dic
