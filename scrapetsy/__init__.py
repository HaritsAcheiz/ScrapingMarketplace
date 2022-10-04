"""
all function and method for scrapetsy
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Scrapetsy:
    # define parent class variable
    def __init__(self, scheme, host, filename, params, description):
        self.scheme = scheme
        self.host = host
        self.params = params
        self.filename = filename
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        self.description = description

    # define parent class function
    def get_page(self):
        self.get_page()

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
            description = {'title':'Most Popular Women Gift','description':'Class to get Most Popular Women Gift'})

    # define function in child class WomanGift

    # Get URL Function
    def get_url(self):
        print('getting url...')

        # config webdriver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe', options=options)

        # initial variable
        page = 1

        #looping for page
        # while 1:
        #     try:
        url = f"{self.scheme}://{self.host}{self.filename}?q={self.params['q']}&ref={self.params['ref']}&anchor_listing_id={self.params['anchor_listing_id']}&page={str(page)}"
        driver.get(url)

        # Wait for response until ID 'content' located
        content = WebDriverWait(driver,10).until(ec.presence_of_element_located((By.ID,'content')))

        # Selecting Element to get url
        parent = content.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul')
        children = parent.find_elements(By.XPATH,'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li')
        i = 1
        urls = []
        for item in children:
            url = item.find_element(By.XPATH,f'/html/body/main/div/div[1]/div/div[3]/div[5]/div[4]/div[9]/div[1]/div/div/ul/li[{i}]/div/div/a[1]').get_attribute('href')
            urls.append(url)
            i+=1
        # except:
        #     break


        # Close driver
        driver.quit()

        print('getting url completed')

        return urls

    # Get Detail Function
    def get_detail(self,urls):
        print('getting details...')

        # config webdriver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe', options=options)
        result = []
        data = {'image':'', 'title':'', 'price':'', 'outlet_name':'', 'link_outlet':'', 'item_sold':'', 'detail':[], 'description':'', 'reviews':'', 'url':''}
        for i in urls:
            driver.get(i)
            content = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.wt-pt-xs-5')))
            data['image'] = content.find_element(By.CSS_SELECTOR,'li.carousel-pane:nth-child(1) > img:nth-child(1)').get_attribute('src')
            data['title'] = content.find_element(By.CSS_SELECTOR, 'h1.wt-text-body-03').text
            data['price'] = content.find_element(By.CSS_SELECTOR, 'wt-text-title-03 > span:nth-child(2)').text
            data['outlet_name'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').text
            data['link_outlet'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1)').get_attribute('href')
            data['item_sold'] = content.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3)').text
            details = content.find_element(By.CSS_SELECTOR, 'ul.wt-text-body-01')
            details = details.find_elements(By.TAG_NAME, 'li')
            for j in details:
                data['detail'].append(j)
            data['description'] = content.find_element(By.CSS_SELECTOR, 'p.wt-break-word').text
            data['reviews'] = content.find_element(By.CSS_SELECTOR, 'h2.wt-mr-xs-2').text
            data['url'] = i
        result.append(data)

        driver.quit()
        print('getting details completed')

        return result

        # f = open('response.html', 'w+', encoding="utf-8")
        # f.write(response)
        # f.close()


            # link_soup = soup.findAll('div', {'class':'js-merch-stash-check-listing v2-listing-card wt-mr-xs-0 search-listing-card--desktop listing-card-experimental-style appears-ready'})
            # for i in link_soup:
            #     result = i.find('a', href=True)['href']
            #     self.result['content'].append(result)
            #
            # page_soup = soup.find('ul', {'class':'wt-action-group wt-list-inline search-pagination'})
            # page_soup = page_soup.findAll('span', {'class':'wt-screen-reader-only'})
            # lastpage = page_soup[-1].text
            #
            # print(f'page {page} collected')
            # page += 1
        # return self.result['content']

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
    urls = result.get_url()
    result.get_detail(urls)
    print(result)




