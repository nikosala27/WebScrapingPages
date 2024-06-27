from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime


class LatienDae():
    def __init__(self) -> None:
        self.base_url = 'https://www.latiendadelapicultor.com/en'
        self.categories = self.get_categories()

    def get_categories(self):
        response = requests.get(self.base_url, headers=scraping_headers()).text
        response_soup = BeautifulSoup(response, 'html.parser')

        categories_links = [a['href'] for a in response_soup.find('div', {'id': 'soymenu'}).find_all('a') if a.has_attr('href')]
        return categories_links
    
    def get_products_from_categories(self):
        scraped_products = []
        start_time = time.time()
        product_list = []
        for category_link in self.categories:
            category_name = " ".join(category_link.split('/')[-1].split('-')).upper()

            for i in range(1, 50):
                random_delay(1, 3)
                try:
                    category_soup = BeautifulSoup(requests.get(f"{category_link}?page={i}", headers=scraping_headers()).text, 'html.parser')
                    products = category_soup.find_all('article', {'class': 'product-miniature js-product-miniature'})
                    if products == []: break
                except Exception as e:
                    category_soup = ""
                    print(f"Błąd przy nawiązywaniu połączenia z kategorią: {category_link}")
                print(f"Przeszukiwana kategoria: {category_link}?page={i}")
                for product in products:
                    try:
                        product_link = product.find('a')['href']
                    except Exception as e:
                        product_link = ""
                        print(f"Błąd przy szukaniu linku do produktu, kategoria: {category_link}, strona: {i}")

                    if product_link != "":
                        random_delay(1, 5)
                        try:
                            product_page = BeautifulSoup(requests.get(product_link, headers=scraping_headers()).text, 'html.parser')
                        except Exception as e:
                            product_page = ""
                            print(f"Błąd nawiązywania połączenia z produktem: {product_link}, błąd: {e}")

                        try:
                            product_name = product_page.find('h1', {'itemprop': 'name'}).text.strip()
                        except Exception as e:
                            product_name = ""
                            print(f"Błąd przy szukaniu nazwy produktu: {product_link}, błąd: {e}")

                        try:
                            product_code = product_page.find('span', {'itemprop': 'sku'}).text.strip()
                        except Exception as e:
                            product_code = ""
                            print(f"Błąd przy szukaniu kodu: {product_link}, błąd: {e}")
                        
                        try:
                            product_price_box = product_page.find('div', {'class':'col-md-5 product-buy-block'})
                            int_price = product_price_box.find('span', {'class': 'soy_entero'}).text.strip()
                            if '€' in int_price:
                                prodcut_price = float(int_price.replace('€', '').strip())
                            else:
                                decimal_price = product_price_box.find('span', {'class': 'soy_decimal'}).text.strip()
                                prodcut_price = float(f"{int_price}{decimal_price}")
                        except Exception as e:
                            prodcut_price = 0.0
                            print(f"Błąd przy szukaniu ceny produktu: {product_link}, błąd: {e}")

                        if product_link not in scraped_products:
                            product = Product(product_name, prodcut_price, product_link, product_code, category_name)
                            print(f"{product}, Working time: {time.time()-start_time}")
                            product_list.append(product)
                            scraped_products.append(product_link)
                        else:
                            print(f"Produkt: {product_link} był już scrapowany")
        return product_list
    
    def export_products_to_xml(self, path):
        today_date = datetime.today()
        today_date_sr = today_date.strftime("%d_%m_%Y")
        products = Products(self.get_products_from_categories())
        products.write_xml(f'{path}/LatienDae.xml')
            
