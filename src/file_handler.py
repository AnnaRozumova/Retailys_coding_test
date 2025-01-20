import os
import zipfile
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class FileHandler:
    '''Handles downloading and extracting files.'''
    def __init__(self, download_dir="./data", extract_dir="./data"):
        self.download_dir = download_dir
        self.extract_dir = extract_dir

    def download_file(self, url, filename):
        '''Downloads a file from the specified URL.'''
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        file_path = os.path.join(self.download_dir, filename)
        logging.info(f"Downloading file from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"File downloaded to {file_path}")
        return file_path

    def extract_file(self, zip_path, target_filename):
        '''Extracts a specific file from a zip archive.'''
        if not os.path.exists(self.extract_dir):
            os.makedirs(self.extract_dir)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract(target_filename, self.extract_dir)

        extracted_path = os.path.join(self.extract_dir, target_filename)
        logging.info(f"Extracted file to {extracted_path}")
        return extracted_path
