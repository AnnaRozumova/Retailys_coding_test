from flask import Blueprint, render_template, jsonify
from xml_parser import XMLParser

bp = Blueprint('routes', __name__)

xml_file_path = "./data/export_full.xml"
# this expects that xml file does not change but in the future
# can be use kind of watchdog which reload the file
parser = XMLParser(xml_file_path)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/get_total_products', methods=['GET'])
def get_total_products():
    total_products = parser.get_total_products()
    return jsonify({"total_products": total_products})

@bp.route('/get_product_names', methods=['GET'])
def get_product_names():
    products = parser.get_products_list()
    product_names = [product["name"] for product in products]
    return jsonify({"product_names": product_names})

@bp.route('/get_spare_parts', methods=['GET'])
def get_spare_parts():
    spare_parts = parser.get_spare_parts()
    spare_part_names = [spare_part["spare_part_name"] for spare_part in spare_parts]
    if not spare_parts:
        return jsonify({"message": "No spare parts found"}), 404
    return jsonify({"spare_part_names": spare_part_names})
