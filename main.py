"""
This code wil get all information from www.etsy.com for popular woman gift
"""
import scrapetsy

if __name__ == '__main__':
    scraper = scrapetsy.WomenGift(webdriver_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe', driver_mode=True, detail_driver=True)
    urls = scraper.get_url(pagination=False)
    print('getting details...')
    result = []
    for i in urls:
        result.append(scraper.get_detail(i))
    print('getting details completed')

    # with open('C:/result/result.json') as f:
    #     data = json.load(f)
    #     f.close()
    # print(type(data))
    # print(data)

    scraper.create_file(data=result, filepath='C:/project/ScrapingMarketplace/result/result.csv')
