from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime
from WebPage import WebPage

class UleWyrobek():
    def __init__(self) -> None:
        self.url = 'https://www.ule-wyrobek.pl/'

    def get_products(self):
        scraped_products = []
        product_list = []
        ule_wyrobek = WebPage('https://www.ule-wyrobek.pl/')
        categories = ule_wyrobek.get_page_content('').find('ul', {'class': 'MenuRozwijaneKolumny MenuNormalne MenuDrzewoKategorie'}).find_all('li', {'class':'LinkiMenu'})
        start = time.time()

        for category in categories:
            category_link = category.find('a')['href']
            category_name = category.text
            ule_wyrobek.add_categories({category_name: category_link})

        for category_link in ule_wyrobek.categories:
            category = list(category_link.values())[0].split('/')[-1]
            category_name = list(category_link.keys())[0]

            category_html_content = ule_wyrobek.get_page_content(f"{ule_wyrobek.base_url}{category}")

            category_pages = int(category_html_content.find('div', {'class': 'IndexStron'}).find_all('a')[-1].text)

            for i in range(1, category_pages+1):
                category_page_html_content = ule_wyrobek.get_page_content(f"{ule_wyrobek.base_url}{category}/s={i}")
                products = category_page_html_content.find_all('div', {'class': 'Okno OknoRwd'})

                for product in products:
                    try:
                        product_link = product.find('div', {'class': 'Zobacz'}).find('a')['href']
                    except Exception as e:
                        product_link = ''

                    try:
                        product_html_content = ule_wyrobek.get_page_content(f"{product_link.split('/')[-1]}")
                    except Exception as e:
                        product_html_content = ''

                    print(f"Current product: {product_link}, Working time: {time.time()-start}")

                    try:
                        product_name = product_html_content.find('h1', {'itemprop': 'name'}).text
                    except Exception as e:
                        product_name = ''

                    try:
                        product_price = float(product_html_content.find('p', {'id': 'CenaGlownaProduktuBrutto'}).find('span')['content'])
                    except Exception as e:
                        product_price = 0.0
                    
                    try:
                        product_code = product_html_content.find('strong', {'itemprop': 'mpn'}).text
                    except Exception as e:
                        product_code = ''

                    if product_link not in scraped_products:
                        product_list.append(Product(product_name, product_price, product_link, product_code, category_name))
                        scraped_products.append(product_link)
                        print(Product(product_name, product_price, product_link, product_code, category_name))
        return product_list
        
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/ule_wyrobek.xml')