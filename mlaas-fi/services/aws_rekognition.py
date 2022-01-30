import boto3
import csv

from botocore.exceptions import ClientError


def parse_aws_credentials(path):
    """
    Parses the AWS credentials from a CSV file

    :param path: The path to the credentials file
    :return: The dictionary with the parsed credentials
    """

    credentials = {}
    with open(path, 'r') as cred_csv:
        next(cred_csv)
        reader = csv.reader(cred_csv)
        for row in reader:
            credentials['access_key_id'] = row[2]
            credentials['secret_access_key'] = row[3]

    return credentials


def create_rekognition_client():
    """
    Creates an Amazon Rekognition boto3 client
    """

    credentials_file = 'credentials.csv'
    credentials = parse_aws_credentials(credentials_file)
    return boto3.client(
        'rekognition',
        aws_access_key_id=credentials['access_key_id'],
        aws_secret_access_key=credentials['secret_access_key'],
        region_name='us-east-2'
    )


def detect_labels_rekognition(rekognition_client, imgs_paths):
    """
    Uses the "detect_labels" API from boto3 to detect the labels in an image using
    the Amazon Rekognition service

    :param rekognition_client: The Amazon Rekognition client
    :param imgs_paths: The paths to the input images
    :return: The list of labels detected in every image
    """

    labels = []
    for img_path in imgs_paths:
        with open(img_path, 'rb') as img_file:
            img = {'Bytes': img_file.read()}

        # Perform the label detection on AWS
        try:
            response = rekognition_client.detect_labels(Image=img)
            response_labels = response['Labels']
            label_names = [response_label['Name'] for response_label in response_labels]
            labels.append(label_names)
        except ClientError:
            raise

    return labels


def detect_text_rekognition(rekognition_client, imgs_paths):
    """
    Uses the "detect_text" API from boto3 to detect text occurrence (lines only) in
    an image using the Amazon Rekognition service

    :param rekognition_client: The Amazon Rekognition client
    :param imgs_paths: The paths to the input images
    :return: The list of texts detected in every image
    """

    texts = []
    for img_path in imgs_paths:
        with open(img_path, 'rb') as img_file:
            img = {'Bytes': img_file.read()}

        # Perform the text detection on AWS
        try:
            response = rekognition_client.detect_text(Image=img)
            response_texts = response['TextDetections']
            texts_content = [resp_text['DetectedText'] for resp_text in response_texts if resp_text['Type'] == 'LINE']
            texts.append(texts_content)
        except ClientError:
            raise

    return texts


def detect_unsafe_labels_rekognition(rekognition_client, imgs_paths):
    """
    Uses the "detect_moderation_labels" API from boto3 to detect unsafe content in an
    image using the Amazon Rekognition service

    :param rekognition_client: The Amazon Rekognition client
    :param imgs_paths: The paths to the input images
    :return: The list of safe/unsafe labels detected in every image
    """

    labels = []
    for img_path in imgs_paths:
        with open(img_path, 'rb') as img_file:
            img = {'Bytes': img_file.read()}

        # Perform the unsafe content detection on AWS
        try:
            response = rekognition_client.detect_moderation_labels(Image=img)
            response_labels = response['ModerationLabels']
            label_names = [response_label['Name'] for response_label in response_labels]
            labels.append(label_names)
        except ClientError:
            raise

    return labels


def recognize_celebrities_rekognition(rekognition_client, imgs_paths):
    """
    Uses the "recognize_celebrities" API from boto3 to recognize celebrities in an
    image using the Amazon Rekognition service

    :param rekognition_client: The Amazon Rekognition client
    :param imgs_paths: The paths to the input images
    :return: The list of celebrities recognized in every image
    """

    celebrities = []
    for img_path in imgs_paths:
        with open(img_path, 'rb') as img_file:
            img = {'Bytes': img_file.read()}

        # Perform the celebrity recognition on AWS
        try:
            response = rekognition_client.recognize_celebrities(Image=img)
            response_celebrities = response['CelebrityFaces']
            celebrities_ids = [response_celebrity['Name'] for response_celebrity in response_celebrities]
            celebrities_ids = celebrities_ids[:1]  # Return only a single celebrity
            celebrities.append(celebrities_ids)
        except ClientError:
            raise

    return celebrities
