import zipfile
import pandas as pd

def unzip(file="202401_NFs.zip"):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall("data")
