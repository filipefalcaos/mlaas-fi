import csv
import json
import tarfile


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
