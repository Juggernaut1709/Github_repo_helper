import zipfile
from pathlib import Path
import shutil
import git
import os

def extract_zip(zip_path, extract_to="repo"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

def clone_github_repo(url, dest="repo"):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        git.Repo.clone_from(url, dest)
        return True
    except Exception as e:
        print(f"❌ Git clone failed: {e}")
        return False