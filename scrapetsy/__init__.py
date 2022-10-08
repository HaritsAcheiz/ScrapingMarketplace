"""
all function and method for scrapetsy
"""
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import json
import csv
import requests
from bs4 import BeautifulSoup


class Scrapetsy:
    # define parent class variable
    def __init__(self, scheme, host, filename, params, description, webdriver_path, driver_mode, headers):
        self.scheme = scheme
        self.host = host
        self.params = params
        self.filename = filename
        self.description = description
        self.webdriver_path = webdriver_path
        self.driver_mode = driver_mode
        self.headers = headers

    # define parent class function
    def get_page(self):
        self.get_page()

    def get_url(self):
        self.get_url()

    def to_csv(self):
        self.to_csv()

# Class to get popular women gift


class WomenGift(Scrapetsy):
    # define variable in child class WomanGift
    def __init__(self, webdriver_path, driver_mode = False, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}):
        super().__init__(
            # https://www.etsy.com/search?q=gift+for+women&ref=pagination&anchor_listing_id=737271222&page=1
            scheme='https',
            host='www.etsy.com',
            filename='/search',
            params={'q': 'gift+for+women', 'ref': 'pagination', 'anchor_listing_id': '737271222', 'page': '1'},
            description={'title': 'Most Popular Women Gift', 'description': 'Class to get Most Popular Women Gift'},
            webdriver_path=webdriver_path,
            driver_mode = driver_mode,
            headers = headers
        )

    # define function in child class WomanGift

    # Get URL Function
    def get_url(self, pagination=False):
        print('getting url...')

        # initial variable
        url_list = []
        page = 1
        i = 1
        if self.driver_mode is True:
            if pagination is False:
                # config webdriver
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)

                # looping for page
                url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                driver.get(url)

                # Wait for response until ID 'content' located
                content = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'content')))

                # Selecting Element to get url
                parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                for item in children:
                    url = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
                    url_list.append(url)
                    i += 1

                # Close driver
                driver.quit()

                print('getting url completed')

            if pagination is True:
                # config webdriver
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)

                # looping for page
                while 1:
                    try:
                        url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                        driver.get(url)

                        # Wait for response until ID 'content' located
                        content = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'content')))

                        # Selecting Element to get url
                        parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                        children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                        for item in children:
                            url = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
                            url_list.append(url)
                            i += 1
                    except Exception:
                        break
                # Close driver
                driver.quit()

                print('getting url completed')
        else:
            url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
            try:
                with requests.Session() as session:
                    response = session.get(url, headers=self.headers)
            except Exception:
                response = 'invalid format'
            if response != 'invalid format':
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    parent = soup.find('ul', {'class': 'wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container'})
                    children = parent.find_all('li')
                    for item in children:
                        url = item.find('a', {'class':'listing-link.wt-display-inline-block.b105b708a1788d6d2.logged'})['href']
                        url_list.append(url)
                        i += 1
                else:
                    print(response.status_code)

        return url_list

    # Get Detail Function
    def get_detail(self, url):
        # initial variable
        data = {'image': '', 'title': '', 'price': '', 'outlet_name': '', 'link_outlet': '', 'item_sold': '',
                'detail': [], 'description': '', 'reviews': '', 'url': ''}

        print(f'collecting {url}')

        if self.driver_mode is True:

            # config webdriver
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)

            driver.get(url)
            content = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'content')))
            data['image'] = content.find_element(By.CSS_SELECTOR, 'li.carousel-pane:nth-child(1) > img:nth-child(1)').get_attribute('src')
            data['title'] = content.find_element(By.CSS_SELECTOR, 'h1.wt-text-body-03').text

            # get price
            prices1 = content.find_element(By.XPATH, "//p[@class='wt-text-title-03 wt-mr-xs-1']")
            prices2 = prices1.find_elements(By.TAG_NAME, 'span')
            try:
                data['price'] = prices2[-1].text
            except Exception:
                data['price'] = prices1.text
            data['outlet_name'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').text
            data['link_outlet'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').get_attribute('href')
            data['item_sold'] = content.find_element(By.XPATH, '/html/body/main/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/span[2]').text

            # get detail
            details = content.find_element(By.CSS_SELECTOR, 'ul.wt-text-body-01')
            details = details.find_elements(By.TAG_NAME, 'li')
            detail_list = []
            for j in details:
                detail_list.append(j.text)
            data['detail'] = detail_list

            data['description'] = content.find_element(By.CSS_SELECTOR, 'p.wt-break-word').text
            data['reviews'] = content.find_element(By.CSS_SELECTOR, 'h2.wt-mr-xs-2').text
            data['url'] = url

            driver.quit()

        else:
            try:
                with requests.Session() as session:
                    response = session.get(url, headers=self.headers)
            except Exception:
                response = 'invalid format'
            if response != 'invalid format':
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    parent = soup.find('main', {'id': 'content'})
                    data['image'] = parent.find('li', {'class': 'carousel-pane'}).find('img')['src']
                    data['title'] = parent.find('h1', {'class':'wt-text-body-03'}).text

                    # Get Price
                    prices1 = parent.find('p', {'class':'wt-text-title-03 wt-mr-xs-1'})
                    prices2 = prices1.find_all('span')
                    try:
                        data['price'] = prices2[-1].text
                    except Exception:
                        data['price'] = prices1.text

                    data['outlet_name'] = parent.find('a',{'class':'wt-text-link-no-underline'}).find('span').text
                    data['link_outlet'] = parent.find('a',{'class':'wt-text-link-no-underline'})['href']
                    data['item_sold'] = parent.find('div', {'class':'wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2'}).find('span', {'class':'wt-text-caption '}).text

                    # Get Detail
                    detail_list = []
                    details = parent.find('ul', {'class':'wt-text-body-01'}).find_all('li')
                    for j in details:
                        detail_list.append(j.text)
                    data['detail'] = detail_list
                    data['description'] = parent.find('p', {'class':'wt-break-word'}).text
                    data['reviews'] = parent.find('h2', {'class':'wt-mr-xs-2'}).text
                    data['url'] = url
                else:
                    print(response.status_code)

        return data

    def to_file(self, data, filepath):
        print('Creating file...')
        ext = filepath.split(".")[-1]
        folder = filepath.rsplit("/", 1)[0]
        if ext == 'json':
            try:
                os.mkdir(folder)
            except Exception:
                pass
            with open(filepath, 'w+', encoding="utf-8", newline='') as f:
                json.dump(data, f)
                f.close()

        elif ext == 'csv':
            try:
                os.mkdir(folder)
            except Exception:
                pass
            with open(filepath, 'w+', encoding="utf-8", newline='') as f:
                headers = ['image', 'title', 'price', 'outlet_name', 'link_outlet', 'item_sold', 'detail',
                           'description', 'reviews', 'url']
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for i in data:
                    writer.writerow(i)
                f.close()

        else:
            print('Unknown format file')
        print(f'{filepath} created')


if __name__ == '__main__':
    scraper = WomenGift(webdriver_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe', driver_mode=True)
    urls = scraper.get_url(pagination=True)
    print('getting details...')
    result = []
    for i in urls:
        result.append(scraper.get_detail(i))
    print('getting details completed')
    print(result)

    # with open('C:/result/result.json') as f:
    #     data = json.load(f)
    #     f.close()
    # print(type(data))
    # print(data)

    scraper.to_file(data=result, filepath='C:/project/ScrapingMarketplace/result/result.csv')
