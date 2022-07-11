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
        texts_content = [resp_text['DetectedText'] for resp_text in response_texts if resp_text['Type'] == 'LINE']
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
        celebrities_ids = [response_celebrity['Name'] for response_celebrity in response_celebrities]
        celebrities_ids = celebrities_ids[:1]  # Return only a single celebrity
        return celebrities_ids


    def run_service(self, service, images):
        # Map a service to a function
        service_fn = None
        if service == "CELEBRITY_RECOGNITION":
            service_fn = self.__recognize_celebrities
        elif service == "LABEL_DETECTION":
            service_fn = self.__detect_labels
        elif service == "NUDITY_DETECTION" or service == "VIOLENCE_DETECTION":
            service_fn = self.__detect_unsafe_labels
        elif service == "TEXT_DETECTION":
            service_fn = self.__detect_text

        # Apply the function to the given images
        output_list = []
        for image in images:
            with open(image, 'rb') as img_file:
                img = {'Bytes': img_file.read()}
            try:
                output = service_fn(img)
                output_list.append(output)
            except ClientError:
                print('Unable to run {} for input image {}'.format(service, image))
        
        return output_list
