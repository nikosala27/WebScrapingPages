from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime
from WebPage import WebPage


class Apikoz():
    def __init__(self) -> None:
        self.url = 'https://apikoz.pl/'

    def get_products(self):
        product_list = []
        scraped_products = []
        apikoz = WebPage('https://apikoz.pl/')
        start = time.time()
        xml_content = requests.get('https://apikoz.pl/wp-sitemap-posts-product-1.xml')
        xml_content_soup = BeautifulSoup(xml_content.text, "xml")

        product_links = [link.text for link in xml_content_soup.find_all('loc')]
        
        for link in product_links:
            product_webpage = WebPage(link)
            product_name = product_webpage.get_page_content('').find('h1', {'class':'entry-title'}).text
            paragraphs = product_webpage.get_page_content('').find_all('p')

            for p in paragraphs:
                if 'Cena' in str(p):
                    try:
                        product_code = str(p).split('Cena')
                        product_code_str = product_code[0].replace('<p>', '')
                        product_code_str_filtered = ''.join(ch for ch in product_code_str if ch.isalnum())
                        
                        product_price = str(p.find_all('span')[-1].text)
                        product_price_filtered = float(''.join(ch for ch in product_price if ch.isalnum() or ch == ',').replace(',', '.').strip())
                        product_dict = {'link': link, 'price': product_price_filtered, 'code':product_code_str_filtered, 'category':'', 'name': product_name}
                        print(f'Current product:{product_dict}, Working time: {time.time()-start}')

                        if link not in scraped_products:
                            product_list.append(Product(product_name, product_price_filtered, link, product_code_str_filtered, ''))
                            scraped_products.append(link)

                    except Exception as e:
                        print(f'Dla linku {link} nie udało się')
        return product_list
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/apikoz_nie_sklep.xml')