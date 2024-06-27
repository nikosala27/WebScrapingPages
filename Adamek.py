from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class Adamek():
    def __init__(self) -> None:
        self.url = 'https://www.adamek.net.pl/3-sklep'
        self.categories = self.get_categories()

    def get_categories(self):
        category_tmp = []
        html_content = BeautifulSoup(requests.get(self.url, headers=scraping_headers()).text, 'html.parser')
        for category in html_content.find('div', {'id':'categories_block_left'}).find_all('a'):
            category_name = category.text.strip()
            category_link = category['href']
            category_tmp.append({category_name: category_link})
        return category_tmp

    def get_products(self):
        product_list = []
        scraped_products = []
        for category in self.categories:
            random_delay(1, 2)
            category_name = list(category.keys())[0]
            category_link = category[category_name]
            category_html_content = BeautifulSoup(requests.get(f'{self.url}/{self.get_last_part_of_link(category_link)}', headers=scraping_headers()).text, 'html.parser')

            category_pagination = category_html_content.find('ul', {'class': 'pagination'})

            category_max_pages = 1
            if category_pagination != None:
                category_max_pages = int(category_pagination.find_all('span')[-1].text)
            
            for i in range(1, category_max_pages+1):
                random_delay(1, 4)
                category_page_html_content = BeautifulSoup(requests.get(f'https://www.adamek.net.pl/{self.get_last_part_of_link(category_link)}?p={i}', headers=scraping_headers()).text, 'html.parser')
                try:
                    products =  category_page_html_content.find_all('div', {'class':'product-container'})
                except Exception as e:
                    products = []

                for product in products:
                    try:
                        product_link = product.find('a', {'class':'product-name'})['href']
                    except Exception as e:
                        product_link = ''

                    try:
                        product_name = product.find('a', {'class':'product-name'})['title']
                    except Exception as e:
                        product_name = ''

                    try:
                        product_price = float(product.find('span', {'class':'price product-price'}).text.strip().replace('zł', '').replace(',', '.'))
                    except Exception as e:
                        product_price = 0.0

                    if product_link not in scraped_products:
                        product_list.append(Product(product_name, product_price, product_link, '', category_link))
                        scraped_products.append(product_link)
                        print(Product(product_name, product_price, product_link, '', category_link))
        return product_list
    
    def get_last_part_of_link(self, link):
        return link.split('/')[-1]
    
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/adamek.xml')
    