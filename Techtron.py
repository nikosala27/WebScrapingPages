from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime


class Techtron():
    def __init__(self) -> None:
        self.url = 'https://techtron-group.pl/'
        self.categories = self.get_categories()

    def get_categories(self):
        response = requests.get(self.url, headers=scraping_headers()).text
        response_soup = BeautifulSoup(response, 'html.parser')
        categories_tags = response_soup.find_all('li', {'class':'category'})
        categories_links = [tag.find('a')['href'] for tag in categories_tags]

        return categories_links

    def get_products(self):
        scraped_products = []
        product_list = []
        start = time.time()
        for category_link in self.categories:
            loop = True
            i = 1
            while loop:
                category_content = BeautifulSoup(requests.get(f"{category_link}?page={i}", headers=scraping_headers()).text, 'html.parser')
                try:
                    page_not_found = category_content.find('div', {'id':'js-product-list'}).find('section', {'id':'content'}).find('h4').text
                except Exception as e:
                    page_not_found = ''
                if page_not_found == 'Brak dostępnych produktów.':
                    loop = False
                    break
                if page_not_found == '':
                    try:
                        category = category_content.find('h1', {'class':'h1'}).text
                    except Exception as e:
                        category = ''

                    products_box =  category_content.find_all('li', {'class':'product_item col-xs-12 col-sm-6 col-md-6 col-lg-4'})
                    products_links = [box.find('h3', {'class': 'h3 product-title'}).find('a')['href'] for box in products_box]

                    for product_link in products_links:
                        product_content = BeautifulSoup(requests.get(product_link, headers=scraping_headers()).text, 'html.parser')

                        try:
                            product_price = float(product_content.find('span', {'class': 'current-price-value'})['content'])
                        except Exception as e:
                            product_price = 0.0

                        try:
                            product_name = product_content.find('h1', {'class':'h1 productpage_title'}).text
                        except Exception as e:
                            product_name = ''
                        
                        try:
                            product_code = product_content.find('span', {'itemprop': 'sku'}).text
                        except Exception as e:
                            product_code = ''
                        
                        if product_link not in scraped_products:
                            product = Product(product_name, product_price, product_link, product_code, category)
                            print(product)
                            product_list.append(product)
                            scraped_products.append(product_link)
                        random_delay(1, 4)
                i = i + 1
        return product_list
    

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/techtron.xml')