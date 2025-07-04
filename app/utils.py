import zipfile
from pathlib import Path

def extract_zip(zip_path, extract_to="repo"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to