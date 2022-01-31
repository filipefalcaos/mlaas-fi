from utils import is_rekognition_service
from .aws_rekognition import AWSRekognition


# Retrieves the predictions from a service for a given set of images
def get_predictions(expconfig, client, images):
    provider = expconfig['provider']
    service_type = expconfig['service_type']

    if provider == "AWS" and is_rekognition_service(service_type):
        if service_type == "CELEBRITY_RECOGNITION":
            return client.recognize_celebrities(images)
        elif service_type == "LABEL_DETECTION":
            return client.detect_labels(images)
        elif service_type == "NUDITY_DETECTION" or service_type == "VIOLENCE_DETECTION":
            return client.detect_unsafe_labels(images)
        elif service_type == "TEXT_DETECTION":
            return client.detect_text(images)


# Retrieves the client to invoke a machine learning cloud service
def get_client(expconfig):
    provider = expconfig['provider']
    service_type = expconfig['service_type']

    if provider == "AWS" and is_rekognition_service(service_type):
        return AWSRekognition(expconfig['credentials_file'])
