from WebScrapingFunctions import scraping_headers, random_delay
from bs4 import BeautifulSoup
from Products import Products
from Product import Product
import requests
import time
import json
from datetime import datetime
from WebPage import WebPage


class phBarc():
    def __init__(self) -> None:
        self.sitemaps = ['https://phbarc.pl/product-sitemap.xml',
                    'https://phbarc.pl/product-sitemap2.xml',
                    'https://phbarc.pl/product-sitemap3.xml',
                    'https://phbarc.pl/product-sitemap4.xml']
        self.product_links = self.get_phbarc_products_links()
    
    def get_phbarc_products_links(self):
        links = []
        links_raw = []
        for sitemap in self.sitemaps:
            sitemap_response = requests.get(sitemap, scraping_headers())
            sitemap_soup = BeautifulSoup(sitemap_response.text, 'xml')
            products_links = [link.text for link in sitemap_soup.find_all('loc') if '/produkt/' in link.text and '/offer/' not in link.text and '/credit/' not in link.text]
            links_raw.append(products_links)
        
        for link_list in links_raw:
            for link in link_list:
                links.append(link)

        return links
    
    def get_product(self, product_link:str, scraped_produts:list, product_list:list):
        random_delay(1, 5)
        product_response = requests.get(product_link, scraping_headers())
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        try:
            product_details = product_soup.find('div', {'class': 'summary-inner set-mb-l reset-last-child'})
        except Exception as e:
            product_details = ''
            print(e)
        link = product_link

        try:
            name = product_details.find('h1', {'class': 'product_title entry-title wd-entities-title'}).text.strip()
        except AttributeError:
            name = ''
        except Exception as e:
            name =''
            print(e)

        try:
            price = float(product_details.find('bdi').text.replace('.', '').split(' ')[0].replace(',', '.').replace('zł', '').replace('\xa0', ''))
        except AttributeError:
            price = 0.0
        except Exception as e:
            price = 0.0
            print(e)

        try:
            code = product_details.find('span', {'class': 'sku'}).text.strip()
        except AttributeError:
            code = ''
        except Exception as e:
            code = ''
            print(e)
        
        try:
            categories = product_details.find('span', {'class': 'posted_in'}).find_all('a', {'rel': 'tag'})
            categories = [category.text for category in categories]
        except Exception as e:
            categories = ['','']
            print(e)

        categories_joined = ', '.join(categories)

        if link not in scraped_produts:
            product_list.append(Product(name, price, link, code, categories_joined))
            scraped_produts.append(link)
        # write_xml('phbarc.xml', generate_xml(all_products))

    def crawl_loop(self):
        scraped_products = []
        product_list = []
        starting_time = time.time()
        for product_link in self.product_links:
            print(f"Working time: {time.time()-starting_time}, current product: {product_link}")
            self.get_product(product_link, scraped_products, product_list)
        return product_list

    def export_products_to_xml(self, path):
        products = Products(self.crawl_loop())
        products.write_xml(f'{path}/phbarc.xml')