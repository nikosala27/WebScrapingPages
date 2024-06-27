from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime
from WebPage import WebPage


class Lukasiewicz():
    def __init__(self) -> None:
        self.categories = ['sprzet-pszczelarski', 'odziez-pszczelarska', 'hodowla-matek', 'weza-pszczela', 'pokarm-dla-pszczol',
                'nakretki-etykiety-sloiki-reklamy', 'pasze-dla-zwierzat', 'srodki-naturalne-i-odzywki-dla-pszczol',
                'srodki-chemiczne', 'torby-woreczki-i-pudelka-ozdobne', 'literatura', 'formy-silikonowe-swiece-z-wosku',
                'produkty-spozywcze-i-preparaty-zdrowotne', 'kosmetyki', 'prezenty-na-kazda-okazje',
                'bizuteria-z-motywami-pszczelimi-i-nie-tylko']
        self.url = 'https://pszczelnictwo.com.pl/shop/category/'

    def get_products(self):
        scraped_products = []
        product_list = []
        start = time.time()
        cursor = 1
        for category in self.categories:
            if cursor == 0:
                cursor = 1
            while cursor > 0:
                url = f'https://pszczelnictwo.com.pl/shop/category/{category}?page={cursor}'
                response = requests.get(url, headers=scraping_headers())
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    try:
                        products = soup.find_all('div', {'class': 'product-wrapper allinone'})
                    except Exception as e:
                        products = ''

                    for product in products:
                        try:
                            name = product.find_all('h3')[0].text
                        except Exception as e:
                            name = ''

                        if '&' in name:
                            name = name.replace('&', ' and ')
                        
                        try:
                            price = product.find_all('ins', {'itemprop': 'price'})[0].text
                            price = float(price.replace(',', '.').replace('zł', '').strip())
                        except Exception as e:
                            price = 0.0

                        try:
                            code = product.find_all('span', {'class': 'code'})[0].text
                        except Exception as e:
                            code = ''

                        try:
                            sales = product.find_all('span', {'class': 'onsale'})
                            on_sale = 1
                        except Exception as e:
                            sales =0
                        
                        try:
                            img = product.find_all('div', {'class': 'product-image'})[0]
                            a_tag = img.find_all('a', href=True)[0]
                            link = "https://pszczelnictwo.com.pl" + a_tag['href']
                        except Exception as e:
                            link = ''

                        on_sale = 1

                        if len(sales) == 1:
                            on_sale = 1
                        elif len(sales) == 0:
                            on_sale = 0

                        details = {
                            'code': code,
                            'name': name,
                            'price': price,
                            'on_sale': on_sale,
                            'category': category,
                            'link': link
                        }
                        
                        print(f'Current product: {details}, Working time: {time.time()-start}')
                        if link not in scraped_products:
                            product_list.append(Product(name, price, link, code, category))
                            scraped_products.append(link)
                    next_page = soup.find_all('a', {'rel': 'next'})
                    if len(next_page) > 0:
                        cursor = int(next_page[0].text)
                        random_delay(1, 3)
                    else:
                        cursor = 0
                else:
                    print(f'Connecting to url: {url} failed!')
            else:
                print(f'WEB SCRAPING OF CATEGORY {category} HAS ENDED')
        return product_list
    

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/lukasiewicz.xml')