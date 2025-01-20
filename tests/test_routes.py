import os
import pytest
import tempfile
from flask import Flask
from src.routes import bp
from src.product_details import ProductDetails

sample_xml_content = """
<export_full>
    <items>
        <item name="Product A" />
        <item name="Product B" />
    </items>
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
def flask_app(sample_xml_file):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), "../src/templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "../src/static"))
    app.register_blueprint(bp)
    app.config["TESTING"] = True
    app.config["product_details"] = ProductDetails(sample_xml_file)
    return app

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"XML Parser Test" in response.data

def test_get_total_products(client):
    response = client.get('/get_total_products')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_products" in data
    assert data["total_products"] == 2

def test_get_product_names(client):
    response = client.get('/get_product_names')
    assert response.status_code == 200
    data = response.get_json()
    assert "product_names" in data
    assert data["product_names"] == ["Product A", "Product B"]

def test_get_spare_parts(client):
    response = client.get('/get_spare_parts')
    assert response.status_code == 200
    assert response.get_json() == {}
