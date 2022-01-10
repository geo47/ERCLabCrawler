import random

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent

template_path = "/home/muzamil/Projects/Python/Crawler/ERCLab Crawler"

debug = False
seoul_1 = "서울특별시"
seoul_2 = "서울"

data_streaming = False


def get_driver():
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    print(random_user_agent)

    # proxy = get_proxy()
    # print(proxy)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    # chrome_options.add_argument('--proxy-server=%s' % proxy)


    # proxy = Proxy()
    # proxy.proxyType = ProxyType.MANUAL
    # proxy.autodetect = False
    # proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = "127.0.0.1:9000"
    # chrome_options.Proxy = proxy
    # chrome_options.add_argument("ignore-certificate-errors")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver')
    return driver

def get_proxy():
    proxy_list = ["188.40.183.185:1080",
                  "203.19.92.3:80",
                  "203.202.245.58:80",
                  "190.93.156.107:8080",
                  "201.55.160.99:3128",
                  "191.102.116.114:999",
                  "35.220.131.188:80",
                  "36.37.177.186:8080",
                  "205.185.127.8:8080",
                  "27.255.58.72:8080",
                  "52.53.135.163:3128",
                  "109.74.130.129:8080",
                  "125.62.192.225:83"]

    return random.choice(proxy_list)

query_url = {
    "naver":"https://m.map.naver.com/search2/search.nhn?query=%s",
    "kakao": "https://map.kakao.com/?q=%s",
    "google": "https://www.google.com/search?q=%s",
    "siksin_hot": "",
    "dining_code": "",
    "mango_plate": ""
}

detail_page_url = {
    "naver":"https://m.place.naver.com/restaurant/%s/home",
    "kakao": "https://place.map.kakao.com/%s",
    "google": "",
    "siksin_hot": "",
    "dining_code": "",
    "mango_plate": ""
}

def get_naver_template():
    with open("template/naver-site.yaml", "r") as yaml_file:
        cfg = yaml.load(yaml_file)

    for section in cfg:
        print(section)
    print(cfg["mysql"])
    print(cfg["other"])