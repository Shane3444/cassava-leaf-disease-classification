import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64
import shutil
import pandas as pd

@ensure_annotations
def read_yaml(path_to_yaml : Path) -> ConfigBox:
    """
    reads yaml file and returns ConfigBox

    Args:
    path_to_yaml (str): path like input

    Raises:
    ValueError: if yaml file is empty
    e: empty file

    Returns:
    ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file {path_to_yaml} loaded succesfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories : list, verbose = True):
    """
    create a list of directories

    Args:
    path_to_directories (list): list of path of directories
    ignore_log (bool, optional): ignore if multiple dirs are to be created. Defaults to false
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    save json data

    Args:
    path (Path): path to json file
    data (dict): data to be saved in file
    """

    with open(path, "w") as f:
        json.dump(data, f, indent = 4)
    
    logger.info(f"file saved at {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    load json file data

    Args:
    path (Path): path to json file

    Returns:
    ConfigBox: data as class attributes instead of dictionary
    """
    with open(path, "r") as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(path: Path, data: Any):
    """
    save binary file

    Args:
    path (Path): path to binary file
    data (Any): data to be saved as binary
    """
    joblib.dump(data, path)
    logger.info(f"binary file saved at {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    load binary data

    Args:
    path (Path): path to binary file

    Returns:
    Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"data loaded from binary file at {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    get size in KB

    Args:
    path (Path): path to file

    Returns:
    str: returns size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, 'rb') as f:
        return base64.b64encode(f.read())

def seperate_and_move_images(filepath = "artifacts/data_ingestion/"):
    """
    Given the filepath, move the images into seperate directories based on the class labels given in a csv file
    """
    try:
        data_dict = pd.read_csv(filepath + "train.csv")
        unique_labels = sorted(data_dict.label.unique())
        os.chdir(filepath + "train_images/")
        for label in unique_labels:
            os.makedirs(str(label))
        for i in range(len(data_dict)):
            shutil.move(data_dict.iloc[i].image_id, f"{data_dict.iloc[i].label}/")
    except Exception as e:
        raise e