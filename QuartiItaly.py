from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime
from tkinter import Text, constants


class QarItaly():
    def __init__(self, entry: Text) -> None:
        self.url = "https://www.quartiitaly.it/en-EN/index.php"
        self.categories = self.get_categories()
        self.entry = entry

    def get_categories(self):
        home_page_html_content = requests.get(self.url, headers=scraping_headers()).text
        home_page_html_soup = BeautifulSoup(home_page_html_content, "html.parser")

        menu_html_content = home_page_html_soup.find('ul', {'id': 'menu-vertical-menu'})
        all_categories_links = [f"https://www.quartiitaly.it{li['href']}" for li in menu_html_content.find_all('a')]

        return all_categories_links
    
    def get_products_from_categories(self):
        start_time = time.time()
        product_list = []
        for category in self.categories:
            category_id = category.split('/')[-1].split('_')[0]
            category_name = " ".join(category.split('/')[-1].split('_')[1].split('-')).upper()

            for i in range(1, 50):
                random_delay(1, 5)
                category_link = f"https://www.quartiitaly.it/en-EN/shop.php?id={category_id}&page={i}"
                print(category_link)

                try:
                    category_response = requests.get(category_link, headers=scraping_headers()).text
                    category_soup = BeautifulSoup(category_response, 'html.parser')
                    if category_soup.find_all('ul', {'class': 'products columns-3'}) == []: break
                except Exception as e:
                    print(f"Bład przy nawiązywaniu połączenia z {category_link}")
                    category_response = ""

                try:
                    products_grid =  category_soup.find('ul', {'class': 'products columns-3'})
                except Exception as e:
                    products_grid = ""
                    print(f"Błąd przy szukaniu gridu produktów: {category_link}, błąd: {e}")

                try:
                    products = products_grid.find_all('div', {'class': 'product-inner'})
                except Exception as e:
                    products = []
                    print(f"Błąd przy wyszukwianiu porduktów: {category_link}, błąd: {e}")

                for product in products:
                    try:
                        product_name = product.find('h3').text.strip()
                    except Exception as e:
                        product_name = ""
                        print(f"Błąd przy suzkaniu nazwy: {category_link}, błąd: {e}")

                    try:
                        product_code = product_name.split('-')[0].strip()
                    except Exception as e:
                        product_code = ""
                        print(f"Błąd przy suzkaniu kodu: {category_link}, błąd: {e}")

                    try:
                        product_link1 = product.find('a')['href']
                        product_link2 = "https://www.quartiitaly.it" + product_link1
                    except Exception as e:
                        product_link2 = ""
                        print(f"Błąd przy suzkaniu linku: {category_link}, błąd: {e}")

                    try:
                        product_price = float(product.find('div', {'class': 'price-add-to-cart'}).find('ins').text.replace('€', '').replace('.', '').replace(',', '.').replace('â\x82¬ ', '').strip())
                    except Exception as e:
                        product_price = 0.0
                        print(f"Błąd przy suzkaniu ceny: {category_link}, błąd: {e}")

                    product = Product(product_name, product_price, product_link2, product_code, category_name)
                    print(f"{product}, Working time: {time.time()-start_time}")
                    product_list.append(product)
        return product_list
    def export_products_to_xml(self, path):
        today_date = datetime.today()
        today_date_sr = today_date.strftime("%d_%m_%Y")
        products = Products(self.get_products_from_categories())
        products.write_xml(f'{path}/QuarItaly.xml')
