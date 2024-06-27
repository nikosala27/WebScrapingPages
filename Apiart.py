from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class Apiart():
    def __init__(self) -> None:
        self.url = 'https://apiart.pl/'
        self.categories_links = ['https://apiart.pl/58-sprzet-pszczelarski',
                                'https://apiart.pl/49-odziez',
                                'https://apiart.pl/13-formy-i-swiece',
                                'https://apiart.pl/28-kosmetyki',
                                'https://apiart.pl/33-produkty-spozywcze',
                                'https://apiart.pl/47-inne',
                                'https://apiart.pl/27-weza-i-wosk'
                                ]
        self.categories_names = ['Sprzęt pszczelarski', 'Odzież', 'Formy i świece', 'Kosmetyki', 'Produkty spożywcze', 'Inne', 'Węza i wosk']

    def get_products(self):
        scraped_products = []
        product_list = []
        for category in self.categories_links:
            category_html_content = BeautifulSoup(requests.get(category, headers=scraping_headers()).text, 'html.parser')

            max_pages = 1
            try:
                max_pages = int(category_html_content.find('ul', {'class': 'pagination col-xs-12 col-lg-6'}).find_all('span')[-1].text)
            except Exception as e:
                print('Kategoria ma tylko jedną stronę')

            for i in range(1, max_pages+1):
                category_page_html_content = BeautifulSoup(requests.get(f"{category}?p={i}", headers=scraping_headers()).text, 'html.parser')
                products_html_content = category_page_html_content.find_all('div', {'class': 'product-container'})
                if products_html_content != []:
                    for product_html_content in products_html_content:
                        has_link = True
                        try:
                            product_link = product_html_content.find('a', {'class': 'product_img_link'})['href']
                        except Exception as e:
                            has_link = False
                            print('Brak linku!')

                        if has_link:
                            try:
                                product_page_html_content = BeautifulSoup(requests.get(product_link, headers=scraping_headers()).text, 'html.parser')
                                random_delay(1, 4)
                            except Exception as e:
                                product_page_html_content = ''
                            
                            try:
                                product_price = float(product_page_html_content.find('span', {'id': 'our_price_display'})['content'])
                            except Exception as e:
                                product_price = 0.0

                            try:
                                product_name = product_page_html_content.find('h1', {'itemprop': 'name'}).text
                            except Exception as e:
                                product_name = ''

                            try:
                                product_code =  product_page_html_content.find('span', {'itemprop': 'sku'})['content']
                            except Exception as e:
                                product_code = ''

                            if product_link not in scraped_products:
                                product_list.append(Product(product_name,product_price, product_link, product_code, category))
                                scraped_products.append(product_link)

                            print(f"Current product: {product_name}, {product_code}, {product_price} zł")
        return product_list
    
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/apiart.xml')