import bs4
import json
import xmltodict
import requests

def custom_header():
    """網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request"""
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "max-age=0",
        "Host": "www.watsons.com.hk",
        "Origin": "https://www.watsons.com.hk",
        "Referer": "https://www.watsons.com.hk/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cora",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "MMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }

def scrapyCategory():
    url = 'https://www.watsons.com.hk/'
    category_api = 'https://api.watsons.com.hk/api/v2/wtchk/categoryTree/CATEGORY_ID?fields=FULL&level=2&lang=zh_HK&curr=HKD'
    
    response = requests.get(url, headers=custom_header())
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('e2-navigation-tab')

    categories_list = []
    categories_url = []
    for cat in categories:
        cat_link = cat.find('a', href=True)

        if cat_link is not None:
            categories_list.append({'category': cat.text.strip(), 'name': cat.text.strip(), 'url': cat_link['href']})
            url_parts = cat_link['href'].split('/')
            # print(url_parts[-1], ' : ', str.isnumeric(url_parts[-1]))
            if str.isnumeric(url_parts[-1]) == True:
                new_url = category_api.replace('CATEGORY_ID', url_parts[-1])
                # print(new_url)
                ## loop sub category
                scrapySubCategory(new_url)
                
        else:
            print('No hyperlink')
    

def scrapySubCategory(url):
    categories_list = []

    header = custom_header()
    # header["cookie"] = ""
    # header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    # header["if-none-match"] = "07f9694967b6150c7dc99f5fc4c086dda:dtagent10243220606153550OOez-gzip:dtagent10243220606153550OOez"
    # header["sec-ch-ua"] = '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"'
    # header["sec-ch-ua-mobile"] = "?0"
    # header["sec-ch-ua-platform"] = "macOS"
    # header["sec-fetch-Dest"] = "document"
    # header["Sec-Fetch-Mode"] = "navigate"
    # header["Sec-Fetch-Site"] = "none"
    # header["sec-fetch-use"] = "?1"

    del header["Host"]
    del header["Origin"]
    del header["Referer"]

    response = requests.get(url, headers=header)

    if str.find(response.text, "<?xml") != -1:
        xmlresponse = xmltodict.parse(response.text)
        res = xmlresponse['elabCategoryTree']
    else:
        print(response.text)
        jsonresponse = json.loads(response.text)
        res = jsonresponse

    for categories in res['secondLevelLinks']:
        if 'childList' in categories:
            for cat in categories['childList']:
                if 'linkName' in cat and 'url' in cat:
                    try:
                        categories_list.append({'category': cat['linkName'].strip(), 'name': cat['linkName'].strip(), 'url': cat['url']})
                        # print(categories_list)
                        # item = CategoryItem()
                        # item['category'] = cat['linkName'].strip()
                        # item['name'] = cat['linkName'].strip()
                        # item['url'] = cat['url']

                        # yield item
                    except OSError as err:
                        print("OS error: {0}".format(err))
                    except ValueError:
                        print("Could not convert data to an integer.")
                    except BaseException as err:
                        print(1234567890)
                        print(cat)
                        print(f"Unexpected {err=}, {type(err)=}")
                        raise
                else:
                    print(cat)
    
    print(categories_list)

def crawler():
    
    scrapyCategory()

    return

crawler()