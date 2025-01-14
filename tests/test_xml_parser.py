import pytest
from lxml import etree
from xml_parser import XMLParser
from io import BytesIO

# Sample XML data for testing
sample_xml = b"""
<catalog>
    <item name="Product A" />
    <item name="Product B" />
    <category type="parts" name="Spare Parts">
        <part itemName="Wheel">
            <item name="Front Wheel" />
            <item name="Rear Wheel" />
        </part>
    </category>
</catalog>
"""

@pytest.fixture
def parser():
    xml_file = BytesIO(sample_xml)
    xml_parser = XMLParser(xml_file)
    return xml_parser

def test_get_total_products(parser):
    assert parser.get_total_products() == 2  # Two "item" elements at root level

def test_get_products_list(parser):
    products_list = parser.get_products_list()
    assert len(products_list) == 2
    assert products_list[0]["name"] == "Product A"
    assert products_list[1]["name"] == "Product B"

def test_get_spare_parts(parser):
    spare_parts = parser.get_spare_parts()
    assert len(spare_parts) == 2
    assert spare_parts[0]["spare_part_name"] == "Front Wheel"
    assert spare_parts[1]["spare_part_name"] == "Rear Wheel"
