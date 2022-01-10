#ElementControl.py
from Connect import *
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

#' Utilize resources when collecting URLs
class Toplist:
    def __init__(self):
        initpage()

    # Click the More button
    def more(self):
        while(1):
            try:
                driver.find_element_by_xpath("//a[@class='btn-more']").click()
                print('Click More')
            except ElementNotVisibleException:
                break
            except WebDriverException:
                break

    # Click the hashtag
    def tagClick(self, tag):
        driver.find_element_by_xpath("//button[@data-keyword='"+tag+"']").send_keys(Keys.ENTER)
        print('Click Hashtag')

# Use of resources when collecting URLs in hashtag URLs
class CategoryURL:
    def __init__(self, url):
        connect(url)
    
    # Click the More button
    def more(self):
        while(1):
            try:
                driver.find_element_by_xpath("//button[@class='more_btn']").click()
                print('Click More from Category')
            except ElementNotVisibleException:
                break
            except WebDriverException:
                break
            except AttributeError:
                break


# Use of resources when collecting URLs in hashtag URLs
class ReviewsURL:
    def __init__(self, url):
        connect(url)

    # Click the More button
    def more(self):
        while (1):
            try:
                driver.find_element_by_xpath("//div[@class='RestaurantReviewList__MoreReviewButton']").click()
                print('Click More from Reviews')
            except ElementNotVisibleException:
                break
            except WebDriverException:
                break
            except AttributeError:
                break