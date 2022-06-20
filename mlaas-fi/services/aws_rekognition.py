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
    def __detect_labels(self, img):
        response = self.client.detect_labels(Image=img)
        response_labels = response['Labels']
        label_names = [response_label['Name'] for response_label in response_labels]
        return label_names


    # Uses the "detect_text" API from boto3 (Amazon Rekognition) to detect text occurrence (lines
    # only)
    def __detect_text(self, img):
        response = self.client.detect_text(Image=img)
        response_texts = response['TextDetections']
        texts_content = [resp_text['DetectedText'] for resp_text in response_texts if resp_text['Type'] == 'LINE']
        return texts_content


    # Uses the "detect_moderation_labels" API from boto3 (Amazon Rekognition) to detect unsafe
    # content
    def __detect_unsafe_labels(self, img):
        response = self.client.detect_moderation_labels(Image=img)
        response_labels = response['ModerationLabels']
        label_names = [response_label['Name'] for response_label in response_labels]
        return label_names


    # Uses the "recognize_celebrities" API from boto3 (Amazon Rekognition) to recognize celebrities
    def __recognize_celebrities(self, img):
        response = self.client.recognize_celebrities(Image=img)
        response_celebrities = response['CelebrityFaces']
        celebrities_ids = [response_celebrity['Name'] for response_celebrity in response_celebrities]
        celebrities_ids = celebrities_ids[:1]  # Return only a single celebrity
        return celebrities_ids
    

    # Runs a specific Rekognition service for a set of images
    def run_service(self, service_type, img_paths):
        # Retrieves the prediction function for the service type
        predict_function = None
        if service_type == "CELEBRITY_RECOGNITION":
            predict_function = self.__recognize_celebrities
        elif service_type == "LABEL_DETECTION":
            predict_function = self.__detect_labels
        elif service_type == "NUDITY_DETECTION" or service_type == "VIOLENCE_DETECTION":
            predict_function = self.__detect_unsafe_labels
        elif service_type == "TEXT_DETECTION":
            predict_function = self.__detect_text

        # Get the predictions for the images
        predictions = []
        for img_path in img_paths:
            with open(img_path, 'rb') as img_file:
                img = {'Bytes': img_file.read()}

            try:
                if predict_function is not None:
                    predictions.append(predict_function(img))
            except ClientError:
                raise('Failed to run AWS Rekognition service')

        return predictions
