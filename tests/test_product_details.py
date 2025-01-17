import os
import pytest
from src.product_details import ProductDetails

@pytest.fixture
def sample_xml_file():
    # Path to the sample XML file in the tests directory
    return os.path.join(os.path.dirname(__file__), "sample_data.xml")

@pytest.fixture
def product_details(sample_xml_file):
    return ProductDetails(sample_xml_file)

def test_parse_total_products(product_details):
    assert product_details.parse_total_products() == 4

def test_parse_products(product_details):
    products = product_details.parse_products()
    assert len(products) == 4
    assert products[0]["name"] == "Product A"
    assert products[1]["name"] == "Product B"
    assert products[2]["name"] == "Engine Block"
    assert products[3]["name"] == "Cylinder Head"

def test_parse_spare_parts(product_details):
    spare_parts = product_details.parse_spare_parts()
    assert "Engine" in spare_parts
    assert "Engine Block" in spare_parts["Engine"]
    assert "Cylinder Head" in spare_parts["Engine"]
