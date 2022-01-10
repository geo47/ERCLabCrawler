#Connect.py

# from selenium import webdriver
# import csv
# # ChromeDriver Connection timeout 3 seconds
# driver = webdriver.Chrome('chromedriver.exe')
# driver.implicitly_wait(3)
#
# # Load web page
# def initpage():
#     print('App initialized \nSeed URL: https://www.mangoplate.com/top_lists')
#     driver.get('https://www.mangoplate.com/top_lists')
#
#     # f = open('db.csv', 'a', encoding="utf-8",)
#     # row = ['파스타', '아방뮤제', '용산구', '이태원로55가길', '서울특별시 용산구 이태원로55가길 13 지번서울시 용산구 한남동 739 - 20', '02 - 790 - 7392', '스테이크 / 바베큐', '4.3', '12: 00 - 22:00', '둘째 / 넷째 화', '+ 1']
#     # with f:
#     #     print('here')
#     #     writer = csv.writer(f, dialect='excel')
#     #     writer.writerow(row)
#     # f = open('db.csv', 'a')
#     # row = [123, 1233]
#     # with f:
#     #     print('here')
#     #     writer = csv.writer(f)
#     #     writer.writerow(row)
#
# def connect(url):
#     print('Connecting to https://www.mangoplate.com/' + url)
#     driver.get('https://www.mangoplate.com/' + url)