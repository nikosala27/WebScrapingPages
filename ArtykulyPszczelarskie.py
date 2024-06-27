from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class ArtykulyPszczelarskie():
    def __init__(self) -> None:
        self.url = 'https://artykulypszczelarskiefit.pl/sklep/'

    def get_products(self):
        product_list = []
        scraped_products = []
        fit_html_content = BeautifulSoup(requests.get(self.url, headers=scraping_headers()).text, 'html.parser')

        try:
            max_pages = int(fit_html_content.find('ul', {'class': 'page-numbers'}).find_all('a', {'class': 'page-numbers'})[-2].text.strip())
        except Exception as e:
            max_pages = 0
            print(f'Error: {e}')

        if max_pages > 0:
            for i in range(1, max_pages+1):
                random_delay(1, 5)
                page_html_content = BeautifulSoup(requests.get(f"{self.url}?product-page={i}", headers=scraping_headers()).text, 'html.parser')
                products_html_content = page_html_content.find_all('div', {'class': 'astra-shop-summary-wrap'})

                for product_html_content in products_html_content:
                    try:
                        product_link = product_html_content.find('a', {'class':'ast-loop-product__link'})['href']
                    except Exception as e:
                        product_link = ''

                    if product_link != '':
                        try:
                            product_category = product_html_content.find('span', {'class': 'ast-woo-product-category'}).text.strip()
                        except Exception as e:
                            product_category = ''
                        
                        try:
                            product_name = product_html_content.find('h2', {'class': 'woocommerce-loop-product__title'}).text
                        except Exception as e:
                            product_name = ''

                        try:
                            product_price = float(product_html_content.find('span', {'class': 'woocommerce-Price-amount amount'}).text.replace('zł', ''))
                        except Exception as e:
                            product_price = 0.0

                        product = Product(product_name, product_price, product_link, "", product_category)
                        if product_link not in scraped_products:
                            product = Product(product_name, product_price, product_link, "", product_category)
                            product_list.append(product)
                            scraped_products.append(product_link)
                            
                        print(f"Current product: {product_name}, {product_category}, {product_price} zł")
        return product_list

    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/fit_artykulu_pszczelarskie.xml')