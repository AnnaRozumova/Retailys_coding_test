from lxml import etree

class XMLParser:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        with open(xml_file_path, 'rb') as file:
            self.tree = etree.parse(file)

    def get_total_products(self):
        '''Counts total items in XML.'''
        products = self.tree.xpath("//item")
        return len(products)
    
    def get_products_list(self):
        '''Returns a list of items from XML.'''
        products = self.tree.xpath("//item")
        product_list = []
        for product in products:
            product_info = {
                "name": product.get("name")
            }
            product_list.append(product_info)
        return product_list
    
    def get_spare_parts(self):
        '''Returns a list of spare parts, if any.'''
        spare_parts_list = []

        categories = self.tree.xpath("//categoriesWithParts/category | //categoriesNew/category")
        for category in categories:
            category_type = category.get("type", "").lower()
            category_name = category.get("name", "Unnamed Category")
            if category_type in ["parts", "part", "partBrand", "partType", "partItem", "partCategory"]:
                for item in category.xpath(".//item"):
                    spare_part_info = {
                        "category_name": category_name,
                        "item_name": item.get("name", "N/A")
                    }
                    print(f"Found spare parts: {spare_part_info['item_name']}")
                    spare_parts_list.append(spare_part_info)
        return spare_parts_list