from lxml import etree

class XMLParser:
    def __init__(self, xml_input):
        if isinstance(xml_input, (str, bytes)):
            with open(xml_input, 'rb') as file:
                self.tree = etree.parse(file)
        elif hasattr(xml_input, 'read'):
            self.tree = etree.parse(xml_input)
        else:
            raise TypeError("xml_input must be a file path (str/bytes) or a file-like object.")

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
        categories = self.tree.xpath("//category")
        for category in categories:
            category_type = category.get("type", "").lower()
            category_name = category.get("name", "Unnamed Category")
            if category_type in ["parts", "part", "partBrand", "partType", "partItem", "partCategory"]:
                parts = category.xpath(".//part")
                for part in parts:
                    item_name = part.get("itemName", "Unknown Part")
                    for item in part.xpath("./item"):
                        spare_part_info = {
                            "category_name": category_name,
                            "item_name": item_name,
                            "spare_part_name": item.get("name", "N/A")
                        }
                        spare_parts_list.append(spare_part_info)
        return spare_parts_list