from Product import Product


class Products():
    def __init__(self, products: list = []) -> None:
        self.products = self.check_product_list(products=products)

    def check_product_list(self, products: list):
        if len(products) < 1:
            raise Exception(
                "W FUNKCJI \'initialize_product_list\' na wejściu podano listę, na której nie ma produktów.")

        for product in products:
            if isinstance(product, Product) != True:
                raise Exception(
                    "W FUNKCJI \'initialize_product_list\' w wejściowej liście znajdują się obiekty klasy innej niż Product")
        return products

    def generate_products_xml(self):
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<products>\n'
        xml_footer = '</products>'
        product_xmls = []

        for product in self.products:
            single_product_xml = f"<product>\n\t<name>{product.name.replace('&', 'and')}</name>\n\t<price>{product.price}</price>" \
                f"\n\t<code>{product.code}</code>\n\t<on_sale></on_sale>" \
                f"\n\t<category>{product.category}</category>\n\t<link>{product.url}</link></product>\n"
            product_xmls.append(single_product_xml)
        xml_file_content = xml_header + ''.join(product_xmls) + xml_footer
        return xml_file_content

    def write_xml(self, file):
        xml_file = open(file, 'w', encoding='UTF-8')
        xml_file.write(self.generate_products_xml())
        xml_file.close()
