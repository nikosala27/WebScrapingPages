from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class PasiekaBarc():
    def __init__(self) -> None:
        self.url = 'http://pasieka-barc.pl/?post_type=product'
        self.categories = self.get_categories()

    def get_categories(self):
        response = requests.get(self.url, headers=scraping_headers())
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, 'html.parser')
            categories_html = html_content.find('ul', {'class': 'product-categories'})
            categories_links = [link['href'] for link in categories_html.find_all('a')]
            return categories_links
        return 0
    
    def get_products(self):
        product_list = []
        scraped_products = []
        for category_link in self.categories:
            category_response = requests.get(category_link, headers=scraping_headers())
            category_html_content = BeautifulSoup(category_response.text, 'html.parser')
            page_numbers = category_html_content.find_all('ul', {'class':'page_numbers'})
            if page_numbers == []:
                products_html = category_html_content.find_all('div', {'class': 'berocket_lgv_additional_data'})
                for product in products_html:
                    code = product.find('h3')
                    name = product.find('div', {'class': 'lgv_description lgv_description_simple'}).text.strip()
                    category = product.find('a', {'rel': 'tag'}).text
                    price = product.find('bdi').text.replace('.', '').split(' ')[0].replace(',', '.').replace('zł', '')
                    link = product.find('a', {'class': 'lgv_link lgv_link_simple'})['href']

                    if link not in scraped_products:
                        product_list.append(Product(name, price, link, code, category))

                    scraped_products.append(link)
                    random_delay(1, 5)
            else:
                products_html = category_html_content.find_all('div', {'class': 'berocket_lgv_additional_data'})
                for product in products_html:
                    try:
                        link = product.find('a', {'class': 'lgv_link lgv_link_simple'})['href']
                    except Exception as e:
                        link = ''

                    code = product.find('h3')
                    name = product.find('div', {'class': 'lgv_description lgv_description_simple'}).text.strip()
                    category = product.find('a', {'rel': 'tag'}).text
                    price = product.find('bdi').text.replace('.', '').split(' ')[0].replace(',', '.').replace('zł', '')

                    if link not in scraped_products:
                        product_list.append(Product(name, price, link, code, category))

                    scraped_products.append(link)                     
                    random_delay(1, 5)

                for i in range(1, int(page_numbers[-2].text)+1):
                    url = category_link + '&paged=' + i
                    category_page_response = requests.get(url, headers=scraping_headers())
                    category_page_html_content = BeautifulSoup(category_page_response.text, 'html.parser')
                    products_html = category_page_html_content.find_all('div', {'class': 'berocket_lgv_additional_data'})
                    for product in products_html:
                        try:
                            link = product.find('a', {'class': 'lgv_link lgv_link_simple'})['href']
                        except Exception as e:
                            link = ''
                        code = product.find('h3')
                        name = product.find('div', {'class': 'lgv_description lgv_description_simple'}).text.strip()
                        category = product.find('a', {'rel': 'tag'}).text
                        price = product.find('bdi').text.replace('.', '').split(' ')[0].replace(',', '.').replace('zł', '')

                        if link not in scraped_products:
                            product_list.append(Product(name, price, link, code, category))

                        scraped_products.append(link)                     
                    random_delay(1, 5)
        return product_list

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/pasieka_barc.xml')