from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime
from WebPage import WebPage


class ApikozSklep():
    def __init__(self) -> None:
        self.url = 'https://sklep.apikoz.pl'

    def get_products(self):
        product_list = []
        scraped_products = []
        start = time.time()
        apikoz_sklep = WebPage("https://sklep.apikoz.pl")
        products_extract ={}

        url = "https://sklep.apikoz.pl"
        response = requests.get(url, headers=scraping_headers())
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all('ul', {'id': 'menu-glowne'})
            categories = products[0].find_all('a', {'class': 'categ'})
            links = [category['href'] for category in categories]
            random_delay(1, 5)

            # przejscie po stronach produktow
            for link in links:
                category_url = url + link
                response = requests.get(category_url, headers=scraping_headers())
                soup = BeautifulSoup(response.text, "html.parser")
                page_length = soup.find_all('div', {'class': 'stronyall'})

                for page in page_length:
                    pages = page.find_all('a', href=True)
                    for sub_page in pages:
                        sub_page_url = url + str(sub_page['href'])
                        response = requests.get(sub_page_url, headers=scraping_headers())
                        soup = BeautifulSoup(response.text, "html.parser")
                        products = soup.find_all('div', {'class': 'paletka1'})
                        for product in products:
                            name = product.find_all('h1')[0].text
                            category = product.find_all('p', {'class': 'nazwakatp'})[0].text
                            price = product.find_all('div', {'class': 'cenains'})[0].text.replace(',', '.').replace(' ', '').split('PLN')[0].strip()
                            on_sale = 0
                            on_sale_checker = product.find_all('div', {'class': 'promocjep'})
                            if len(on_sale_checker) == 1: on_sale = 1
                            product_link = product.find_all('div', {'class': 'obraz'})[0].find_all('a', href=True)[0]
                            product_link_string = url + str(product_link['href'])
                            
                            if product_link_string not in scraped_products:
                                product_list.append(Product(name, float(price), product_link_string, '', category))
                                scraped_products.append(product_link_string)
                                print(f"Current product:{Product(name, float(price), product_link_string, '', category)}, Working time: {time.time()-start}")
                        random_delay(1, 5)
                random_delay(1, 5)
        return product_list
    

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/apikoz_sklep.xml')
