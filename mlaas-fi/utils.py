import json
import os
import shutil
import tarfile

from PIL import Image


# Creates a directory in a given path if not existent
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# Deletes a directory
def delete_dir(dir_path):
    shutil.rmtree(dir_path)


# Recreates a directory if it already exists
def recreate_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


# Extracts the content of a tar file
def extract_tarfile(path, output_dir):
    tar_file = tarfile.open(path)
    tar_file.extractall(output_dir)
    tar_file.close()


# Parses the content of a JSON file
def parse_json(path):
    with open(path, 'r') as json_file:
        parsed_content = json.load(json_file)
        return parsed_content


# Dumps given data into a JSON file
def dump_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


# Checks wether a dict has a given key
def has_key(dict, key):
    return key in dict
