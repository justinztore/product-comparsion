import json
from re import T
import requests
import time
import pandas as pd
from datetime import datetime

def custom_header():
    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cora",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "MMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    

def getProductDetail(products_list, products, category_code):
    for product in products:
        #print(product)
        description = ''
        if 'description' in product:
            description = product['description']
        
        elabProductName = product['elabProductName']
        gtmCategoryPath = product['gtmCategoryPath']
        brand = product['masterBrand']['name']
        name = product['name']
        code = product['code']
        currency = product['price']['currencyIso']
        price = product['price']['value']

        promotionFirstTag = ''
        if 'promotionFirstTag' in product:
            promotionFirstTag = product['promotionFirstTag']

        # priceRange
        reviewAvgRating = product['reviewAvgRating']

        url = ''
        if 'promotionFirstTag' in product:
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
    if current_page != 0:
        url = f'https://api.watsons.com.hk/api/v2/wtchk/products/search?fields=FULL&query=%3Arelevance%3Acategory%3A{category_code}&pageSize=32&currentPage={current_page}&sort=price-asc&lang=zh_HK&curr=HKD'
    else:
        url = f'https://api.watsons.com.hk/api/v2/wtchk/products/search?fields=FULL&query=%3Arelevance%3Acategory%3A{category_code}&pageSize=32&sort=price-asc&lang=zh_HK&curr=HKD'

    response = requests.get(url, headers=custom_header())
    jsonresponse = json.loads(response.text)
    res = jsonresponse
    # categories = soup.find_all('e2-navigation-tab')

    # print(res['pagination'])

    currentPage = res['pagination']['currentPage']
    totalPages = res['pagination']['totalPages']

    #print(res['products'])

    products = res['products']

    return currentPage, totalPages, products


def crawler(parameters):
    products_list = []

    print(f"pass in parameters : {parameters}")

    category_code = parameters['category_code']

    currentPage, totalPages, products = scrapProduct(category_code, 0)
    print('currentPage: ', currentPage)
    print('totalPages: ', totalPages)

    products_list = getProductDetail(products_list, products, category_code)

    if(totalPages > 1):
        current_page = 1
        while totalPages > current_page:
            cp, tp, p = scrapProduct(category_code, current_page)
            
            products_list = getProductDetail(products_list, products, category_code)
            current_page = current_page + 1

    # print(products_list)

    data = pd.DataFrame(products_list)
    print('-------------------------')
    # print(data)
    print('=========================')

    return data