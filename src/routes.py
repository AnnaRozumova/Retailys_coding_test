from flask import Blueprint, render_template, jsonify
from product_details import ProductDetails

bp = Blueprint('routes', __name__)

xml_file_path = "./data/export_full.xml"
# this expects that xml file does not change but in the future
# can be use kind of watchdog which reload the file
parser = ProductDetails(xml_file_path)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/get_total_products', methods=['GET'])
def get_total_products():
    total_products = parser.parse_total_products()
    return jsonify({"total_products": total_products})

@bp.route('/get_product_names', methods=['GET'])
def get_product_names():
    products = parser.parse_products()
    product_names = [product["name"] for product in products]
    return jsonify({"product_names": product_names})

@bp.route('/get_spare_parts', methods=['GET'])
def get_spare_parts():
    grouped_spare_parts = parser.parse_spare_parts()
    return jsonify(grouped_spare_parts)
