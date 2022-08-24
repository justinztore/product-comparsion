import bs4
import json
import xmltodict
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
        "Host": "www.hktvmall.com",
        "Origin": "https://www.hktvmall.com",
        "Referer": "https://www.hktvmall.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "MMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }

def scrapyCategory():
    url = 'https://www.hktvmall.com/hktv/zh/beautynhealth'
    
    response = requests.get(url, headers=custom_header())
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('div', {"class": "subnav"}).find_all('li')
    # categories = navigation.find_all('li')

    categories_list = []
    data = pd.DataFrame()
    now = datetime.now()

    for cat in categories:
        cat_link = cat.find('a', href=True)
        cat_name = cat_link.getText().strip()
        
        if cat_link is not None and cat_name != '':
            cat_main_code = cat_link['data-maincat']
            cat_code = cat_link['data-cat']
            #print(cat_link['href'])
            print(cat_link.getText())
            print(cat_main_code)
            print(cat_code)

            if cat_main_code == cat_code:
                # categories_list.append({'category': cat.text.strip(), 'name': cat.text.strip(), 'url': f"{url}{cat_link['href']}"})
                url_parts = cat_link['href'].split('/')
                # print(url_parts)

                try:
                    categories_list.append({'type' : 'category', 'platform' : 'hktvmall', 'name': cat_name, 'url': cat_link['href'], 'updated_at' : now.strftime("%Y-%m-%d %H:%M:%S")})
                except OSError as err:
                    print("OS error: {0}".format(err))
                except ValueError:
                    print("Could not convert data to an integer.")
                except BaseException as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                    raise

                # if str.isnumeric(url_parts[-1]) == True:
                #     new_url = category_api.replace('CATEGORY_ID', url_parts[-1])
                #     # print(new_url)
                #     ## loop sub category
                #     temp = scrapySubCategory(new_url)
                #     categories_list = categories_list + temp
            else:
                print('No category name')
        else:
            print('No hyperlink')
    
    data = pd.DataFrame(categories_list)
    print('-------------------------')
    # print(data)
    print('=========================')

    return data

def crawler(parameters):
    print(f"pass in parameters : {parameters}")
    return scrapyCategory()