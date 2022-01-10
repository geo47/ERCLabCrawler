#Parsing.py

from Connect import *
from bs4 import BeautifulSoup
from selenium.common.exceptions import *
import time

class Parsing :

    # Hashtag collection
    def collectHashTag(self):
        print('Collecting Hashtags...')
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        hashTag = []
        for dataKeyWord in soup.find_all('button'):
            if dataKeyWord.get('data-keyword') is None:
                continue
            else:
                hashTag.append(dataKeyWord.get('data-keyword'))
        print('Hashtags collected: '+str(len(hashTag)))
        return hashTag

    # Hashtag URL Collection
    def getLink(self):
        print('Collecting Hashtag URLs...')
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        rlink = []
        for link in soup.find_all('a'):
            try:
                if link.get('href').find('top_lists/') != -1 :
                    if link.get('href').find('link_key') == -1 :
                        rlink.append(link.get('href'))
            except AttributeError:
                continue
        print('Hashtag URLs Collected: '+str(len(rlink)))
        return rlink

    # Restaurant URL Collection
    def getHotLink(self):
        print('Collecting Restaurant Links...')
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        hotlink = []
        for link in soup.find_all('a'):
            try:
                if link.get('href').find('restaurants') != -1 :
                    if link.get('href').find('restaurant_key') == -1 :
                        hotlink.append(link.get('href'))
            except AttributeError:
                continue
        print('Restaurant Links Collected:: '+str(len(hotlink)))
        return list(set(hotlink))

    # Parsing and pre-processing restaurant information
    def parsingHot(self, url):
        print('connecting and parsing restaurant: '+url)
        connect(url)
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        try:
            # Restaurant name
            title = soup.find("h1",{"class": "restaurant_name"})
            # Restaurant rating
            rating = soup.find("strong",{"class": "rate-point"})
            # Restaurant information
            info = dict()
            info['url'] = url
            info['이름'] = title.get_text()
            info['평점'] = rating.get_text().replace('\n', '')
            print('restaurant name: '+info['이름'])
            table = soup.find("tbody")
            for thtd in table.find_all("tr"):
                if thtd.th.get_text() != "메뉴":
                    temp = thtd.th.get_text().replace(' ', '')
                    info[temp.replace('\n', '')] = thtd.td.get_text().replace('\n', '')
                else:
                    info[thtd.th.get_text()] = thtd.td.get_text()

            # total_reviews_el = soup.find("span",{"class": "RestaurantReviewList__AllCount"}).get_text()
            # print('total_reviews_el: '+total_reviews_el)
            # total_reviews_count = int(total_reviews_el)
            # reviews_count = 0
            # while reviews_count < total_reviews_count:
            #     try:
            #         driver.find_element_by_xpath("//div[@class='RestaurantReviewList__MoreReviewButton']").click()
            #         time.sleep(2)
            #         print('Click More from Reviews')
            #         reviews_count = reviews_count + 5
            #     except ElementNotVisibleException:
            #         break
            #     except WebDriverException:
            #         break
            #     except AttributeError:
            #         break
            #
            # reviews = []
            # reviews_html = soup.find("ul",{"class": "RestaurantReviewList__ReviewList"})
            # print('reviewList length: ' + str(len(reviews_html.find_all("li"))))
            # for li in reviews_html.find_all("li"):
            #     review = {}
            #     try:
            #         reviewer = li.find("span", {"class": "RestaurantReviewItem__UserNickName"}).getText()
            #         review_content = li.find("p", {"class": "RestaurantReviewItem__ReviewText"}).getText()
            #         review_date = li.find("span", {"class": "RestaurantReviewItem__ReviewDate"}).getText()
            #         review_rate = li.find("span", {"class": "RestaurantReviewItem__RatingText"}).getText()
            #         review['reviewer'] = reviewer
            #         review['review_content'] = review_content
            #         review['review_date'] = review_date
            #         review['review_rate'] = review_rate
            #         print('r: '+reviewer+', r_content: '+review_content+', r_date: '+review_date+', r_rate: '+review_rate)
            #
            #         reviews.append(str(review))
            #     except:
            #         print('error')
            # info['reviews'] = reviews
            return info
        except AttributeError:
            print("없음")