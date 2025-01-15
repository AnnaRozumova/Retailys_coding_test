from lxml import etree

class XMLParser:
    def __init__(self, xml_input):
        if isinstance(xml_input, (str, bytes)):
            self.xml_input = xml_input
        elif hasattr(xml_input, 'read'):
            self.xml_input = xml_input
        else:
            raise TypeError("xml_input must be a file path (str/bytes) or a file-like object.")
    
    def _get_iterparse_context(self, tags):
        """Helper function to create an iterparse context for the given tags."""
        return etree.iterparse(self.xml_input, events=("start", "end"), tag=tags)

    def get_total_products(self):
        '''Counts total items in XML using SAX parsing.'''
        total_products = 0
        for event, elem in self._get_iterparse_context("item"):
            if event == "end":
                total_products += 1
                elem.clear()  # Free memory for parsed element
        return total_products
    
    def get_products_list(self):
        '''Returns a list of item names from XML using SAX parsing.'''
        product_list = []
        for event, elem in self._get_iterparse_context("item"):
            if event == "end":
                product_info = {
                    "name": elem.get("name")
                }
                product_list.append(product_info)
                elem.clear()  # Free memory for parsed element
        return product_list
    
    def get_spare_parts(self):
        '''Returns a list of spare parts using SAX parsing.'''
        spare_parts_list = []
        current_category = None
        for event, elem in self._get_iterparse_context(["category", "part", "item"]):
            if event == "start" and elem.tag == "category":
                category_type = elem.get("type", "").lower()
                if category_type in ["parts", "part", "partBrand", "partType", "partItem", "partCategory"]:
                    current_category = {
                        "category_name": elem.get("name", "Unnamed Category"),
                        "parts": []
                    }
            elif event == "end" and elem.tag == "part" and current_category:
                item_name = elem.get("itemName", "Unknown Part")
                for item in elem.xpath("./item"):
                    spare_part_info = {
                        "category_name": current_category["category_name"],
                        "item_name": item_name,
                        "spare_part_name": item.get("name", "N/A")
                    }
                    spare_parts_list.append(spare_part_info)
                elem.clear()
            elif event == "end" and elem.tag == "category":
                current_category = None  # End of category; reset context
                elem.clear()
        return spare_parts_list
