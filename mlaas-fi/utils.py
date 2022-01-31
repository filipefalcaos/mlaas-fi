import csv
import json
import os
import shutil
import tarfile


# Creates a directory in a given path if not existent
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# Recreate a directory if it already exists
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
        json.dump(data, outfile, indent=2)


# Parses the AWS credentials from a CSV file
def parse_aws_credentials(path):
    credentials = {}
    with open(path, 'r') as cred_csv:
        next(cred_csv)
        reader = csv.reader(cred_csv)
        for row in reader:
            credentials['access_key_id'] = row[2]
            credentials['secret_access_key'] = row[3]

    return credentials


# Checks if a service is an AWS Rekognition service
def is_rekognition_service(service):
    rekognition_services = ["CELEBRITY_RECOGNITION", "LABEL_DETECTION",
                            "NUDITY_DETECTION", "TEXT_DETECTION", "VIOLENCE_DETECTION"]
    return service in rekognition_services
