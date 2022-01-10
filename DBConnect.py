#DBConnect.py

import pymysql
import csv

def insertDB(dataDic):

    if '카테고리' in dataDic.keys():
        category = str(dataDic['카테고리']).strip()
    else:
        category = None
    
    if '이름' in dataDic.keys():
        R_name = str(dataDic['이름']).strip()
    else:
        R_name = None

    if 'url' in dataDic.keys():
        url = dataDic['url']
    else:
        url = None

    if '주소' in dataDic.keys():
        addr = str(dataDic['주소']).strip()
        x = addr.split(' ')
        R_gu = str(x[1]).strip()
        R_dong = str(x[2]).strip()
    else:
        addr = None
        R_gu = None
        R_dong = None

    if '전화번호' in dataDic.keys():
        tel = str(dataDic['전화번호']).strip()
    else:
        tel = None
    
    if '음식종류' in dataDic.keys():
        kind = str(dataDic['음식종류']).strip()
    else:
        kind = None
    
    if '평점' in dataDic.keys():
        rating = str(dataDic['평점']).strip()
    else:
        rating = None

    if '영업시간' in dataDic.keys():
        open_time = str(dataDic['영업시간']).strip()
    else:
        open_time = None

    if '휴일' in dataDic.keys():
        holiday = str(dataDic['휴일']).strip()
    else:
        holiday = None

    if '메뉴' in dataDic.keys():
        menu = str(dataDic['메뉴']).strip()
        menu = menu.replace('\n', ' ')
    else:
        menu = None

    # if 'reviews' in dataDic.keys():
    #     reviews = '|'.join(dataDic['reviews'])
    # else:
    #     reviews = None

    # try:
    #     conn = pymysql.connect(host='localhost', user='root', password='1234', port=3306, db='hotplace', charset='utf8')
    #     print ('values: '+category+', '+R_name+', '+R_gu+', '+R_dong+', '+addr+', '+tel+', '+kind+', '+rating+', '+open_time+', '+holiday+', '+menu)
    #     with conn.cursor() as cursor:
    #         sql = 'INSERT INTO s_restaurants (category, R_name, R_gu, R_dong, addr, tel, kind, rating, open_time, holiday, menu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #         cursor.execute(sql, (category, R_name, R_gu, R_dong, addr, tel, kind, rating, open_time, holiday, menu))
    #         conn.commit()
    # finally:
    #     conn.close()

    print(
        'values: ' + url + ', '+ category + ', ' + R_name + ', ' + R_gu + ', ' + R_dong + ', ' + addr + ', ' + tel + ', ' + kind + ', ' + rating + ', ' + open_time + ', ' + holiday + ', ' + menu)
    f = open('db.csv', 'a', newline='', encoding="utf-8")
    field_row = ['category', 'R_name', 'R_gu', 'R_dong', 'addr', 'tel', 'kind', 'rating', 'open_time', 'holiday', 'menu', 'reviews']
    # row = [category, R_name, R_gu, R_dong, addr, tel, kind, rating, open_time, holiday, menu, reviews]
    row = [category, url, R_name, R_gu, R_dong, addr, tel, kind, rating, open_time, holiday, menu]
    with f:
        writer = csv.writer(f, dialect='excel')
        # writer = csv.DictWriter(f, dialect='excel', field_names=field_row)
        # restaurant_record = {'category': category, 'R_name': R_name, 'R_gu': R_gu, 'R_dong': R_dong, 'address': addr,
        #                      'tel': tel, 'kind': kind, 'rating': rating, 'open_time': open_time, 'holiday': holiday,
        #                      'menu': menu, 'reviews': reviews}
        # writer.writerow(restaurant_record)
        writer.writerow(row)