from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime

class HoneyExtractors:
    def __init__(self) -> None:
        self.base_url = "https://www.honey-extractors.com/"
        self.categories = self.get_categories_names_and_urls()


    def get_categories_names_and_urls(self): # tylko dla jednej kategorii jakaś dziwna strona to jest :/
        categories = {}
        url = self.base_url + "/beekeeping-equipment"

        response = requests.get(url, headers=scraping_headers())
        response_soup = BeautifulSoup(response.text, 'html.parser')

        categories_boxes = response_soup.find_all('article', {'class':'art'})
        categories_links = [box.find('div', {'class': 'art-genericname'}).find('a')['href'] for box in categories_boxes]
        categories_links = [f"https://www.honey-extractors.com{link}" for link in categories_links]
        categories_names = [box.find('div', {'class': 'art-genericname'}).find('a')['title'] for box in categories_boxes]

        for category_link, category_name in zip(categories_links, categories_names):
            if category_link not in categories.keys():
                categories[category_link] = category_name

        categories['https://www.honey-extractors.com/varrox-4'] = 'VARROX'
        categories['https://www.honey-extractors.com/bee-corridor-to-prevent-bee-robbery-2'] = 'BEE CORRIDOR'
        categories['https://www.honey-extractors.com/beehive-scales'] = 'BEEHIVE SCALES'

        return categories
    

    def get_products_from_categories(self):
        start_time = time.time()
        product_list = []

        for category_url in self.categories.keys():
            random_delay(2, 5)
            products_category = self.categories[category_url]

            category_html_content = requests.get(category_url, headers=scraping_headers())
            category_html_content_soup = BeautifulSoup(category_html_content.text, 'html.parser')

            products_box = category_html_content_soup.find_all('div', {'class':'product-list-container'})

            if products_box != []:
                products_html = products_box[0].find_all('article', {'class':'art'})
                for product_html in products_html:
                    random_delay(2, 5)
                    try:
                        product_link1 = product_html.find('div', {'class': 'art-picture-block'}).find('a')['href']
                        product_link2 = 'https://www.honey-extractors.com' + product_link1
                    except Exception as e:
                        print(f"Błąd przy szukaniu linku: {e}, kategoria: {self.categories[category_url]}")
                    
                    product_info_response = requests.get(product_link2, headers=scraping_headers())

                    if product_info_response.status_code == 200:
                        product_page_soup = BeautifulSoup(product_info_response.text, 'html.parser')

                        try:
                            product_name = product_page_soup.find('h1', {'itemprop':'name'}).text.strip()
                        except Exception as e:
                            product_name = ""
                            print(f"Błąd przy szukaniu nazwy produktu: {e}, produkt: {product_link2}")

                        try:
                            product_price = float(product_page_soup.find('meta', {'itemprop':'price'})['content'])
                        except Exception as e:
                            product_price = 0.0
                            print(f"Błąd przy szukaniu ceny produktu: {e}, produkt: {product_link2}")

                        try:
                            product_code = product_page_soup.find('td', {'itemprop':'sku'}).text
                        except Exception as e:
                            product_code = ""
                            print(f"Błąd przy szukaniu kodu produktu: {e}, produkt: {product_link2}")

                        product = Product(product_name, product_price, product_link2, product_code, products_category)
                        product_list.append(product)

                        print(f"Kategoria: {category_url}, Czas pracy: {time.time()-start_time}")
        return product_list
    
        
    def export_products_to_xml(self, path):
        today_date = datetime.today()
        today_date_sr = today_date.strftime("%d_%m_%Y")
        products = Products(self.get_products_from_categories())
        products.write_xml(f'{path}/HoneyExtractors.xml')