import shutil
import os
from config import Config as cf

def create_base():
    os.makedirs(cf.INPUT_DIR, exist_ok=True)
    os.makedirs(cf.OUTPUT_DIR, exist_ok=True)
    os.makedirs(cf.TEMP_DIR, exist_ok=True)

def create_temp_dir(path):

    os.makedirs(
        path,
        exist_ok=True
    )

def remove_temp_dir(path):

    if os.path.exists(path):
        shutil.rmtree(path)