'''Main entry point for the Flask application.'''
import os
from flask import Flask
from dotenv import load_dotenv
from routes import bp
from product_details import ProductDetails
from file_handler import FileHandler

load_dotenv()
app = Flask(__name__)

ZIP_URL = os.getenv("ZIP_URL")
ZIP_FILENAME = os.getenv("ZIP_FILENAME")
XML_FILENAME = os.getenv("XML_FILENAME")

file_handler = FileHandler()
zip_path = file_handler.download_file(ZIP_URL, ZIP_FILENAME)
xml_path = file_handler.extract_file(zip_path, XML_FILENAME)

product_details = ProductDetails(xml_path)
app.config["product_details"] = product_details
app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
