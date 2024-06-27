from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime

class LaTienda():
    def __init__(self) -> None:
        self.url = 'https://apicolalospedroches.com/'
        self.categories = self.get_categories()
    
    def get_categories(self):
        response = requests.get(self.url, headers=scraping_headers()).text
        response_soup = BeautifulSoup(response, 'html.parser')

        categories_dict = {}
        categories_names = [a.text for a in response_soup.find('ul', {'id':'accordion'}).find_all('a')]
        categories_links = [f"{self.url}{a['href']}" for a in response_soup.find('ul', {'id':'accordion'}).find_all('a') if a.has_attr('href')]

        for name, link in zip(categories_names, categories_links):
            categories_dict[link] = name

        return categories_dict
    
    def get_products(self):
        product_list = []
        scraped_products = []
        start_time = time.time()
        for category_link in self.categories.keys():
            random_delay(1, 2)
            try:
                category_response = requests.get(category_link, headers=scraping_headers()).text
                category_response_soup = BeautifulSoup(category_response, 'html.parser')
            except Exception as e:
                category_response_soup = ""
                print(f"Błąd przy nawiązywaniu połączenia z kategorią: {category_link}")

            products_box = category_response_soup.find('ul', {'id': 'ulprueba'})
            for product in products_box.find_all('div', {'class':'producto'}):
                try:
                    product_link = f"{self.url}{product.find('a')['href']}"
                except Exception as e:
                    product_link = ""
                    print(f"Błąd przy szukaniu linku do produktu: {category_link}, błąd: {e}")

                if product_link != "" and product_link not in scraped_products:
                    random_delay(1, 3)
                    try:
                        product_response = requests.get(product_link, headers=scraping_headers()).text
                        product_response_soup = BeautifulSoup(product_response, 'html.parser')
                    except Exception as e:
                        product_response_soup = ""
                        print(f"Błąd przy nawiązywaniu połączenia z produktem: {product_link}, błąd: {e}")

                    try:
                        product_name = product_response_soup.find('h2', {'id': 'n_arti'}).text.strip()
                    except Exception as e:
                        product_name = ""
                        print(f"Błąd przy szukaniu nazwy produktu: {product_link}, błąd: {e}")

                    try:
                        product_code = product_response_soup.find('h2', {'id': 'n_arti'}).find_next('span').text.replace('Ref: ', '').strip()
                    except Exception as e:
                        product_code = ""
                        print(f"Błąd przy szukaniu kodu produktu {product_link}, błąd: {e}")

                    try:
                        product_price = float(''.join((char for char in product_response_soup.find('div', {'id': 'precio'}).text if char.isdigit() or char=='.')))
                    except Exception as e:
                        product_price = 0.0
                        print(f"Błąd przy szukaniu ceny produku: {product_link}, błąd: {e}")

                    scraped_products.append(product_link)
                    product = Product(product_name, product_price, product_link, product_code, self.categories[category_link])
                    product_list.append(product)
                    print(f"{product}, Working time: {time.time()-start_time}")
        return product_list
    
    def export_products_to_xml(self, path):
        today_date = datetime.today()
        today_date_sr = today_date.strftime("%d_%m_%Y")
        products = Products(self.get_products())
        products.write_xml(f'{path}/LaTienda.xml')
