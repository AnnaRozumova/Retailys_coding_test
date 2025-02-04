'''Module for handling parsing logic'''
import logging
from lxml import etree

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ProductDetails:
    '''Parses an XML file'''
    def __init__(self, xml_input):
        with open(xml_input, 'r', encoding='utf-8') as file:
            xml = file.read()
        self.root = etree.fromstring(xml)

    def parse_total_products(self):
        '''Count total <item> elements in the XML'''
        return len(self.root.xpath("/export_full/items/item"))

    def parse_products(self):
        '''Extract a list of products'''
        products = []
        for elem in self.root.xpath("/export_full/items/item"):
            product_info = {"name": elem.get("name")}
            products.append(product_info)
        return products

    def parse_spare_parts(self):
        '''Extract a list of products'''
        grouped_spare_parts = {}
        for part in self.root.xpath("//part"):
            if part.get('partName') == 'Náhradní díly':
                item_name = part.get("itemName", "Unknown Part")
                if item_name not in grouped_spare_parts:
                    grouped_spare_parts[item_name] = []
                for item in part.xpath("./item"):
                    grouped_spare_parts[item_name].append(item.get("name", "N/A"))
        return grouped_spare_parts
