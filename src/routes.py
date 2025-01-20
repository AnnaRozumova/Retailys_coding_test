'''Blueprint routse for the Flask application'''
from flask import Blueprint, render_template, jsonify, current_app

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    '''Render the main index page'''
    return render_template('index.html')

@bp.route('/get_total_products', methods=['GET'])
def get_total_products():
    '''Return total number of products on XML'''
    product_details = current_app.config["product_details"]
    total_products = product_details.parse_total_products()
    return jsonify({"total_products": total_products})

@bp.route('/get_product_names', methods=['GET'])
def get_product_names():
    '''Return all product names from the XML'''
    product_details = current_app.config["product_details"]
    products = product_details.parse_products()
    product_names = [product["name"] for product in products]
    return jsonify({"product_names": product_names})

@bp.route('/get_spare_parts', methods=['GET'])
def get_spare_parts():
    '''Return spare parts grouped by the associated item name'''
    product_details = current_app.config["product_details"]
    grouped_spare_parts = product_details.parse_spare_parts()
    return jsonify(grouped_spare_parts)
