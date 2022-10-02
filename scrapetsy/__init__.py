"""
all function and method for scrapetsy
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Scrapetsy:
    # define parent class variable
    def __init__(self, scheme, host, filename, params, result):
        self.scheme = scheme
        self.host = host
        self.params = params
        self.filename = filename
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        self.result = result
    # define parent class function

    # def get_page(self):
    #     self.get_page()

    def get_url(self):
        self.get_url()

    # def run(self):
    #     self.get_page()
    #     self.get_url()

# Class to get popular women gift
class WomenGift(Scrapetsy):
    # define variable in child class WomanGift
    def __init__(self):
        super(WomenGift,self).__init__(
            # https://www.etsy.com/search?q=gift+for+women&ref=pagination&anchor_listing_id=737271222&page=1
            scheme = 'https', #://
            host = 'www.etsy.com',
            filename = '/search', #?
            params = {'q':'gift+for+women', 'ref':'pagination', 'anchor_listing_id':'737271222', 'page':'1'},
            result = {'title':'Most Popular Women Gift','description':'Class to get Most Popular Women Gift','content':['']})

    # define function in child class WomanGift

    def get_url(self,page):
        print('getting url...')
        # real access to web
        try:
            driver = webdriver.Firefox(executable_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe')
            # url = 'https://www.etsy.com/search?q=gift+for+women&ref=pagination&anchor_listing_id=737271222&page=1'
            url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={page}"
            driver.get(url)
            time.sleep(5)
            response = driver.page_source

        except:
            response = 'Invalid Format'

        soup = BeautifulSoup(response, 'html.parser')

        # f = open('response.html', 'w+', encoding="utf-8")
        # f.write(response)
        # f.close()

        # checking file response.html
        # soup = BeautifulSoup(open('response.html', encoding = 'utf-8'),'html.parser')

        soup = soup.findAll('div', {'class':'js-merch-stash-check-listing v2-listing-card wt-mr-xs-0 search-listing-card--desktop listing-card-experimental-style appears-ready'})
        for i in soup:
            result = i.find('a', href=True)['href']
            print(result)

        # collecting data
            # datacontent = {'image': '', 'name': '', 'solditem': '', 'badge': '', 'price': '', 'promotion': '',
            #                'shop': '', 'link': ''}
            # soup = BeautifulSoup(response.text, 'html.parser')
            # soup = soup.find('ul', {'class':'wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container'})
            # soup = soup.findAll('li')
            # for i in soup:
            # #     if i.find('img') != None:
            # #         datacontent['image'] = i.find('img')['src']
            # #     else:
            # #         None
            #     if i.find('h3',{'class':'wt-text-caption v2-listing-card__title wt-text-truncate'}) != None:
            #         datacontent['name'] = i.find('h3',{'class':'wt-text-caption v2-listing-card__title wt-text-truncate'}).text
            #     else:
            #         None
            #     self.result['content'].append(datacontent)
            # # for i in self.result['content']:
            # print(self.result['content'])

if __name__ == '__main__':
    result = WomenGift()
    result.get_url('1')



