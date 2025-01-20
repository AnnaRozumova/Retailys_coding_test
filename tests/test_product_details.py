import pytest
import os
import tempfile
from src.product_details import ProductDetails

sample_xml_content = """
<export_full>
    <items>
        <item name="Product A" />
        <item name="Product B" />
    </items>
    <parts>
        <part partName="Náhradní díly" itemName="Engine">
            <item name="Engine Block" />
            <item name="Cylinder Head" />
        </part>
    </parts>
</export_full>
"""

@pytest.fixture
def sample_xml_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(sample_xml_content)
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)

@pytest.fixture
def product_details(sample_xml_file):
    return ProductDetails(sample_xml_file)

def test_parse_total_products(product_details):
    assert product_details.parse_total_products() == 2

def test_parse_products(product_details):
    products = product_details.parse_products()
    assert len(products) == 2
    assert products[0]["name"] == "Product A"
    assert products[1]["name"] == "Product B"

def test_parse_spare_parts(product_details):
    spare_parts = product_details.parse_spare_parts()
    assert "Engine" in spare_parts
    assert "Engine Block" in spare_parts["Engine"]
    assert "Cylinder Head" in spare_parts["Engine"]

