
from urllib import request
import bs4
import json
import xmltodict
import requests
import time
import pandas as pd
from datetime import datetime
import re

JSESSIONID = ''
LBI = ''

def get_cokkies():

    if JSESSIONID == '':
        response = requests.get('https://www.hktvmall.com/')
        print(response.cookies.get_dict())

        cookies = json.loads(response.cookies.get_dict())

        JSESSIONID = cookies['JSESSIONID']
        LBI = cookies['LBI']

        return JSESSIONID, LBI
    else:
        print('JSESSIONID is not empty')
        return JSESSIONID, LBI
        

def custom_header():
    # JSESSIONID, LBI = get_cokkies()
    JSESSIONID, LBI = '4FA8109F2106A924D302740D45A27955', -159110788

    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "186",
        #"Cookie": "ott-uuid=8d5ca6b9-9880-4c11-9041-df43b58ccd94; device-type=desktop-web; _fbp=fb.1.1661006563162.1661875918; _ALGOLIA=anonymous-ed651703-3681-45ae-be13-86ab92660dd4; _gid=GA1.2.332039707.1661006563; _ga=GA1.2.1834688676.1661006563; JSESSIONID=E8BFFDAB750B6CE3267010B7BD6EACE9; LBI=-159110788; _gat_UA-55283480-1=1; _gat_UA-68175808-1=1; _ga_3NCT4DYDM1=GS1.1.1661184936.8.0.1661184936.0.0.0",
        "Cookie": f"ott-uuid=8d5ca6b9-9880-4c11-9041-df43b58ccd94; device-type=desktop-web; _fbp=fb.1.1661006563162.1661875918; _ALGOLIA=anonymous-ed651703-3681-45ae-be13-86ab92660dd4; _gid=GA1.2.332039707.1661006563; LBI={LBI}; JSESSIONID={JSESSIONID}; _ga_3NCT4DYDM1=GS1.1.1661322165.11.1.1661322166.0.0.0; _ga=GA1.1.1834688676.1661006563",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.hktvmall.com",
        "Origin": "https://www.hktvmall.com",
        "Referer": "https://www.hktvmall.com/hktv/zh/%E8%AD%B7%E8%86%9A%E5%8C%96%E5%A6%9D/%E9%9D%A2%E9%83%A8%E8%AD%B7%E7%90%86%E8%AD%B7%E8%86%9A/main/search?q=%3Arelevance%3Astreet%3Amain%3Acategory%3AAA16050000000",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "MMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
# https://www.hktvmall.com/hktv/zh/%E8%AD%B7%E8%86%9A%E5%8C%96%E5%A6%9D/%E9%9D%A2%E9%83%A8%E8%AD%B7%E7%90%86%E8%AD%B7%E8%86%9A/main/search?q=%3Arelevance%3Astreet%3Amain%3Acategory%3AAA16050000000


def getProductDetail(products_list, products, category_code):
    for product in products:
        #print(product)
        description = ''
        if 'description' in product:
            description = product['description']
        
        elabProductName = product['name']

        gtmCategoryPath = ''
        for cat in product['categories']:
            gtmCategoryPath += cat['name']+','

        brand = product['brandName']
        name = product['name']
        code = product['baseProduct']

        for _price in product['priceList']:
            if len(product['priceList']) > 1:
                if _price['priceType'] == 'DISCOUNT':
                    currency = _price['currencyIso']
                    price = _price['value']
            else:
                currency = _price['currencyIso']
                price = _price['value']

        promotionFirstTag = ''
        # if 'promotionFirstTag' in product:
        #     promotionFirstTag = product['promotionFirstTag']

        # averageRating
        reviewAvgRating = ''
        if 'averageRating' in product:
            reviewAvgRating = product['averageRating']

        url = ''
        if 'url' in product:
            url = product['url']

        image = ''
        if 'url' in product['images'][0]:
            image = product['images'][0]['url']

        # images
        # print(elabProductName)
        now = datetime.now()

        products_list.append({'code':f'watsons_{category_code}_{code}', 'platform':'watsons', 'product_code':code, 'category_code':category_code, 'name':elabProductName, 'description':description, 'category':gtmCategoryPath, 'brand':brand, 'currency':currency, 'price':price, 'promotion_tag': promotionFirstTag, 'review_avg_rating':reviewAvgRating, 'url':url, 'image':image, 'updated_at' : now.strftime("%Y-%m-%d %H:%M:%S")})

    print('-------------------- Separate Line -------------------------')

    return products_list


def scrapProduct(category_code, current_page):
    url = 'https://www.hktvmall.com/hktv/zh/ajax/search_products'

    parameters = {
        'query': ':relevance:street:main:category:AA16050000000:',
        #'query': '"":relevance:category:AA16050000000:zone:beautynhealth:street:main:',
        'currentPage': 0,
        'pageSize': 60,
        'pageType': 'searchResult',
        'categoryCode': 'AA16050000000',
        'CSRFToken': '112046bb-b84a-44a1-8c1c-4492c52fb8d0'
    }

    # for pam in parameters:
    #     url += f'{pam}={parameters[pam]}&'

    # print(url)

    # response = requests.post(url, headers=custom_header())
    response = requests.post(url, data=parameters, headers=custom_header())
    #print(response.text)
    jsonresponse = json.loads(response.text)
    res = jsonresponse
    # categories = soup.find_all('e2-navigation-tab')

    # print(res['pagination'])

    currentPage = res['pagination']['currentPage']
    pageSize = res['pagination']['pageSize']
    numberOfPages = res['pagination']['numberOfPages']

    #print(res['products'])

    products = res['products']

    return currentPage, pageSize, numberOfPages, products


def crawler(parameters):
    products_list = []

    print(f"pass in parameters : {parameters}")

    category_code = parameters['category_code']

    currentPage, totalPages, numberOfPages, products = scrapProduct(category_code, 0)
    print('currentPage: ', currentPage)
    print('totalPages: ', totalPages)
    print('numberOfPages: ', numberOfPages)

    products_list = getProductDetail(products_list, products, category_code)

    # if(totalPages > 1):
    #     current_page = 1
    #     while totalPages > current_page:
    #         cp, tp, p = scrapProduct(category_code, current_page)
            
    #         products_list = getProductDetail(products_list, products, category_code)
    #         current_page = current_page + 1

    # # print(products_list)

    data = pd.DataFrame(products_list)
    print('-------------------------')
    # print(data)
    print('=========================')

    return data

crawler({'category_code':'0'})

#session = requests.Session()
#response = requests.get('https://www.hktvmall.com/')
#print(response.cookies.get_dict())
