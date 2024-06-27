from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class Koningin():
    def __init__(self) -> None:
        self.categories = self.get_categories()

    def get_categories(self):
        links = []
        with open('./html_files/KONINGIN.html', 'r+', encoding='UTF-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            categories = soup.find_all('li', {'data-depth': '0'})
            links = [category.find('a')['href'] for category in categories]
        return links
    
    def get_products(self):
        product_list = []
        categories_links = self.get_categories()
        all_products = {}
        start_time = time.time()
        for category_link in categories_links:
            for i in range(1, 30):
                response = requests.get(f"{category_link}?page={i}", headers=scraping_headers()).text
                response_soup = BeautifulSoup(response, 'html.parser').find_all('script', {'type': "application/ld+json"})[-2].text
                response_json = json.loads(response_soup)

                products_list = response_json['itemListElement']

                if products_list == []:
                    break
                else:
                    for product in products_list:
                        try:
                            product_link = product['url']
                        except Exception as e:
                            product_link = ""

                        try:
                            product_name = product['name']
                        except Exception as e:
                            product_name = ""

                        if product_link != "":
                            try:
                                product_details = requests.get(product_link, headers=scraping_headers()).text
                                product_details_soup = BeautifulSoup(product_details, 'html.parser').find_all('script', {'type': 'application/ld+json'})[-2].text
                                product_details_json = json.loads(product_details_soup)
                            except Exception as e:
                                print(f"Dla produktu: {product_link} nie udało się exportować info")

                            try:
                                product_category = category_link.split('/')[-1].split('-')
                                product_category_text = " ".join(product_category[1:]).upper()
                            except Exception as e:
                                product_category_text = ""

                            try:
                                product_code = product_details_json['sku']
                            except Exception as e:
                                product_code = ""

                            try:
                                product_price = float(product_details_json['offers']['price'])
                            except Exception as e:
                                product_price = 0.0

                            if product_link not in all_products.keys():
                                all_products[product_link] = {'name':product_name, 'code':product_code, 'category':product_category_text, 'price':product_price, 'link':product_link}
                                product = Product(product_name, product_price, product_link, product_code, product_category_text)
                                product_list.append(product)
                                print(f"{product}, Working time: {time.time()-start_time}")
                                random_delay(1, 5)
        return product_list

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/klingin.xml')
    
