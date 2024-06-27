from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class Apitec():
    def __init__(self) -> None:
        self.url = 'https://apitec.pl/'
        self.categories = self.get_categories()


    def get_categories(self):
        categories = requests.get('https://apitec.pl/sitemaps/sitemap_400ea6b15338ba759dfd8c157f582a9d_2.xml')
        categories_soup = BeautifulSoup(categories.text, 'xml')
        categories_links = [category.text for category in categories_soup.find_all('loc')]
        return categories_links

    def get_products(self):
        scraped_products = []
        product_list = []
        start = time.time()

        for category_link in self.categories:
            print(f"Current category: {category_link}, Working time: {time.time()-start}")
            category_html_content = BeautifulSoup(requests.get(category_link, headers=scraping_headers()).text, 'html.parser')
            products = category_html_content.find_all('article', {'itemtype':'http://schema.org/Product'})

            if products != []:
                category_html_content = BeautifulSoup(requests.get(f"{category_link},1.html", headers=scraping_headers()).text, 'html.parser')
                try:
                    pagination_links = category_html_content.find('div', {'class': 'pagination'}).find_all('a')
                    print(pagination_links[-1])
                    if pagination_links[-1]['class'] == ['button', 'button-light', 'active']:
                        max_pages = 2
                    elif pagination_links[-1].text == '»':
                        max_pages = int(pagination_links[-2].text)
                    elif pagination_links[-1].text == '»»':
                        max_pages = int(pagination_links[-1]['title'])
                    else:
                        max_pages = 0
                        print(f'WYSTĄPIŁ BŁAD W ZNAJDOWANIU MAX LICZBY STRON: {category_link}')
                    print(f'Maksymalna liczba stron: {max_pages}')

                    for i in range(1, max_pages+1):
                        print(f"Current category: {category_link}, strona: {i-1}, Working time: {time.time()-start}")
                        if i==1:
                            link = f"{category_link}"
                        else:
                            link = f"{category_link},{i-1}.html"

                        category_page_html_content = BeautifulSoup(requests.get(f"{link}", headers=scraping_headers()).text, 'html.parser')
                        category_page_products = category_page_html_content.find_all('article', {'itemtype':'http://schema.org/Product'})

                        try:
                            category_text = category_html_content.find('div', {'class': 'category-description'}).find('h1').text.strip()
                        except Exception as e:
                            category_text = ''

                        for category_page_product in category_page_products:
                            try:
                                product_link = category_page_product['data-url']
                            except Exception as e:
                                product_link = ''
                            try:
                                product_price = float(category_page_product.find('span', {'itemprop': 'price'})['content'])
                            except Exception as e:
                                product_price = 0.0
                            try:
                                product_name = category_page_product.find('h2', {'class':'product-name'}).text.strip()
                            except Exception as e:
                                product_name = ''
                            try:
                                product_code = str(category_page_product.find('div', {'data-correct': 'product-photo-1'})['title']).replace('Model: ', '')
                            except Exception as e:
                                product_code = ''

                            if product_link not in scraped_products:
                                product_list.append(Product(product_name, product_price, product_link, product_code, category_text))
                                scraped_products.append(product_link)

                except Exception as e:
                    print(f"Nie znaleziono paginacji ({category_link}): {e}")
                    category_products = BeautifulSoup(requests.get(f"{category_link}", headers=scraping_headers()).text, 'html.parser')
                    products = category_products.find_all('article', {'itemtype':'http://schema.org/Product'})

                    for product in products:
                        try:
                            category_text = category_products.find('div', {'class': 'category-description'}).find('h1').text.strip()
                        except Exception as e:
                            category_text = ''
                        try:
                            product_link = product['data-url']
                        except Exception as e:
                            product_link = ''
                        try:
                            product_price = float(product.find('span', {'itemprop': 'price'})['content'])
                        except Exception as e:
                            product_price = 0.0
                        try:
                            product_name = product.find('h2', {'class':'product-name'}).text.strip()
                        except Exception as e:
                            product_name = ''
                        try:
                            product_code = str(product.find('div', {'data-correct': 'product-photo-1'})['title']).replace('Model: ', '')
                        except Exception as e:
                            product_code = ''

                        if product_link not in scraped_products:
                            product_list.append(Product(product_name, product_price, product_link, product_code, category_text))
                            scraped_products.append(product_link)
            else:
                print(f"Link - {category_link} nie ma produktów!")
        return product_list
    
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/apitec.xml')