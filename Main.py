#Main.py
#coding: utf-8

from time import sleep
from datetime import datetime

import pandas as pd

from Connect import *
from ElementControl import *
from Parsing import *
from DBConnect import *
from Scrapper import Scrapper


class Main():
    scrapper = Scrapper()

    # scrapper.search_naver('야채순대곱창', '서울특별시 동작구 동작대로27길 16-7 (사당동)')
    def load_restaurant_file(self):

        print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        df = pd.read_csv("Dongjak-Gu_Restaurants_20190416.csv")

        n_by_state = df.groupby("업태명", sort=False)["업소명"].count()
        # print(n_by_state)

        filter_df = df[(df["업태명"] != "커피숍") & (df["업태명"] != "편의점") & (df["업태명"] != "기타") & (df["업태명"] != "아이스크림")
                       & (df["업태명"] != "일반조리판매") & (df["업태명"] != "기타 휴게음식점") & (df["업태명"] != "다방")
                       & (df["업태명"] != "키즈카페") & (df["업태명"] != "푸드트럭") & (df["업태명"] != "전통찻집")
                       & (df["업태명"] != "떡카페") & (df["업태명"] != "철도역구내") & (df["업태명"] != "과자점")
                       & (df["업태명"] != "백화점") & (df["업태명"] != "감성주점") & (df["업태명"] != "까페")]

        print(str(len(filter_df)))

        # load_naver(filter_df)
        load_kakao(filter_df)

        # for index, row in filter_df.iterrows():
        #     if index < 3:
        #         continue
        #     print("\n\n ============== Scrapping: "+str(index)+" =============")
        #     if pd.isnull(row['소재지(도로명)']):
        #         address = row['소재지(지번)']
        #     else:
        #         address = str(row['소재지(도로명)'])
        #
        #     print("name: "+row['업소명']+" -address: "+address)
        #     scrapper.search_kakao(row['업소명'], address)
        #     print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        #     sleep(2)
        # for index, row in filter_df.iterrows():
        #     if index < 310:
        #         continue
        #     print("\n\n ============== Scrapping: "+str(index)+" =============")
        #     if pd.isnull(row['소재지(도로명)']):
        #         address = row['소재지(지번)']
        #     else:
        #         address = str(row['소재지(도로명)'])
        #
        #     print("name: "+row['업소명']+" -address: "+address)
        #     scrapper.search_naver(row['업소명'], address)
        #     print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        #     sleep(2)

        print("Current Time =", datetime.now().strftime("%H:%M:%S"))


def load_naver(df):
    for index, row in df.iterrows():
        if index < 1433 or index == 257:
            continue
        print("\n\n ============== Scrapping: " + str(index) + " =============")
        if pd.isnull(row['소재지(도로명)']):
            address = row['소재지(지번)']
        else:
            address = str(row['소재지(도로명)'])

        print("name: " + row['업소명'] + " -address: " + address)
        scrapper.search_naver(str(index), row['업소명'], address)
        print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        sleep(2)

def load_kakao(df):
    for index, row in df.iterrows():
        if index < 1324:
            continue

        if index == 2335:
            break
        print("\n\n ============== Scrapping: " + str(index) + " =============")
        if pd.isnull(row['소재지(도로명)']):
            address = row['소재지(지번)']
        else:
            address = str(row['소재지(도로명)'])

        print("name: " + row['업소명'] + " -address: " + address)
        scrapper.search_kakao(str(index), row['업소명'], address)
        print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        sleep(2)

if __name__ == "__main__":

    # Hashtag url list
    collect = []

    scrapper = Scrapper()

    # scrapper.search_naver('안동장', '서울특별시 동작구 흑석로 105-1 (흑석동)')
    # scrapper.scrap_naver("https://m.place.naver.com/restaurant/11677524/home")

    # scrapper.search_kakao('안동장', '서울특별시 동작구 흑석로 105-1 (흑석동)')
    # scrapper.scrap_kakao("https://place.map.kakao.com/16904507")
    Main().load_restaurant_file()
