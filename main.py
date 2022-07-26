
import bs4
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

r = requests.get('https://www.watsons.com.hk/', headers=headers)
print(r.text)
soup = bs4.BeautifulSoup(r.text, 'html.parser')
category = soup.find_all('e2-navigation-tab')

for cat in category:
    print(cat.text.strip())
