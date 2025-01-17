'''Blueprint routse for the Flask application'''
from flask import Blueprint, render_template, jsonify
from product_details import ProductDetails

bp = Blueprint('routes', __name__)

XML_FILE_PATH = "./data/export_full.xml"
# this expects that xml file does not change but in the future
# can be use kind of watchdog which reload the file
parser = ProductDetails(XML_FILE_PATH)

@bp.route('/')
def index():
    '''Render the main index page'''
    return render_template('index.html')

@bp.route('/get_total_products', methods=['GET'])
def get_total_products():
    '''Return total number of products on XML'''
    total_products = parser.parse_total_products()
    return jsonify({"total_products": total_products})

@bp.route('/get_product_names', methods=['GET'])
def get_product_names():
    '''Return all product names from the XML'''
    products = parser.parse_products()
    product_names = [product["name"] for product in products]
    return jsonify({"product_names": product_names})

@bp.route('/get_spare_parts', methods=['GET'])
def get_spare_parts():
    '''Return spare parts grouped by the associated item name'''
    grouped_spare_parts = parser.parse_spare_parts()
    return jsonify(grouped_spare_parts)
