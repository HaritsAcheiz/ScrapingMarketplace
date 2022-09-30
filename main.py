"""
This code wil get all information from www.etsy.com for popular woman gift
"""
import scrapetsy

if __name__ == '__main__':
    result = scrapetsy.WomenGift()
    result.extract()
    # view()
    # load()
