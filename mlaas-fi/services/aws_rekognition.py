from boto3 import client
from botocore.config import Config

from .utils import RETRY_TIMES


class AWSRekognition:
    def __init__(self, aws_config):
        config = Config(retries={'max_attempts': RETRY_TIMES, 'mode': 'standard'})
        self.client = client(
            'rekognition',
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key'],
            config=config,
            region_name=aws_config['region_name']
        )

    # Labels objects detected in an image
    # Leveraged API: detect_labels from boto3
    def __detect_labels(self, img):
        response = self.client.detect_labels(Image=img)
        response_labels = response['Labels']
        label_names = [response_label['Name'] for response_label in response_labels]
        return label_names

    # Detects text occurrences (lines only) in an image
    # Leveraged API: detect_text from boto3
    def __detect_text(self, img):
        response = self.client.detect_text(Image=img)
        response_texts = response['TextDetections']
        texts_content = [
            resp_text['DetectedText'] for resp_text in response_texts if resp_text['Type'] == 'LINE'
        ]
        return texts_content

    # Detects unsafe content (violence and adult) in an image
    # Leveraged API: detect_moderation_labels from boto3
    # TODO: handle different label types
    def __detect_unsafe_labels(self, img):
        response = self.client.detect_moderation_labels(Image=img)
        response_labels = response['ModerationLabels']
        label_names = [response_label['Name'] for response_label in response_labels]
        return label_names

    # Recognizes a single celebrity in an image (other celebrities found are not returned)
    # Leveraged API: recognize_celebrities from boto3
    def __recognize_celebrities(self, img):
        response = self.client.recognize_celebrities(Image=img)
        response_celebrities = response['CelebrityFaces']
        celebrities_ids = [
            response_celebrity['Name'] for response_celebrity in response_celebrities
        ]
        celebrities_ids = celebrities_ids[:1]  # Return only a single celebrity
        return celebrities_ids

    # Run an AWS Rekognition service for a given image
    def run_service(self, service, image):
        # Map a service to a prediction function
        service_map = {
            'CELEBRITY_RECOGNITION': self.__recognize_celebrities,
            'LABEL_DETECTION': self.__detect_labels,
            'NUDITY_DETECTION': self.__detect_unsafe_labels,
            'VIOLENCE_DETECTION': self.__detect_unsafe_labels,
            'TEXT_DETECTION': self.__detect_text
        }

        # Apply the function to the given image
        with open(image, 'rb') as img_file:
            img_payload = {'Bytes': img_file.read()}
        output = service_map[service](img_payload)
        return output
