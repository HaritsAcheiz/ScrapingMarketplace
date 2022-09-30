"""
all function and method for scrapetsy
"""

import requests
from bs4 import BeautifulSoup

class Scrapetsy:
    # define parent class variable
    def __init__(self, url,result):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        self.result = result
    # define parent class function
    def extract(self):
        self.extract()

# Class to get popular women gift
class WomenGift(Scrapetsy):
    # define child class variable aka "Constructor"
    def __init__(self):
        super(WomenGift,self).__init__(
            url = 'https://www.etsy.com/search?q=gift+for+women&ref=hp_gbs&anchor_listing_id=737271222',
            result = {'title':'Most Popular Women Gift','description':'Class to get Most Popular Women Gift','content':[]})

    #define child class function
    def extract(self):
        try:
            with requests.Session() as session:
                response = session.get(self.url,headers=self.header)
        except:
            response = 'Invalid Format'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            soup = soup.find('ul', {'class':'wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container'})
            soup = soup.findAll('li', {'class':'wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-order-xs-0 wt-order-md-0 wt-order-lg-0 wt-show-xs wt-show-md wt-show-lg'})
            for i in soup:
                datacontent = {'image':'', 'name':'', 'solditem':'', 'badge':'', 'price':'', 'promotion':'', 'shop':'', 'link':''}
                datacontent['image'] = i.find('img')['src']
                print(datacontent['image'])

if __name__ == '__main__':
    result = WomenGift()
    result.extract()


