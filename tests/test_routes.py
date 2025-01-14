import os
import pytest
from flask import Flask
from routes import bp

@pytest.fixture
def flask_app_fixture():
    app = Flask(__name__, template_folder=os.path.abspath("tests/templates"))
    app.register_blueprint(bp)
    app.config["TESTING"] = True
    return app

@pytest.fixture
def flask_test_client_fixture(flask_app_fixture):
    return flask_app_fixture.test_client()

def test_index_returns_200_status_code(flask_test_client_fixture):
    response = flask_test_client_fixture.get('/')
    assert response.status_code == 200

def test_get_total_products_returns_json(flask_test_client_fixture):
    response = flask_test_client_fixture.get('/get_total_products')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_products" in data

def test_get_product_names_returns_list_of_names(flask_test_client_fixture):
    response = flask_test_client_fixture.get('/get_product_names')
    assert response.status_code == 200
    data = response.get_json()
    assert "product_names" in data
    assert isinstance(data["product_names"], list)

def test_get_spare_parts_returns_list_or_404(flask_test_client_fixture):
    response = flask_test_client_fixture.get('/get_spare_parts')
    assert response.status_code in [200, 404]  # 200 if parts available, 404 otherwise
    data = response.get_json()
    if response.status_code == 200:
        assert "spare_part_names" in data
        assert isinstance(data["spare_part_names"], list)
    else:
        assert data["message"] == "No spare parts found"
