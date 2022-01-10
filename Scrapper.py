from spider.NaverSpider import NaverSpider
from spider.KakaoSpider import KakaoSpider

class Scrapper:

    index = ""
    query = ""
    address = ""

    def search(self, query, address):

        self.query = query
        self.address = address

        self.search_naver_url()
        self.search_kakao_url()


    '''Naver Scrapper'''
    '''Search the Restaurant URL from given search query
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant'''
    def search_naver(self, query, address):
        self.query = query
        self.address = address

        self.search_naver_url()

    '''Naver Scrapper'''
    '''Search the Restaurant URL from given search query
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant'''

    def search_naver(self, index, query, address):
        self.index = index
        self.query = query
        self.address = address

        self.search_naver_url()


    def search_naver_url(self):
        naver_spider = NaverSpider()
        naver_spider.set_id(self.index)
        naver_url_id = naver_spider.search(self.query, self.address)
        if naver_url_id:
            naver_spider.scrap_restaurant(naver_url_id, url=False)
        print("============= scrapped restaurant ==========")


    def scrap_naver(self, url):
        naver_spider = NaverSpider()
        naver_spider.set_id(self.index)
        naver_spider.scrap_naver_restaurant(url)

    '''Kakao Scrapper'''
    '''Search the Restaurant URL from given search query
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant'''
    def search_kakao(self, query, address):
        self.query = query
        self.address = address

        self.search_kakao_url()


    '''Kakao Scrapper'''
    '''Search the Restaurant URL from given search query
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant'''
    def search_kakao(self, index, query, address):
        self.index = index
        self.query = query
        self.address = address

        self.search_kakao_url()


    def search_kakao_url(self):
        kakao_spider = KakaoSpider()
        kakao_spider.set_id(self.index)
        kakao_url = kakao_spider.search(self.query, self.address)
        if kakao_url:
            kakao_spider.scrap_restaurant(kakao_url)
        print("============= scrapped restaurant ==========")

    def scrap_kakao(self, url):
        kakao_spider = KakaoSpider()
        kakao_spider.set_id(self.index)
        kakao_spider.scrap_kakao_restaurant(url)

    '''Google Scrapper'''
    '''Search the Restaurant URL from given search query
        @:param query: restaurant name to search
        @:param address: restaurant address for verifying the valid restaurant'''
    def search_google(self, query, address):
        self.query = query
        self.address = address

        self.search_google()

    def search_google(self):
        naver_spider = NaverSpider()
        naver_url_id = naver_spider.search(self.query, self.address)
        if naver_url_id:
            naver_spider.scrap_restaurant(naver_url_id, url=False)
        print("============= scrapped restaurant ==========")

    def scrap_naver(self, url):
        naver_spider = NaverSpider()
        naver_spider.scrap_naver_restaurant(url)
