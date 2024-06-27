from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime


class Burnat():
    def __init__(self) -> None:
        self.url = 'https://burnat.com.pl'
        self.categories = self.get_categories()

    def get_categories(self):
        response = requests.get(self.url, headers=scraping_headers())
        soup = BeautifulSoup(response.text, 'html.parser')

        categories_divs = soup.find_all('div', {'class': 'submenu level1'})
        categories_links = [div.find_all('a', href=True) for div in categories_divs]
        categories_links = [a['href'] for link in categories_links for a in link]

        return categories_links
    
    def get_products(self):
        product_list = []
        starting_time = time.time()
        scraped_products = []

        for category in self.categories:
            response = requests.get(self.url+category, headers=scraping_headers())
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                last_page_index = soup.find('ul', {'class': 'paginator'}).find_all('li')[-2].text
            except Exception as e:
                last_page_index = 1
                print(f"Error in page index: {e}")

            for i in range(1, int(last_page_index)+1):
                random_delay(1, 2)
                print(f"Working time: {time.time() - starting_time}, current page: {self.url}{category}/{i}")
                response = requests.get(f"{self.url}{category}/{i}", headers=scraping_headers())
                soup = BeautifulSoup(response.text, 'html.parser')

                try:
                    producs_divs = soup.find_all('div', {'class':'f-row description'})
                except Exception as e:
                    producs_divs = []
                    print(f"Error in prouct divs: {e}")

                try:
                    product_category = soup.find('h1', {'class': 'category-name'}).text.strip()
                except Exception as e:
                    product_category = category
                    print(f"Error in product category: {e}")

                for product_div in producs_divs:
                    try:
                        product_link =  self.url + product_div.find('a', {'rel': 'dofollow'})['href']
                    except Exception as e:
                        product_link = ''
                        print(f"Error in prouct link: {e}")

                    try:
                        product_name =  product_div.find('span', {'class': 'productname'}).text
                    except Exception as e:
                        product_name = ''
                        print(f"Error in prouct name: {e}")

                    try:
                        product_price = float(product_div.find('em').text.replace('zł', '').replace('\xa0', '').replace(',', '.'))
                    except Exception as e:
                        product_price = ''
                        print(f"Error in prouct price: {e}")

                    try:
                        product_texts = product_div.find_all('p')
                        product_texts  = [product for product in product_texts if 'Nr katalogowy' in product.text]

                        if product_texts != []:
                            if '<br>' in str(product_texts[0]) or '<br/>' in str(product_texts[0]):
                                product_code = str(product_texts[0]).replace('<br>', '\t').replace('<br/>', '\t').split('\t')[0].split(' ')[-1]
                            else:
                                product_code = product_texts[0].split(' ')[-1]
                        else:
                            product_code = ''
                    except Exception as e:
                        product_code = ''
                        print(f"Error in prouct code: {e}")

                    if product_link not in scraped_products: 
                        product = Product(product_name, product_price, product_link, product_code, product_category)
                        product_list.append(product)
                        scraped_products.append(product_link)
                        print(product)
        return product_list
    
    def export_products_to_xml(self, path):
        products = Products(self.get_products())
        products.write_xml(f'{path}/burnat.xml')