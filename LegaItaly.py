from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
from datetime import datetime

class LegaItaly:
    def __init__(self) -> None:
        self.base_url = "https://www.legaitaly.com/en"
        self.categories = self.get_categories_names_and_urls()

    def get_categories_names_and_urls(self):
        subcategories = {}
        main_categories = {}

        categories_html_content = requests.get(f"{self.base_url}/products", headers=scraping_headers()).text
        categories_html_content_soup = BeautifulSoup(categories_html_content, "html.parser")

        categories_box = categories_html_content_soup.find("div", {"class": "categories"})
        categories_divs = categories_box.find_all("div", {"class": "categoria-primaria"})

        for category_div in categories_divs:
            category_name = category_div.find("h4").text
            category_url = f"https://www.legaitaly.com{category_div.find('a')['href']}"
            main_categories[category_url] = category_name

        subcategories_box = categories_html_content_soup.find("div", {"class": "megamenu"})
        subcategories_links = [f"https://www.legaitaly.com{subcategory['href']}" for subcategory in subcategories_box.find_all("a")]

        subcategories_links_filtered = [subcategory for subcategory in subcategories_links if subcategory not in main_categories.keys()]

        for subcategory in subcategories_links_filtered:
            subcategories[subcategory] = subcategory.split('/')[-1].replace('-', ' ').upper()

        return subcategories

    def get_products_from_categories(self):
        start_time = time.time()
        product_list = []
        for url in self.categories.keys():
            random_delay(2, 5)
            category_html_content = requests.get(f"{url}", headers=scraping_headers()).text
            category_html_content_soup = BeautifulSoup(category_html_content, "html.parser")

            products_html = category_html_content_soup.find_all('li', {'class':'item item-autoload item-buy-wrapper item-tipo-0'})

            for product_html in products_html:
                try:
                    product_name = product_html.find('div', {'class':'item-name'}).find('a')['title']
                except Exception as e:
                    product_name = ""
                    print(f'Wyjątek dla kategorii {url}, kod błędu: {e} = PRODUCT NAME')

                try:
                    product_code = product_html.find('div', {'class':'item-sku'}).text.replace('Code:', '').strip()
                except Exception as e:
                    product_code = ""
                    print(f"Wyjątek dla kategorii {url}, kod błędu: {e} = PRODUCT CODE")

                try:
                    product_price = float(product_html.find('span', {'class': 'price item-buy-price'}).text.replace('€', '').replace('.', '').replace(',', '.').strip())
                except Exception as e:
                    print(f"Wyjątek dla kategorii {url}, kod błędu: {e} = PRODUCT PRICE")
                    product_price = 0.0

                try:
                    product_url = f"https://www.legaitaly.com{product_html.find('a', {'class':'item-img'})['href']}"
                except Exception as e:
                    print(f"Wyjątek dla kategorii {url}, kod błędu: {e} = PRODUCT URL")
                    product_url = ""

                product_category = self.categories[url]

                product = Product(product_name, product_price, product_url, product_code, product_category)
                product_list.append(product)

            print(f"====Kategoria: {url}, Czas pracy: {time.time()-start_time}=====")
        return product_list

    def export_products_to_xml(self, path):
        today_date = datetime.today()
        today_date_sr = today_date.strftime("%d_%m_%Y")
        products = Products(self.get_products_from_categories())

        products.write_xml(f'{path}/LegItaly.xml')