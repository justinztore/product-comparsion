import scrapy
import bs4
import json
import xmltodict

from crawler.items import CategoryItem

class WatsonsSpider(scrapy.Spider):
    name = 'watsons'
    allowed_domains = ['www.watsons.com.hk']
    start_urls = ['https://www.watsons.com.hk/']
    category_api = 'https://api.watsons.com.hk/api/v2/wtchk/categoryTree/CATEGORY_ID?fields=FULL&level=2&lang=zh_HK&curr=HKD'

    def parse(self, response):
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
                    new_url = self.category_api.replace('CATEGORY_ID', url_parts[-1])
                    # print(new_url)
                    ## loop sub category
                    yield scrapy.Request(
                        new_url,
                        callback = self.parse_category,
                        dont_filter = True
                    )
            else:
                print('No hyperlink')
        

        # print(categories_list)

        pass

    def parse_category(self, response):
        categories_list = []

        if str.find(response.text, "<?xml") != -1:
            xmlresponse = xmltodict.parse(response.text)
            res = xmlresponse['elabCategoryTree']
        else:
            jsonresponse = json.loads(response.text)
            res = jsonresponse

        for categories in res['secondLevelLinks']:
            if 'childList' in categories:
                for cat in categories['childList']:
                    if 'linkName' in cat and 'url' in cat:
                        try:
                            categories_list.append({'category': cat['linkName'].strip(), 'name': cat['linkName'].strip(), 'url': cat['url']})
                            # print(categories_list)
                            item = CategoryItem()
                            item['category'] = cat['linkName'].strip()
                            item['name'] = cat['linkName'].strip()
                            item['url'] = cat['url']

                            yield item
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
        # print(categories_list)

        # pass
    
    def parse_category_product(self, response):

        pass