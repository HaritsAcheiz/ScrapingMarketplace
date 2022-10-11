"""
all function and method for Scrapetsy
"""

import os
import selenium.webdriver.firefox.options
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import json
import csv
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Scrapetsy:
    # define parent class variable
    def __init__(self, scheme, host, filename, params, description, webdriver_path, driver_mode, detail_driver, headers):
        self.scheme = scheme
        self.host = host
        self.params = params
        self.filename = filename
        self.description = description
        self.webdriver_path = webdriver_path
        self.driver_mode = driver_mode
        self.detail_driver = detail_driver
        self.headers = {'User-Agent': headers}

    # define parent class function
    def get_page(self):
        self.get_page()

    def get_url(self):
        self.get_url()

    def create_file(self):
        self.create_file()

# Class to get popular women gift
class WomenGift(Scrapetsy):
    # define variable in child class WomanGift
    def __init__(self, webdriver_path, driver_mode=False, detail_driver=False, headers='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'):
        super().__init__(
            # https://www.etsy.com/search?q=gift+for+women&ref=pagination&anchor_listing_id=737271222&page=1
            scheme='https',
            host='www.etsy.com',
            filename='/search',
            params={'q': 'gift+for+women', 'ref': 'pagination', 'anchor_listing_id': '737271222', 'page': '1'},
            description={'title': 'Most Popular Women Gift', 'description': 'Class to get Most Popular Women Gift'},
            webdriver_path=webdriver_path,
            driver_mode=driver_mode,
            detail_driver=detail_driver,
            headers={'User-Agent': headers}
        )

    # define function in child class WomanGift

    # Get URL Function
    def get_url(self, pagination=False):
        print('getting url...')

        # initial variable
        url_list = []
        page = 1

        # switch webdriver on
        if self.driver_mode is True:

            # switch pagination off
            if pagination is False:
                drivertype = self.webdriver_path.rsplit("/", 1)[1]

                # switch firefox geckodriver
                if drivertype == 'geckodriver.exe':

                    # config webdriver
                    options = selenium.webdriver.firefox.options.Options()
                    options.add_argument("--headless")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-translate")
                    options.add_argument(f"user-agent={self.headers['User-Agent']}")
                    driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)

                    # get url
                    url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                    driver.get(url)

                    # Wait for response until ID 'content' located
                    content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))

                    # Selecting Element to get url
                    parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                    children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                    i = 1
                    for item in children:
                        url_result = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
                        url_list.append(url_result)
                        i += 1

                    # Close driver
                    driver.quit()

                    print(f'{len(url_list)} urls collected')

                # switch chrome driver
                else:
                    options = selenium.webdriver.chrome.options.Options()
                    options.add_argument("--headless")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-translate")
                    # options.add_argument(f"--proxy-server={ip}")
                    # options.add_argument(f"user-agent={generate_user_agent()}")
                    options.add_argument(f"user-agent={self.headers['User-Agent']}")
                    driver = webdriver.Chrome(executable_path=self.webdriver_path, options=options)

                    # looping for page
                    url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                    driver.get(url)

                    # Wait for response until ID 'content' located
                    content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))

                    # Selecting Element to get url
                    parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                    children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                    i = 1
                    for item in children:
                        url_result = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute(
                            'href')
                        url_list.append(url_result)
                        i += 1

                    # Close driver
                    driver.quit()

                    print(f'{len(url_list)} urls collected')

            # switch pagination on
            if pagination is True:

                # config webdriver
                drivertype = self.webdriver_path.rsplit("/", 1)[1]
                if drivertype == 'geckodriver.exe':

                    # looping for page
                    while 1:
                        try:
                            c = 1
                            while c < 6:
                                try:
                                    options = selenium.webdriver.firefox.options.Options()
                                    options.add_argument("--headless")
                                    options.add_argument("--no-sandbox")
                                    options.add_argument("--disable-gpu")
                                    options.add_argument("--disable-translate")
                                    # options.add_argument(f"--proxy-server={ip}")
                                    # options.add_argument(f"user-agent={generate_user_agent()}")
                                    options.add_argument(f"user-agent={self.headers['User-Agent']}")
                                    driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)
                                    url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                                    driver.get(url)

                                    # Wait for response until ID 'content' located
                                    content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[64]/div/div/a[1]')))
                                    break
                                except AttributeError:
                                    print(f"{c} trials")
                                    driver.refresh()
                                    c += 1


                            # Selecting Element to get url
                            parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                            children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                            i = 0
                            for item in children:
                                try:
                                    i += 1
                                    url_result = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
                                    print(i, url_result)
                                    url_list.append(url_result)
                                except AttributeError:
                                    print('Attribute Error')
                                    break
                            page += 1
                        except AttributeError:
                            print('Attribute Error')
                            break

                    # Close driver
                    driver.quit()

                    print(f'{len(url_list)} urls collected')

                # switch chrome driver
                else:

                    # looping for page
                    while 1:
                        try:
                            options = selenium.webdriver.chrome.options.Options()
                            options.add_argument("--headless")
                            options.add_argument("--no-sandbox")
                            options.add_argument("--disable-gpu")
                            options.add_argument("--disable-translate")
                            # options.add_argument(f"--proxy-server={ip}")
                            # options.add_argument(f"user-agent={generate_user_agent()}")
                            options.add_argument(f"user-agent={self.headers['User-Agent']}")
                            driver = webdriver.Chrome(executable_path=self.webdriver_path, options=options)
                            url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                            driver.get(url)

                            # Wait for response until ID 'content' located
                            content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[64]/div/div/a[1]')))

                            # Selecting Element to get url
                            parent = content.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
                            children = parent.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
                            i = 0
                            print(page)
                            for item in children:
                                try:
                                    i += 1
                                    url_result = item.find_element(By.XPATH, f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
                                    url_list.append(url_result)
                                except AttributeError:
                                    print('Attribute Error')
                                    break
                            page += 1
                        except AttributeError:
                            print('Attribute Error')
                            break

                    # Close driver
                    driver.quit()

                    print(f'{len(url_list)} urls collected')

        # switch webdriver mode off
        else:

            # switch pagination off
            if pagination is False:
                url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                try:
                    with HTMLSession() as session:
                        response = session.get(url, headers=self.headers['User-Agent'])
                        response.html.render(wait=20, timeout=200, sleep=20)

                    # with AsyncHTMLSession() as session:
                    #     response = session.get(url, headers=self.headers['User-Agent'])
                    #     await response.html.arender()

                except ConnectionError:
                    print(f"ConnectionError: {response.status_code}")

                try:
                    soup = BeautifulSoup(response.html.html, "html.parser")
                    print(soup)
                    # response.close()
                    parent = soup.find('ul', {'class': 'wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container'})
                    children = parent.find_all('li')
                    i = 1
                    for item in children:
                        url = item.find('a', {'class': 'listing-link'})['href']
                        url_list.append(url)
                        i += 1

                except AttributeError:
                    print('AttributeError')

            # switch pagination on
            else:
                while 1:
                    url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
                    try:
                        with HTMLSession() as session:
                            response = session.get(url, headers=self.headers['User-Agent'])
                            response.html.render(wait=20, timeout=200, sleep=20)

                        # with AsyncHTMLSession() as session:
                        #     response = session.get(url, headers=self.headers['User-Agent'])
                        #     await response.html.arender()

                    except ConnectionError:
                        print(f"ConnectionError: {response.status_code}")
                        break

                    try:
                        soup = BeautifulSoup(response.html.html, "html.parser")
                        # response.close()
                        parent = soup.find('ul', {'class': 'wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container'})
                        children = parent.find_all('li')
                        i = 1
                        for item in children:
                            url = item.find('a', {'class': 'listing-link'})['href']
                            url_list.append(url)
                            i += 1
                        page += 1

                    except AttributeError:
                        print(f'{len(url_list)} urls collected')
                        break

        return url_list

    # Get Detail Function
    def get_detail(self, url):
        # initial variable
        data = {'image': '', 'title': '', 'price': '', 'outlet_name': '', 'link_outlet': '', 'item_sold': '',
                'detail': [], 'description': '', 'reviews': '', 'url': ''}

        print(f'collecting {url}')

        # detail driver on
        if self.detail_driver is True:

            # get driver type
            drivertype = self.webdriver_path.rsplit("/", 1)[1]

            # switch geckodriver
            if drivertype == 'geckodriver.exe':
                options = selenium.webdriver.firefox.options.Options()
                options.add_argument("--headless")
                driver = webdriver.Firefox(executable_path=self.webdriver_path, options=options)

                driver.get(url)
                content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))
                data['image'] = content.find_element(By.CSS_SELECTOR, 'li.carousel-pane:nth-child(1) > img:nth-child(1)').get_attribute('src')
                data['title'] = content.find_element(By.CSS_SELECTOR, 'h1.wt-text-body-03').text

                # get price
                prices1 = content.find_element(By.XPATH, "//p[@class='wt-text-title-03 wt-mr-xs-1']")
                prices2 = prices1.find_elements(By.TAG_NAME, 'span')
                try:
                    data['price'] = prices2[-1].text
                except IndexError:
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

            # switch chromedriver
            else:
                options = selenium.webdriver.chrome.options.Options()
                options.add_argument("--headless")
                driver = webdriver.Chrome(executable_path=self.webdriver_path, options=options)

                driver.get(url)
                content = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))
                data['image'] = content.find_element(By.CSS_SELECTOR, 'li.carousel-pane:nth-child(1) > img:nth-child(1)').get_attribute(
                    'src')
                data['title'] = content.find_element(By.CSS_SELECTOR, 'h1.wt-text-body-03').text

                # get price
                prices1 = content.find_element(By.XPATH, "//p[@class='wt-text-title-03 wt-mr-xs-1']")
                prices2 = prices1.find_elements(By.TAG_NAME, 'span')
                try:
                    data['price'] = prices2[-1].text
                except IndexError:
                    data['price'] = prices1.text

                data['outlet_name'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').text
                data['link_outlet'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').get_attribute(
                    'href')

                # get sales
                try:
                    data['item_sold'] = content.find_element(By.XPATH, '/html/body/main/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/span[2]').text
                except AttributeError:
                    data['item_sold'] = '0'

                # Get Detail
                try:
                    detail_list = []
                    details = content.find('ul', {'class': 'wt-text-body-01'}).find_all('li')
                    for j in details:
                        detail_list.append(j.text)
                    data['detail'] = detail_list
                except AttributeError:
                    data['detail'] = ''

                data['description'] = content.find_element(By.CSS_SELECTOR, 'p.wt-break-word').text
                data['reviews'] = content.find_element(By.CSS_SELECTOR, 'h2.wt-mr-xs-2').text
                data['url'] = url

                driver.quit()

        # detail driver off
        else:
            try:
                with HTMLSession() as session:
                    response = session.get(url, headers=self.headers['User-Agent'])
                    response.html.render(wait=15, timeout=100)

            except ConnectionError:
                print(f"ConnectionError: {response.status_code}")

            # try:
            #     with requests.Session() as session:
            #         response = session.get(url, headers=self.headers['User-Agent'])

            # except ConnectionError:
            #     print(f"ConnectionError: {response.status_code}")

            soup = BeautifulSoup(response.html.html, "html.parser")
            # soup = BeautifulSoup(response.text, "html.parser")
            response.close()
            parent = soup.find('main', {'id': 'content'})
            data['image'] = parent.find('li', {'class': 'carousel-pane'}).find('img')['src']
            data['title'] = parent.find('h1', {'class': 'wt-text-body-03'}).text

            # Get Price
            prices1 = parent.find('p', {'class': 'wt-text-title-03 wt-mr-xs-1'})
            prices2 = prices1.find_all('span')
            try:
                data['price'] = prices2[-1].text
            except IndexError:
                data['price'] = prices1.text

            data['outlet_name'] = parent.find('a', {'class': 'wt-text-link-no-underline'}).find('span').text
            data['link_outlet'] = parent.find('a', {'class': 'wt-text-link-no-underline'})['href']

            # Get sales
            try:
                data['item_sold'] = parent.find('div', {'class': 'wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2'}).find('span', {'class': 'wt-text-caption '}).text
            except AttributeError:
                data['item_sold'] = 0

            # Get Detail
            try:
                detail_list = []
                details = parent.find('ul', {'class': 'wt-text-body-01'}).find_all('li')
                for j in details:
                    detail_list.append(j.text)
                data['detail'] = detail_list
            except AttributeError:
                data['detail'] = ''

            data['description'] = parent.find('p', {'class': 'wt-break-word'}).text
            data['reviews'] = parent.find('h2', {'class': 'wt-mr-xs-2'}).text
            data['url'] = url

        return data

    def create_file(self, data, filepath='/result/result.json'):
        print('Creating file...')
        ext = filepath.split(".")[-1]
        folder = filepath.rsplit("/", 1)[0]
        if ext == 'json':
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass
            with open(filepath, 'w+', encoding="utf-8", newline='') as f:
                json.dump(data, f)
                f.close()

        elif ext == 'csv':
            try:
                os.mkdir(folder)
            except FileExistsError:
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
