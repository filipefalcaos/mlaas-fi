import json
import tarfile


def extract_tarfile(path, output_dir):
    """
    Extracts the content of a given tar file
    :param path: The path to the tar file
    :param output_dir: The path to the output directory
    """

    tar_file = tarfile.open(path)
    tar_file.extractall(output_dir)
    tar_file.close()


def parse_json(path):
    """
    Parses the content of a JSON file

    :param path: The path to the JSON file
    :return: The dictionary with the parsed content
    """

    with open(path, 'r') as json_file:
        parsed_content = json.load(json_file)
        return parsed_content
