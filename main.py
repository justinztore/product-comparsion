
import bs4
import requests
import json

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
    

def getProductDetail(products):

    for product in products:
        #print(product)

        description = ''
        if 'description' in product:
            description = product['description']
        elabProductName = product['elabProductName']
        gtmCategoryPath = product['gtmCategoryPath']
        brand = product['masterBrand']['name']
        name = product['name']
        currency = product['price']['currencyIso']
        price = product['price']['value']

        promotionFirstTag = ''
        if 'promotionFirstTag' in product:
            promotionFirstTag = product['promotionFirstTag']

        # priceRange
        reviewAvgRating = product['reviewAvgRating']
        url = product['url']
        image = product['images'][0]['url']
        # images
        print(elabProductName)

    print('-------------------- Separate Line -------------------------')


def scrapProduct(current_page):
    if current_page != 0:
        url = f'https://api.watsons.com.hk/api/v2/wtchk/products/search?fields=FULL&query=%3Arelevance%3Acategory%3A010301&pageSize=32&currentPage={current_page}&lang=zh_HK&curr=HKD'
    else:
        url = 'https://api.watsons.com.hk/api/v2/wtchk/products/search?fields=FULL&query=%3Arelevance%3Acategory%3A010301&pageSize=32&lang=zh_HK&curr=HKD'

    response = requests.get(url, headers=custom_header())
    jsonresponse = json.loads(response.text)
    res = jsonresponse
    # categories = soup.find_all('e2-navigation-tab')

    print(res['pagination'])

    currentPage = res['pagination']['currentPage']
    totalPages = res['pagination']['totalPages']

    #print(res['products'])

    products = res['products']

    return currentPage, totalPages, products

currentPage, totalPages, products = scrapProduct(0)

print('currentPage: ', currentPage)
print('totalPages: ', totalPages)
# print('products: ', products)

getProductDetail(products)

if(totalPages > 1):
    current_page = 1
    while totalPages > current_page:
        cp, tp, p = scrapProduct(current_page)
        
        getProductDetail(p)
        current_page = current_page + 1
