import os
import pytest
from flask import Flask
from src.routes import bp

@pytest.fixture
def flask_app():
    # Setting up Flask application with the correct paths for templates and static files
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), "../src/templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "../src/static"))
    app.register_blueprint(bp)
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # Verify important content in the updated index.html
    assert b"<h1>XML Parser Test</h1>" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>' in response.data

def test_get_total_products(client):
    response = client.get('/get_total_products')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_products" in data
    assert isinstance(data["total_products"], int)

def test_get_product_names(client):
    response = client.get('/get_product_names')
    assert response.status_code == 200
    data = response.get_json()
    assert "product_names" in data
    assert isinstance(data["product_names"], list)

def test_get_spare_parts(client):
    response = client.get('/get_spare_parts')
    assert response.status_code in [200, 404]
    data = response.get_json()
    if response.status_code == 200:
        assert isinstance(data, dict)  # Check if the response is a dictionary
        for key, value in data.items():
            assert isinstance(key, str)  # Item name
            assert isinstance(value, list)  # List of spare parts
    else:
        assert "message" in data
        assert data["message"] == "No spare parts found"
