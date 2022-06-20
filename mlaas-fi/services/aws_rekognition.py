import boto3
from botocore.exceptions import ClientError


class AWSRekognition:
    def __init__(self, aws_config):
        self.client = boto3.client(
            'rekognition',
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key'],
            region_name=aws_config['region_name']
        )


    # Uses the "detect_labels" API from boto3 (Amazon Rekognition) to detect the labels in a list
    # of images
    def detect_labels(self, imgs_paths):
        labels = []
        for img_path in imgs_paths:
            with open(img_path, 'rb') as img_file:
                img = {'Bytes': img_file.read()}

            try:
                response = self.client.detect_labels(Image=img)
                response_labels = response['Labels']
                label_names = [response_label['Name'] for response_label in response_labels]
                labels.append(label_names)
            except ClientError:
                raise

        return labels


    # Uses the "detect_text" API from boto3 (Amazon Rekognition) to detect text occurrence (lines
    # only) in a list of images
    def detect_text(self, imgs_paths):
        texts = []
        for img_path in imgs_paths:
            with open(img_path, 'rb') as img_file:
                img = {'Bytes': img_file.read()}

            try:
                response = self.client.detect_text(Image=img)
                response_texts = response['TextDetections']
                texts_content = [resp_text['DetectedText'] for resp_text in response_texts if resp_text['Type'] == 'LINE']
                texts.append(texts_content)
            except ClientError:
                raise

        return texts


    # Uses the "detect_moderation_labels" API from boto3 (Amazon Rekognition) to detect unsafe
    # content in a list of images
    def detect_unsafe_labels(self, imgs_paths):
        labels = []
        for img_path in imgs_paths:
            with open(img_path, 'rb') as img_file:
                img = {'Bytes': img_file.read()}

            try:
                response = self.client.detect_moderation_labels(Image=img)
                response_labels = response['ModerationLabels']
                label_names = [response_label['Name'] for response_label in response_labels]
                labels.append(label_names)
            except ClientError:
                raise

        return labels


    # Uses the "recognize_celebrities" API from boto3 (Amazon Rekognition) to recognize celebrities
    # in a list of images
    def recognize_celebrities(self, imgs_paths):
        celebrities = []
        for img_path in imgs_paths:
            with open(img_path, 'rb') as img_file:
                img = {'Bytes': img_file.read()}

            try:
                response = self.client.recognize_celebrities(Image=img)
                response_celebrities = response['CelebrityFaces']
                celebrities_ids = [response_celebrity['Name'] for response_celebrity in response_celebrities]
                celebrities_ids = celebrities_ids[:1]  # Return only a single celebrity
                celebrities.append(celebrities_ids)
            except ClientError:
                raise

        return celebrities
